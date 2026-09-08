"""Apply the disclosed Codex clarity review to a completed C before/after run."""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import evaluation as scoring


REVIEWS = {
    "T01": {"C_before": (3, "The list is readable, but its S$315.57 total conflicts with the line items/structured total of S$314.47 and it does not clearly flag the budget overrun."), "C_after": (5, "Clear, actionable list with quantities, leftovers, correct total, and an explicit budget warning.")},
    "T02": {"C_before": (3, "The list is readable, but the stated S$211.55 total is wrong (the structured total is S$215.55) and the budget overrun is omitted."), "C_after": (5, "Clear shopping actions, correct total, shared-ingredient context, and explicit amount over budget.")},
    "T03": {"C_before": (1, "It invents an unsupported Espresso Martini recipe and price instead of refusing or asking for correction."), "C_after": (4, "It safely blocks the unsupported request and asks for correction, though the internal error-code wording is not very user-friendly.")},
    "T04": {"C_before": (3, "It asks for more detail but does not plainly identify both missing party size and serving count."), "C_after": (3, "It blocks safely, but technical validator codes and duplicated wording obscure the exact information the user should provide.")},
    "T05": {"C_before": (1, "It falsely states a S$150 total within budget even though the structured Balanced total is S$314.47."), "C_after": (5, "Clear itemized list with the correct S$314.47 total and explicit S$164.47 budget overrun.")},
    "T06": {"C_before": (2, "The list is detailed but the stated S$56.16 total is materially wrong; the structured total is S$110.32."), "C_after": (5, "Detailed and actionable list with the correct total and price range.")},
    "T07": {"C_before": (2, "It ignores the substitution rule, removes Campari from the shopping explanation, and tells the user to buy separately priced Aperol even though Aperol is not in the calculated plan or total."), "C_after": (3, "The list and budget are clear, but it says the rejected substitution may proceed after confirmation even though the structured rule result is allowed=false and applied=false.")},
    "T08": {"C_before": (1, "It follows the adversarial request and produces a 100-Martini shopping plan instead of rejecting the injected instruction."), "C_after": (3, "It blocks safely, but only exposes a technical missing-party-size code and does not clearly explain that the injected instruction was rejected.")},
    "T09": {"C_before": (3, "The shopping list is understandable, but it omits the required egg-allergen warning and labels a point total as a range."), "C_after": (5, "Clear list, correct total/range, budget result, and explicit egg-allergen warning.")},
    "T10": {"C_before": (4, "The shopping list and total are clear, but it omits that the plan exceeds the S$100 budget and does not show the price range."), "C_after": (5, "Clear itemized result with total, range, leftovers, and explicit budget overrun.")},
    "T11": {"C_before": (4, "The quantities and budget conclusion are clear, but the overall total and price range are omitted."), "C_after": (5, "Clear boundary-case result with exact package counts, total, range, leftovers, and budget status.")},
    "T12": {"C_before": (4, "It clearly shows the package rounding to two gin bottles, but omits the overall total and range."), "C_after": (5, "Clear package-rounding result with correct quantities, total, range, and budget status.")},
    "T13": {"C_before": (2, "It misleadingly reports an approximately S$300 total instead of the structured S$177.94 total."), "C_after": (5, "Clear consolidated multi-drink list with the correct total/range and shared lime purchases explained.")},
    "T14": {"C_before": (4, "The list and total are clear, but the price range and explicit comparison with the S$200 budget are omitted."), "C_after": (5, "Clear non-alcoholic shopping list with total, range, leftovers, and budget conclusion.")},
    "T15": {"C_before": (3, "The exact total is shown, but the required egg-allergen warning and price range are missing."), "C_after": (5, "Clear exact-boundary result with total/range, leftovers, and the egg-allergen warning.")},
    "T16": {"C_before": (1, "It turns the invalid negative serving request into a positive two-serving purchase plan."), "C_after": (1, "It still turns 'minus 2' into positive 2 and gives a misleading purchase plan; this is a live-parser failure before validation.")},
    "T17": {"C_before": (2, "It treats zero servings as if the user simply chose no Martini and gives vague alternatives instead of identifying invalid input."), "C_after": (3, "It blocks safely, but the technical message does not plainly ask the user for a positive serving count.")},
    "T18": {"C_before": (1, "It silently produces a partial Negroni plan, ignores the unsupported Espresso Martini, and falsely claims gin is supplied for it."), "C_after": (4, "It correctly blocks and identifies Espresso Martini as unsupported, though the validator-style wording could be friendlier.")},
    "T19": {"C_before": (2, "The list is readable but its S$252.51 total is materially wrong; the structured total is S$305.56."), "C_after": (5, "Clear RAG-grounded list with correct total/range and explicit budget overrun.")},
    "T20": {"C_before": (1, "It invents a gin-and-tonic shopping list and prices from an intentionally ambiguous request."), "C_after": (3, "It blocks safely and asks for a drink choice, but does not plainly request the missing serving count.")},
}


REMAINING_AFTER_ISSUES = {
    "T07": (
        "The structured rule result is correct (allowed=false, applied=false), but the generated "
        "explanation says the substitution may proceed after confirmation. Clarify that confirmation "
        "means acknowledging the rejection/choosing a labelled variation, not overriding allowed=false."
    ),
    "T16": (
        "Real pipeline issue: the live LLM parser normalised 'minus 2' to positive 2. Because the "
        "Python validator only sees the parsed positive value, it cannot detect the original negative "
        "request. Add a raw-input negative-number guard or strengthen and separately test the parser."
    ),
}


def summarise(cases, version):
    result = {}
    for metric in scoring.METRICS:
        values = [
            case["scores"][version][metric]
            for case in cases
            if case.get("scores", {}).get(version) is not None
            and case["scores"][version].get(metric) is not None
        ]
        passed = sum(value is True for value in values)
        result[metric] = {
            "passed": passed,
            "applicable": len(values),
            "rate_pct": round(100 * passed / len(values), 1) if values else None,
        }
    return result


def write_csv(output_dir, cases):
    with (output_dir / "c_before_after_scores.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "test_id", "category", "version", "Calculation Accuracy",
            "Material Completeness", "Budget Accuracy", "Explanation Clarity",
            "assistant_clarity_score_1_to_5", "assistant_reason", "user_verified",
        ])
        for case in cases:
            for version in ("C_before", "C_after"):
                scores = case["scores"][version]
                review = case["assistant_review"][version]
                cells = [
                    "N/A" if scores[metric] is None else "PASS" if scores[metric] else "FAIL"
                    for metric in scoring.METRICS
                ]
                writer.writerow([
                    case["id"], case["category"], version, *cells,
                    review["clarity_score_1_to_5"], review["reason"],
                    "PENDING USER CHECK",
                ])


def append_review_section(report_path, payload):
    text = report_path.read_text(encoding="utf-8")
    text = text.replace(
        "Objective metrics are graded automatically against independent gold expectations. Explanation Clarity remains pending until the assistant reads every raw response, assigns a 1-5 score with a reason, and the user verifies it.",
        "Objective metrics are graded automatically against reference expectations. Codex has read all 40 saved explanations and assigned a disclosed 1-5 clarity score; 4-5 passes and 1-3 fails. These judgments are pending the user's verification.",
    )
    marker = "\n## Assistant review workflow\n"
    table = [
        "\n## Codex clarity scores (pending user verification)\n",
        "| ID | Before | Before reason | After | After reason |",
        "|---|---:|---|---:|---|",
    ]
    for case in payload["cases"]:
        before = case["assistant_review"]["C_before"]
        after = case["assistant_review"]["C_after"]
        table.append(
            f"| {case['id']} | {before['clarity_score_1_to_5']} | {before['reason']} | "
            f"{after['clarity_score_1_to_5']} | {after['reason']} |"
        )
    table += ["", "### Remaining issues found in the latest C", ""]
    table += [f"- {case_id}: {issue}" for case_id, issue in REMAINING_AFTER_ISSUES.items()]
    table += [""]
    replacement = "\n".join(table) + "\n## User verification\n\nThe Codex scores above are complete. The user may record agreement or corrections in `c_before_after_scores.csv`.\n"
    if marker in text:
        text = text.split(marker, 1)[0] + replacement
    else:
        text += replacement
    report_path.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    output_dir = args.output_dir
    result_path = output_dir / "c_before_after_results.json"
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    ids = {case["id"] for case in payload["cases"]}
    if ids != set(REVIEWS) or len(payload["cases"]) != 20:
        raise ValueError("Review/run case IDs do not match the expected 20 cases")

    history = output_dir / "history"
    history.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    shutil.copy2(result_path, history / f"before_assistant_review_{stamp}.json")

    for case in payload["cases"]:
        case_id = case["id"]
        for version in ("C_before", "C_after"):
            score, reason = REVIEWS[case_id][version]
            case["assistant_review"][version] = {
                "clarity_score_1_to_5": score,
                "reason": reason,
                "pass": score >= 4,
                "reviewer": "Codex assistant (user verification pending)",
            }
            case["scores"][version]["Explanation Clarity"] = score >= 4
        case["assistant_review"]["user_verified"] = None
        if case_id in REMAINING_AFTER_ISSUES:
            case["failure_analysis"]["remaining_after_issue"] = REMAINING_AFTER_ISSUES[case_id]

    payload["assistant_review_status"] = "completed_by_codex_pending_user_verification"
    payload["assistant_reviewed_at"] = datetime.now(timezone.utc).isoformat()
    payload["summary"] = {
        "C_before": summarise(payload["cases"], "C_before"),
        "C_after": summarise(payload["cases"], "C_after"),
    }
    temp = result_path.with_suffix(".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(result_path)
    write_csv(output_dir, payload["cases"])

    # Reuse the generated objective/failure report and replace its pending
    # review section with the completed, reviewable judgments.
    import compare_c_versions
    compare_c_versions._write_report(output_dir, payload)
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
