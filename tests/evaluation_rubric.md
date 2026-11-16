
# AI Mock Interviewer - Evaluation Rubric

## 1. Objective
Evaluate the baseline and improved prompt versions using the same 10 test cases.

## 2. Evaluation Method
Each test is evaluated against predefined expected behaviour.

A test receives:
- PASS: The output satisfies all essential expected criteria.
- FAIL: The output misses or violates at least one essential criterion.

Partial correctness may be mentioned in the observations, but the final result is recorded as Pass or Fail.

## 3. Evaluation Criteria

| Criterion | What is evaluated |
|---|---|
| Question Relevance | Is the question relevant to the selected role and interview type? |
| Question Structure | Does the AI ask only one question at a time? |
| Answer Evaluation | Does it correctly identify strengths and weaknesses? |
| Scoring Quality | Is the score justified and consistent with the answer? |
| Feedback Quality | Is feedback specific, constructive and understandable? |
| Adaptability | Does it use previous answers to generate relevant follow-ups? |
| Reliability | Does it avoid inventing student information? |

## 4. Test-Specific Pass Conditions

| Test | Essential pass condition |
|---|---|
| TC01 | Generates a beginner-level Python question |
| TC02 | Generates a relevant AI/ML question |
| TC03 | Generates an appropriate HR question |
| TC04 | Asks exactly one question |
| TC05 | Identifies missing details in the incomplete answer |
| TC06 | Accepts the technically valid alternative explanation |
| TC07 | Recognises the irrelevant answer and evaluates it fairly |
| TC08 | Does not invent student experience or achievements |
| TC09 | Uses the previous answer to ask a relevant follow-up |
| TC10 | Gives comparable scores and reasoning for identical answers |

## 5. Consistency Rules

1. Use identical test inputs for V1, V2 and V3.
2. Keep the interview context and model settings consistent.
3. Record the actual output from every run.
4. Do not change expected results after seeing the output.
5. Repeat TC10 to examine scoring consistency.
6. Record failures honestly.

## 6. Performance Calculation

Pass Rate = (Number of Passed Tests / 10) x 100

Compare the pass rates of all three prompt versions.

## 7. Limitations

AI-generated evaluations may vary between runs.
A passing result does not guarantee perfect interview feedback.
Human review is necessary for subjective evaluations.
