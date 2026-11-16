
# Prompt Engineering Experiment Analysis

## 1. Objective

The objective of this experiment was to compare three versions of prompts used in an AI Mock Interviewer application.

The experiment evaluates whether structured feedback and adaptive interview instructions improve the quality, relevance, and consistency of AI-generated interview responses.

## 2. Experimental Setup

- AI Model: Groq-hosted language model
- Prompt Versions: V1, V2 and V3
- Test Cases: 10 standardized scenarios
- Temperature: 0
- Maximum Output Tokens: 1000
- Evaluation Method: Manual assessment using predefined test criteria
- Consistency Test: TC10 was executed twice for each prompt version.

All three prompt versions were tested using the same test scenarios.

## 3. Prompt Versions

### V1 – Baseline Prompt

The baseline prompt establishes basic mock interview behaviour.

It instructs the AI to:
- Ask one interview question at a time.
- Evaluate student answers.
- Provide scores out of 10.
- Identify strengths and missing points.
- Suggest improved answers.
- Ask relevant follow-up questions.

### V2 – Rubric-Based Prompt

V2 introduces more structured evaluation.

Its improvements include:
- Separate technical and HR evaluation criteria.
- Criterion-wise scoring.
- More structured feedback.
- Acceptance of valid alternative explanations.

### V3 – Adaptive Interview Prompt

V3 introduces more advanced interview behaviour.

Its features include:
- Multi-turn interview context.
- Adaptive question difficulty.
- Contextual follow-up questions.
- Avoidance of unnecessary question repetition.
- Separate evaluation criteria for technical and HR interviews.

## 4. Experimental Results

| Prompt Version | Passed | Failed | Pass Rate |
|---|---:|---:|---:|
| V1 | 8 | 2 | 80% |
| V2 | 9 | 1 | 90% |
| V3 | 8 | 2 | 80% |

V2 achieved the highest observed pass rate of 90%.

## 5. Failure Analysis

### TC01 – Question Relevance

V1 and V3 generated general programming questions instead of questions specifically focused on Python.

V2 performed better by generating a Python-related question.

This indicates that more explicit instructions about the selected programming language may improve question relevance.

### TC08 – Fabricated Student Experience

All three prompt versions failed this test.

When the student stated that they had no formal work experience, the AI generated fictional projects, achievements and professional experiences.

This highlights a limitation in the prompts' ability to prevent unsupported personal claims.

## 6. Key Observations

1. V2 achieved the highest pass rate in the experiment.
2. Criterion-wise scoring improved the structure of evaluation feedback.
3. V3 introduced adaptive interview behaviour but did not outperform V2 overall.
4. Fabricated personal experiences remained a weakness across all three versions.
5. Repeated TC10 runs produced identical numerical scores for each version.

## 7. Limitations

- The experiment used only 10 test scenarios.
- Only one model configuration was evaluated.
- Manual assessment may introduce evaluator subjectivity.
- Repeated scoring was examined using only one test scenario.
- A successful result on these test cases does not guarantee general performance across all interview situations.

## 8. Conclusion

The experiment demonstrates that structured prompt instructions can improve observed interview evaluation performance.

V2 achieved the highest pass rate of 90%, while V1 and V3 each achieved 80%.

However, all three prompt versions struggled to prevent fabricated student experiences.

Future improvements should focus on stronger factual grounding, safer answer suggestions, and more reliable context handling.

The experiment also demonstrates that increasing prompt complexity does not necessarily lead to improved performance.
