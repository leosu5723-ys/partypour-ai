# Variant C end-to-end before/after evaluation

Generated: 2026-09-07T10:15:37.579033+00:00

Generator model for both versions: `openai/gpt-4o-mini`

Both versions start from the same 20 raw customer messages and call their own real parser and explanation prompts. C_before restores the original code from Assignment.ipynb; C_after is the latest implementation. No reference parse is supplied to either version.

Objective metrics are graded automatically against independent gold expectations. Codex clarity reviews are present for 40/40 outputs; any newly rerun output remains pending until Codex reads it again. All scores remain pending user verification.

## Objective score summary

| Version | Calculation Accuracy | Material Completeness | Budget Accuracy | Explanation Clarity |
|---|---:|---:|---:|---:|
| C_before | 65.0% (13/20) | 100.0% (13/13) | 100.0% (12/12) | 20.0% (4/20) |
| C_after | 95.0% (19/20) | 100.0% (13/13) | 100.0% (12/12) | 70.0% (14/20) |

## Per-case evidence, causes, and fixes

| ID | Category | Before status | After status | Before parser matched | After parser matched | Cause and implemented fix |
|---|---|---|---|---|---|---|
| T01 | normal_calculation | ok | ok | True | True | Observed: No objective failure was observed in this run. Root cause: No known legacy workflow defect is expected; any failure should be traced to the saved parser/output evidence. Fix: No case-specific modification; retain as a regression/control case. |
| T02 | shared_ingredient | ok | ok | True | True | Observed: No objective failure was observed in this run. Root cause: No known legacy workflow defect is expected; any failure should be traced to the saved parser/output evidence. Fix: No case-specific modification; retain as a regression/control case. |
| T03 | unsupported_drink | ok | blocked | False | False | Observed: The live LLM parser did not match the reference party size, budget, drink/serving list, or missing/unsupported fields. The workflow returned status=ok but the expected status was blocked. Failed objective checks: Calculation Accuracy. Diagnostic evidence: STATUS_MISMATCH. Root cause: The old parser could flag an unsupported drink, but the old validator treated that flag as metadata and never stopped the workflow. Fix: Promote unsupported_drinks to UNSUPPORTED_DRINKS and return status=blocked before retrieval/calculation. |
| T04 | missing_information | ok | blocked | False | False | Observed: The live LLM parser did not match the reference party size, budget, drink/serving list, or missing/unsupported fields. The workflow returned status=ok but the expected status was blocked. Failed objective checks: Calculation Accuracy. Diagnostic evidence: STATUS_MISMATCH. Root cause: The old validator checked only whether missing fields were flagged; it did not turn a correctly flagged omission into a blocking error. Fix: Promote missing_fields to MISSING_REQUIRED_FIELDS, stop downstream modules, and return a corrective explanation. |
| T05 | budget_insufficient | ok | ok | True | True | Observed: No objective failure was observed in this run. Root cause: No known legacy workflow defect is expected; any failure should be traced to the saved parser/output evidence. Fix: No case-specific modification; retain as a regression/control case. |
| T06 | non_alcoholic | ok | ok | True | True | Observed: No objective failure was observed in this run. Root cause: No known legacy workflow defect is expected; any failure should be traced to the saved parser/output evidence. Fix: No case-specific modification; retain as a regression/control case. |
| T07 | rejected_substitution | ok | ok | True | True | Observed: Diagnostic evidence: SUBSTITUTION_PIPELINE_MISMATCH. Root cause: The old parser stored the request only as free-text restrictions and the pipeline never called the substitution rule inside the real workflow. Fix: Extract a structured substitution request, evaluate it inside C, return substitution_decisions, and never apply an unapproved replacement. |
| T08 | prompt_injection | ok | blocked | False | False | Observed: The live LLM parser did not match the reference party size, budget, drink/serving list, or missing/unsupported fields. The workflow returned status=ok but the expected status was blocked. Failed objective checks: Calculation Accuracy. Diagnostic evidence: STATUS_MISMATCH, BLOCKED_CASE_GENERATED_PLAN. Root cause: The old run did not have a workflow gate after parsing, so an adversarial or incomplete parse could continue to a misleading plan. Fix: Keep customer text delimited as untrusted data, validate the live parse, and block invalid results before RAG/calculation. |
| T09 | allergen_warning | ok | ok | True | True | Observed: No objective failure was observed in this run. Root cause: No known legacy workflow defect is expected; any failure should be traced to the saved parser/output evidence. Fix: No case-specific modification; retain as a regression/control case. |
| T10 | margarita_now_supported | ok | ok | True | True | Observed: No objective failure was observed in this run. Root cause: No known legacy workflow defect is expected; any failure should be traced to the saved parser/output evidence. Fix: No case-specific modification; retain as a regression/control case. |
| T11 | package_exact_boundary | ok | ok | True | True | Observed: No objective failure was observed in this run. Root cause: No known legacy workflow defect is expected; any failure should be traced to the saved parser/output evidence. Fix: No case-specific modification; retain as a regression/control case. |
| T12 | package_rounding_over_boundary | ok | ok | True | True | Observed: No objective failure was observed in this run. Root cause: No known legacy workflow defect is expected; any failure should be traced to the saved parser/output evidence. Fix: No case-specific modification; retain as a regression/control case. |
| T13 | multi_drink_shared_lime | ok | ok | True | True | Observed: No objective failure was observed in this run. Root cause: No known legacy workflow defect is expected; any failure should be traced to the saved parser/output evidence. Fix: No case-specific modification; retain as a regression/control case. |
| T14 | budget_sufficient | ok | ok | True | True | Observed: No objective failure was observed in this run. Root cause: No known legacy workflow defect is expected; any failure should be traced to the saved parser/output evidence. Fix: No case-specific modification; retain as a regression/control case. |
| T15 | budget_exact_boundary | ok | ok | True | True | Observed: No objective failure was observed in this run. Root cause: No known legacy workflow defect is expected; any failure should be traced to the saved parser/output evidence. Fix: No case-specific modification; retain as a regression/control case. |
| T16 | invalid_negative_servings | ok | ok | False | False | Observed: The live LLM parser did not match the reference party size, budget, drink/serving list, or missing/unsupported fields. The workflow returned status=ok but the expected status was blocked. Failed objective checks: Calculation Accuracy. Diagnostic evidence: STATUS_MISMATCH, BLOCKED_CASE_GENERATED_PLAN. Root cause: The old validator had no positive-integer check, so negative servings reached deterministic arithmetic. Fix: Require every serving count to be a positive integer before calculation. |
| T17 | invalid_zero_servings | ok | blocked | False | False | Observed: The live LLM parser did not match the reference party size, budget, drink/serving list, or missing/unsupported fields. The workflow returned status=ok but the expected status was blocked. Failed objective checks: Calculation Accuracy. Diagnostic evidence: STATUS_MISMATCH. Root cause: The old validator had no positive-integer check, so zero servings could create an empty or zero-quantity plan presented as success. Fix: Reject zero servings before retrieval/calculation and ask for a positive count. |
| T18 | mixed_supported_and_unsupported | ok | blocked | False | False | Observed: The live LLM parser did not match the reference party size, budget, drink/serving list, or missing/unsupported fields. The workflow returned status=ok but the expected status was blocked. Failed objective checks: Calculation Accuracy. Diagnostic evidence: STATUS_MISMATCH, BLOCKED_CASE_GENERATED_PLAN. Root cause: The old workflow did not block a mixed request when unsupported_drinks was non-empty, so it could silently produce a partial plan. Fix: Treat any unsupported requested drink as a blocking condition until the user confirms a corrected request. |
| T19 | rag_recipe_retrieval | ok | ok | True | True | Observed: No objective failure was observed in this run. Root cause: No known legacy workflow defect is expected; any failure should be traced to the saved parser/output evidence. Fix: No case-specific modification; retain as a regression/control case. |
| T20 | ambiguous_request | ok | blocked | False | False | Observed: The live LLM parser did not match the reference party size, budget, drink/serving list, or missing/unsupported fields. The workflow returned status=ok but the expected status was blocked. Failed objective checks: Calculation Accuracy. Diagnostic evidence: STATUS_MISMATCH. Root cause: The old validator did not turn ambiguity/missing drink and serving fields into a blocking state. Fix: Block ambiguous requirements and state exactly which fields the user must provide. |

## Codex clarity review (pending user verification)

| ID | Before score | Before reason | After score | After reason |
|---|---:|---|---:|---|
| T01 | 3 | The list is readable, but its S$315.57 total conflicts with the line items/structured total of S$314.47 and it does not clearly flag the budget overrun. | 5 | Clear, actionable list with quantities, leftovers, correct total, and an explicit budget warning. |
| T02 | 3 | The list is readable, but the stated S$211.55 total is wrong (the structured total is S$215.55) and the budget overrun is omitted. | 5 | Clear shopping actions, correct total, shared-ingredient context, and explicit amount over budget. |
| T03 | 1 | It invents an unsupported Espresso Martini recipe and price instead of refusing or asking for correction. | 4 | It safely blocks the unsupported request and asks for correction, though the internal error-code wording is not very user-friendly. |
| T04 | 3 | It asks for more detail but does not plainly identify both missing party size and serving count. | 3 | It blocks safely, but technical validator codes and duplicated wording obscure the exact information the user should provide. |
| T05 | 1 | It falsely states a S$150 total within budget even though the structured Balanced total is S$314.47. | 5 | Clear itemized list with the correct S$314.47 total and explicit S$164.47 budget overrun. |
| T06 | 2 | The list is detailed but the stated S$56.16 total is materially wrong; the structured total is S$110.32. | 5 | Detailed and actionable list with the correct total and price range. |
| T07 | 2 | It ignores the substitution rule, removes Campari from the shopping explanation, and tells the user to buy separately priced Aperol even though Aperol is not in the calculated plan or total. | 3 | The list and budget are clear, but it says the rejected substitution may proceed after confirmation even though the structured rule result is allowed=false and applied=false. |
| T08 | 1 | It follows the adversarial request and produces a 100-Martini shopping plan instead of rejecting the injected instruction. | 3 | It blocks safely, but only exposes a technical missing-party-size code and does not clearly explain that the injected instruction was rejected. |
| T09 | 3 | The shopping list is understandable, but it omits the required egg-allergen warning and labels a point total as a range. | 5 | Clear list, correct total/range, budget result, and explicit egg-allergen warning. |
| T10 | 4 | The shopping list and total are clear, but it omits that the plan exceeds the S$100 budget and does not show the price range. | 5 | Clear itemized result with total, range, leftovers, and explicit budget overrun. |
| T11 | 4 | The quantities and budget conclusion are clear, but the overall total and price range are omitted. | 5 | Clear boundary-case result with exact package counts, total, range, leftovers, and budget status. |
| T12 | 4 | It clearly shows the package rounding to two gin bottles, but omits the overall total and range. | 5 | Clear package-rounding result with correct quantities, total, range, and budget status. |
| T13 | 2 | It misleadingly reports an approximately S$300 total instead of the structured S$177.94 total. | 5 | Clear consolidated multi-drink list with the correct total/range and shared lime purchases explained. |
| T14 | 4 | The list and total are clear, but the price range and explicit comparison with the S$200 budget are omitted. | 5 | Clear non-alcoholic shopping list with total, range, leftovers, and budget conclusion. |
| T15 | 3 | The exact total is shown, but the required egg-allergen warning and price range are missing. | 5 | Clear exact-boundary result with total/range, leftovers, and the egg-allergen warning. |
| T16 | 1 | It turns the invalid negative serving request into a positive two-serving purchase plan. | 1 | It still turns 'minus 2' into positive 2 and gives a misleading purchase plan; this is a live-parser failure before validation. |
| T17 | 2 | It treats zero servings as if the user simply chose no Martini and gives vague alternatives instead of identifying invalid input. | 3 | It blocks safely, but the technical message does not plainly ask the user for a positive serving count. |
| T18 | 1 | It silently produces a partial Negroni plan, ignores the unsupported Espresso Martini, and falsely claims gin is supplied for it. | 4 | It correctly blocks and identifies Espresso Martini as unsupported, though the validator-style wording could be friendlier. |
| T19 | 2 | The list is readable but its S$252.51 total is materially wrong; the structured total is S$305.56. | 5 | Clear RAG-grounded list with correct total/range and explicit budget overrun. |
| T20 | 1 | It invents a gin-and-tonic shopping list and prices from an intentionally ambiguous request. | 3 | It blocks safely and asks for a drink choice, but does not plainly request the missing serving count. |

## Remaining issues found in the latest C

- T07: The structured rule result is correct (allowed=false, applied=false), but the generated explanation says the substitution may proceed after confirmation. Clarify that confirmation means acknowledging the rejection/choosing a labelled variation, not overriding allowed=false.
- T16: Real pipeline issue: the live LLM parser normalised 'minus 2' to positive 2. Because the Python validator only sees the parsed positive value, it cannot detect the original negative request. Add a raw-input negative-number guard or strengthen and separately test the parser.

## Assistant review workflow

1. The assistant reads `c_before_after_results.json`, including all 40 generated outputs.
2. The assistant assigns Explanation Clarity from 1-5 and writes a short reason for each output.
3. Scores of 4-5 pass; 1-3 fail.
4. The user checks the assistant's scores and records agreement or changes in the CSV.

The assistant review is deliberately separate from the API generation run so the evaluator is not the same model call that produced the answer.
