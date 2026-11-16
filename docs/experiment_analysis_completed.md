# Prompt Experiment Analysis — AI Mock Interviewer

## 1. Objective
The experiment compares three prompt versions (V1, V2 and V3) for an AI mock interviewer. Each version was evaluated against the same 10 test cases covering question relevance, interview behaviour, answer evaluation, alternative explanations, irrelevant answers, fabricated candidate experience, contextual follow-ups and scoring consistency.

## 2. Prompt iteration summary

- **V1 — Baseline:** Establishes the interviewer role and the basic question, evaluation and feedback workflow.
- **V2 — Structured evaluation:** Adds role/interview/experience context, explicit technical scoring weights, criterion-wise feedback and HR-specific evaluation criteria.
- **V3 — Adaptive interview:** Adds multi-turn context retention, difficulty adaptation, contextual follow-ups, fairness/consistency rules and a final interview summary.

## 3. Quantitative results

| Prompt version | Passed | Failed | Pass rate |
|---|---:|---:|---:|
| V1 | 8/10 | 2/10 | 80% |
| V2 | 9/10 | 1/10 | 90% |
| V3 | 8/10 | 2/10 | 80% |

V2 achieved the highest observed pass rate at **90%**, improving by 10 percentage points over V1. V3 achieved 80%, matching V1 and falling 10 percentage points below V2. These results are based on the recorded PASS/FAIL labels in `evaluation_results.csv`.

## 4. Test observations

- **TC08 (avoid invented experience) failed in all three versions.** V1 generated fictional projects and achievements; V2 suggested a lab assistant role and project experience; V3 suggested projects and performance metrics. The no-fabrication instruction alone did not reliably prevent invented details in suggested answers.
- **TC01 (basic Python question) passed only in V2.** V1 and V3 produced an array-versus-linked-list question that was programming-related but not specifically Python-related.
- **TC09 (contextual follow-up) passed in all versions.** The recorded follow-ups connected to the earlier discussion of overfitting.
- **TC10 (scoring consistency) passed in all versions.** The recorded repeated runs had matching numerical scores within each version.
- V2's TC07 observation notes a minor inconsistency in clarity scoring, despite the test being labelled PASS.

## 5. Interpretation

V2 performed best on the current test set. Its explicit scoring weights and required feedback structure appear to have improved evaluation transparency and helped the system meet more of the recorded expected behaviours. V3 introduced valuable adaptive-interview capabilities, but the current evaluation results do not show a higher overall pass rate. In particular, adding fairness instructions did not resolve the fabricated-experience issue.

The results suggest that prompt complexity alone does not guarantee better test performance. The most important remaining weakness is the generation of candidate-specific details that were never supplied by the student.

## 6. Recommended next iteration

1. Explicitly prohibit adding any candidate-specific role, project, achievement, metric, qualification or personal detail that is absent from the student's answer or interview context.
2. When information is missing, use clearly marked placeholders (for example, `[add your actual project]`) or ask the student for the real details instead of inventing them.
3. Add a targeted regression test for fabricated experience and retain TC01 to ensure questions match the selected role and topic.
4. Re-run all 10 test cases after any prompt change and update the CSV using actual outputs. Do not change PASS/FAIL labels unless the expected behaviour and observed output justify the change.

## 7. Limitations

The analysis reflects the 30 recorded evaluation rows and the observations entered in `evaluation_results.csv`. It does not establish statistical significance, and the scores should not be generalized beyond these test cases. The raw model outputs should be retained as supporting evidence. No unrecorded experiment settings or model parameters have been assumed.

## 8. Conclusion

Based on the current recorded tests, **V2 is the best-performing prompt version at 90%**. V3 offers the most complete adaptive interview design, but it requires further refinement and regression testing before it can be considered the strongest version overall. The recurring TC08 failure is the highest-priority issue to address.
