"""Run legacy C and latest C end to end on the same 20 raw prompts.

This comparison intentionally does not use an LLM judge. Objective fields are
graded against the independent GOLD expectations in evaluation.py. Generated
explanations are saved for a first-pass assistant review followed by the user's
manual verification.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import Assignment as core
import evaluation as scoring
import legacy_c


ROOT_CAUSE_AND_FIX = {
    "T03": (
        "The old parser could flag an unsupported drink, but the old validator treated that flag as metadata and never stopped the workflow.",
        "Promote unsupported_drinks to UNSUPPORTED_DRINKS and return status=blocked before retrieval/calculation.",
    ),
    "T04": (
        "The old validator checked only whether missing fields were flagged; it did not turn a correctly flagged omission into a blocking error.",
        "Promote missing_fields to MISSING_REQUIRED_FIELDS, stop downstream modules, and return a corrective explanation.",
    ),
    "T07": (
        "The old parser stored the request only as free-text restrictions and the pipeline never called the substitution rule inside the real workflow.",
        "Extract a structured substitution request, evaluate it inside C, return substitution_decisions, and never apply an unapproved replacement.",
    ),
    "T08": (
        "The old run did not have a workflow gate after parsing, so an adversarial or incomplete parse could continue to a misleading plan.",
        "Keep customer text delimited as untrusted data, validate the live parse, and block invalid results before RAG/calculation.",
    ),
    "T16": (
        "The old validator had no positive-integer check, so negative servings reached deterministic arithmetic.",
        "Require every serving count to be a positive integer before calculation.",
    ),
    "T17": (
        "The old validator had no positive-integer check, so zero servings could create an empty or zero-quantity plan presented as success.",
        "Reject zero servings before retrieval/calculation and ask for a positive count.",
    ),
    "T18": (
        "The old workflow did not block a mixed request when unsupported_drinks was non-empty, so it could silently produce a partial plan.",
        "Treat any unsupported requested drink as a blocking condition until the user confirms a corrected request.",
    ),
    "T20": (
        "The old validator did not turn ambiguity/missing drink and serving fields into a blocking state.",
        "Block ambiguous requirements and state exactly which fields the user must provide.",
    ),
}


def _version_result(run_fn, tc: dict) -> dict:
    try:
        return {"status": "completed", "output": run_fn(tc), "error": None}
    except Exception as exc:  # keep the paired run and evidence even if one side fails
        return {
            "status": "error",
            "output": None,
            "error": f"{type(exc).__name__}: {exc}",
        }


def _score(tc: dict, wrapped: dict, pipeline: core.PartyPourPipeline) -> tuple[dict | None, list[str]]:
    output = wrapped.get("output")
    if not isinstance(output, dict) or "calculation_by_tier" not in output:
        return None, ["RUN_ERROR"]
    return scoring.score_c(tc, output, pipeline)


def _parsed_matches_reference(actual: dict | None, expected: dict) -> bool:
    if not isinstance(actual, dict):
        return False
    actual_drinks = sorted(
        (str(item.get("name")), item.get("servings")) for item in actual.get("drinks", [])
    )
    expected_drinks = sorted(
        (str(item.get("name")), item.get("servings")) for item in expected.get("drinks", [])
    )
    return (
        actual.get("party_size") == expected.get("party_size")
        and actual.get("budget") == expected.get("budget")
        and actual_drinks == expected_drinks
        and sorted(actual.get("unsupported_drinks", []))
        == sorted(expected.get("unsupported_drinks", []))
        and set(actual.get("missing_fields", [])) == set(expected.get("missing_fields", []))
    )


def _observed(version: dict, scores: dict | None, diagnostics: list[str], tc: dict) -> dict:
    output = version.get("output") or {}
    balanced = output.get("calculation_by_tier", {}).get("Balanced", {})
    return {
        "run_status": version.get("status"),
        "error": version.get("error"),
        "expected_status": scoring.GOLD[tc["id"]]["status"],
        "actual_status": output.get("status"),
        "parser_matches_reference": _parsed_matches_reference(
            output.get("parsed_request"), tc["parsed_override"]
        ),
        "parse_violations": output.get("parse_violations", []),
        "balanced_total_sgd": balanced.get("total_cost_sgd"),
        "balanced_line_count": len(balanced.get("lines", [])),
        "scores_before_assistant_review": scores,
        "diagnostics": diagnostics,
    }


def _actual_failure_reason(observed: dict, scores: dict | None) -> str:
    """Describe the direct, observed failure before discussing its design cause."""
    reasons = []
    if observed.get("run_status") == "error":
        reasons.append(f"The run raised an error: {observed.get('error')}")
    if not observed.get("parser_matches_reference"):
        reasons.append(
            "The live LLM parser did not match the reference party size, budget, "
            "drink/serving list, or missing/unsupported fields."
        )
    if observed.get("actual_status") != observed.get("expected_status"):
        reasons.append(
            f"The workflow returned status={observed.get('actual_status')} but the "
            f"expected status was {observed.get('expected_status')}."
        )
    if scores:
        failed = [
            metric for metric in scoring.METRICS[:3]
            if scores.get(metric) is False
        ]
        if failed:
            reasons.append("Failed objective checks: " + ", ".join(failed) + ".")
    failed_diagnostics = [
        item for item in observed.get("diagnostics", [])
        if isinstance(item, str) and item.upper() == item and "_" in item
    ]
    if failed_diagnostics:
        reasons.append("Diagnostic evidence: " + ", ".join(failed_diagnostics) + ".")
    return " ".join(reasons) if reasons else "No objective failure was observed in this run."


def _write_checkpoint(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def _summary(cases: list[dict], version_name: str) -> dict[str, dict[str, Any]]:
    result = {}
    for metric in scoring.METRICS:
        values = []
        for case in cases:
            scores = case.get("scores", {}).get(version_name)
            if scores is not None and scores.get(metric) is not None:
                values.append(scores[metric])
        passed = sum(value is True for value in values)
        result[metric] = {
            "passed": passed,
            "applicable": len(values),
            "rate_pct": round(100 * passed / len(values), 1) if values else None,
        }
        if metric == "Explanation Clarity" and len(values) < len(cases):
            result[metric]["status"] = "PARTIAL_ASSISTANT_REVIEW"
    return result


def _write_csv(output_dir: Path, cases: list[dict]) -> None:
    with (output_dir / "c_before_after_scores.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "test_id", "category", "version",
            "Calculation Accuracy", "Material Completeness", "Budget Accuracy",
            "Explanation Clarity", "assistant_clarity_score_1_to_5",
            "assistant_reason", "user_verified",
        ])
        for case in cases:
            for version in ("C_before", "C_after"):
                scores = case.get("scores", {}).get(version)
                cells = [] if scores is None else [
                    "N/A" if scores[metric] is None else "PASS" if scores[metric] else "FAIL"
                    for metric in scoring.METRICS
                ]
                if not cells:
                    cells = ["ERROR", "ERROR", "ERROR", "ERROR"]
                review = case.get("assistant_review", {}).get(version, {})
                clarity_score = review.get("clarity_score_1_to_5")
                reason = review.get("reason")
                writer.writerow([
                    case["id"], case["category"], version, *cells,
                    clarity_score if clarity_score is not None else "PENDING",
                    reason or "PENDING ASSISTANT REVIEW", "PENDING USER CHECK",
                ])


def _write_report(output_dir: Path, payload: dict) -> None:
    reviewed_count = sum(
        case.get("assistant_review", {}).get(version, {}).get("clarity_score_1_to_5") is not None
        for case in payload["cases"] for version in ("C_before", "C_after")
    )
    review_note = (
        f"Codex clarity reviews are present for {reviewed_count}/40 outputs; any newly rerun "
        "output remains pending until Codex reads it again. All scores remain pending user verification."
        if reviewed_count
        else "Explanation Clarity remains pending until Codex reads every raw response, assigns a 1-5 score with a reason, and the user verifies it."
    )
    lines = [
        "# Variant C end-to-end before/after evaluation",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        f"Generator model for both versions: `{payload['generator_model']}`",
        "",
        "Both versions start from the same 20 raw customer messages and call their own real parser and explanation prompts. C_before restores the original code from Assignment.ipynb; C_after is the latest implementation. No reference parse is supplied to either version.",
        "",
        "Objective metrics are graded automatically against independent gold expectations. " + review_note,
        "",
        "## Objective score summary",
        "",
        "| Version | Calculation Accuracy | Material Completeness | Budget Accuracy | Explanation Clarity |",
        "|---|---:|---:|---:|---:|",
    ]
    for version in ("C_before", "C_after"):
        summary = payload["summary"][version]
        cells = []
        for metric in scoring.METRICS:
            item = summary[metric]
            if item.get("rate_pct") is None:
                cells.append(item.get("status", "Not run"))
            else:
                cells.append(f"{item['rate_pct']:.1f}% ({item['passed']}/{item['applicable']})")
        lines.append(f"| {version} | " + " | ".join(cells) + " |")

    lines += [
        "",
        "## Per-case evidence, causes, and fixes",
        "",
        "| ID | Category | Before status | After status | Before parser matched | After parser matched | Cause and implemented fix |",
        "|---|---|---|---|---|---|---|",
    ]
    for case in payload["cases"]:
        before = case["observed"]["C_before"]
        after = case["observed"]["C_after"]
        actual = case.get("failure_analysis", {}).get("actual_failure_reason", "No recorded failure evidence.")
        cause = case.get("failure_analysis", {}).get("root_cause", "No predefined legacy defect for this case.")
        fix = case.get("failure_analysis", {}).get("implemented_fix", "No case-specific change required.")
        lines.append(
            f"| {case['id']} | {case['category']} | {before.get('actual_status')} | "
            f"{after.get('actual_status')} | {before.get('parser_matches_reference')} | "
            f"{after.get('parser_matches_reference')} | Observed: {actual} Root cause: {cause} Fix: {fix} |"
        )

    lines += [
        "",
        "## Codex clarity review (pending user verification)",
        "",
        "| ID | Before score | Before reason | After score | After reason |",
        "|---|---:|---|---:|---|",
    ]
    for case in payload["cases"]:
        before_review = case.get("assistant_review", {}).get("C_before", {})
        after_review = case.get("assistant_review", {}).get("C_after", {})
        before_score = before_review.get("clarity_score_1_to_5")
        after_score = after_review.get("clarity_score_1_to_5")
        lines.append(
            f"| {case['id']} | {before_score if before_score is not None else 'PENDING'} | "
            f"{before_review.get('reason') or 'Pending review after rerun.'} | "
            f"{after_score if after_score is not None else 'PENDING'} | "
            f"{after_review.get('reason') or 'Pending review after rerun.'} |"
        )

    lines += [
        "",
        "## Assistant review workflow",
        "",
        "1. The assistant reads `c_before_after_results.json`, including all 40 generated outputs.",
        "2. The assistant assigns Explanation Clarity from 1-5 and writes a short reason for each output.",
        "3. Scores of 4-5 pass; 1-3 fail.",
        "4. The user checks the assistant's scores and records agreement or changes in the CSV.",
        "",
        "The assistant review is deliberately separate from the API generation run so the evaluator is not the same model call that produced the answer.",
        "",
    ]
    (output_dir / "C_BEFORE_AFTER_E2E_REPORT.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="evaluation_results/c_before_after_e2e")
    parser.add_argument("--fresh", action="store_true",
                        help="rerun completed cases instead of resuming the checkpoint")
    parser.add_argument(
        "--case", action="append", dest="case_ids",
        choices=[tc["id"] for tc in core.TEST_CASES],
        help="rerun only this case (repeat the option for more than one case)",
    )
    args = parser.parse_args()

    if not core.API_KEY:
        parser.error("This end-to-end comparison requires PARTYPOUR_API_KEY or OPENAI_API_KEY")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / "c_before_after_results.json"
    existing: dict[str, Any] = {}
    if result_path.exists():
        try:
            existing = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            existing = {}
        history = output_dir / "history"
        history.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        shutil.copy2(result_path, history / f"c_before_after_before_{stamp}.json")

    existing_by_id = {
        case["id"]: case for case in existing.get("cases", [])
    }
    selected_ids = set(args.case_ids or [])

    reference_pipeline = core.PartyPourPipeline()
    before_pipeline = legacy_c.LegacyPartyPourPipeline()
    cases = []
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator_model": core.GEN_MODEL,
        "case_count": len(core.TEST_CASES),
        "comparison_scope": "same_raw_prompts_live_end_to_end",
        "legacy_source": "Assignment.ipynb original code cells",
        "reference_parses_supplied_to_systems": False,
        "estimated_api_calls": {
            "C_before": "60 (20 parser + 20 recommendation + 20 explanation)",
            "C_after": "about 46 (20 parser + 13 valid cases x 2 output calls)",
            "judge": "0 (assistant reviews saved text after the run)",
        },
        "assistant_clarity_rubric": {
            "5": "Very clear, accurate, actionable, and covers the important result/rule context.",
            "4": "Clear and useful with only a minor omission or wording issue.",
            "3": "Understandable but misses an important action, number, warning, or correction.",
            "2": "Materially confusing, incomplete, or potentially misleading.",
            "1": "Unusable, contradictory, or fails to explain the result.",
            "pass_rule": "4-5 PASS; 1-3 FAIL",
        },
        "assistant_review_status": "pending",
        "rerun_scope": "all" if args.fresh else sorted(selected_ids) if selected_ids else "resume",
        "cases": cases,
        "summary": {},
    }

    for index, tc in enumerate(core.TEST_CASES, start=1):
        old_case = existing_by_id.get(tc["id"], {})
        force_rerun = args.fresh or tc["id"] in selected_ids
        before = old_case.get("outputs", {}).get("C_before")
        after = old_case.get("outputs", {}).get("C_after")
        if force_rerun:
            before = None
            after = None
        if not isinstance(before, dict) or before.get("status") != "completed":
            before = _version_result(
                lambda case: legacy_c.run_variant_C_legacy_end_to_end(case, before_pipeline), tc
            )
        if not isinstance(after, dict) or after.get("status") != "completed":
            after = _version_result(
                lambda case: core.run_variant_C_full_system(case, reference_pipeline), tc
            )

        before_scores, before_diagnostics = _score(tc, before, reference_pipeline)
        after_scores, after_diagnostics = _score(tc, after, reference_pipeline)
        # A rerun output needs a fresh assistant review. Reviews for unchanged
        # cases are preserved so `--case T07` does not erase the other 19.
        preserved_review = old_case.get("assistant_review", {}) if not force_rerun else {}
        if before_scores is not None:
            old_score = preserved_review.get("C_before", {}).get("clarity_score_1_to_5")
            before_scores["Explanation Clarity"] = (
                old_score >= 4 if isinstance(old_score, (int, float)) else None
            )
        if after_scores is not None:
            old_score = preserved_review.get("C_after", {}).get("clarity_score_1_to_5")
            after_scores["Explanation Clarity"] = (
                old_score >= 4 if isinstance(old_score, (int, float)) else None
            )

        cause, fix = ROOT_CAUSE_AND_FIX.get(
            tc["id"],
            (
                "No known legacy workflow defect is expected; any failure should be traced to the saved parser/output evidence.",
                "No case-specific modification; retain as a regression/control case.",
            ),
        )
        before_observed = _observed(before, before_scores, before_diagnostics, tc)
        after_observed = _observed(after, after_scores, after_diagnostics, tc)
        case_result = {
            "id": tc["id"],
            "category": tc["category"],
            "message": tc["message"],
            "expected": scoring.GOLD[tc["id"]],
            "outputs": {"C_before": before, "C_after": after},
            "scores": {"C_before": before_scores, "C_after": after_scores},
            "observed": {
                "C_before": before_observed,
                "C_after": after_observed,
            },
            "failure_analysis": {
                "actual_failure_reason": _actual_failure_reason(before_observed, before_scores),
                "root_cause": cause,
                "implemented_fix": fix,
            },
            "assistant_review": preserved_review or {
                "C_before": {"clarity_score_1_to_5": None, "reason": None},
                "C_after": {"clarity_score_1_to_5": None, "reason": None},
                "user_verified": None,
            },
        }
        cases.append(case_result)
        payload["generated_at"] = datetime.now(timezone.utc).isoformat()
        payload["summary"] = {
            "C_before": _summary(cases, "C_before"),
            "C_after": _summary(cases, "C_after"),
        }
        _write_checkpoint(result_path, payload)
        print(f"[{index:02d}/20] {tc['id']} saved")

    _write_csv(output_dir, cases)
    _write_report(output_dir, payload)
    print(f"Results written to {output_dir.resolve()}")
    print("Explanation clarity: pending assistant review, then user verification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
