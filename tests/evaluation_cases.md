
# AI Mock Interviewer - Evaluation Dataset

## Objective
Evaluate the performance of three prompt versions:
- V1: Baseline Interviewer
- V2: Rubric-Based Interviewer
- V3: Adaptive Interviewer

## Test Cases

### TC01 - Basic Technical Question
Input: Conduct a beginner-level Python interview for a Software Development Intern.
Expected: A relevant beginner-level Python question.
Category: Normal

### TC02 - Role Relevance
Input: Conduct an AI/ML Engineer interview for an intermediate candidate.
Expected: A question relevant to machine learning or AI.
Category: Normal

### TC03 - HR Interview
Input: Conduct an HR interview for an internship candidate.
Expected: A relevant behavioural question.
Category: Normal

### TC04 - One Question at a Time
Input: Start a technical interview.
Expected: Exactly one interview question, not multiple questions.
Category: Normal

### TC05 - Incomplete Answer
Input: Question: What is machine learning?
Answer: It is when computers learn.
Expected: Fair evaluation that identifies missing details.
Category: Edge Case

### TC06 - Valid Alternative Explanation
Input: Question: What is a Python list?
Answer: A list is an ordered collection that can store multiple values and can be modified.
Expected: Accept the correct explanation without demanding textbook wording.
Category: Edge Case

### TC07 - Irrelevant Answer
Input: Question: Explain supervised learning.
Answer: My favourite subject is cricket.
Expected: Identify that the answer is irrelevant and score accordingly.
Category: Edge Case

### TC08 - Missing Student Experience
Input: Conduct an HR interview without any supplied work experience.
Expected: Do not invent qualifications, achievements, or experience.
Category: Edge Case

### TC09 - Follow-up Relevance
Input: Previous question: What is overfitting?
Answer: A model performs well on training data but poorly on unseen data.
Expected: Ask a relevant follow-up about causes or prevention of overfitting.
Category: Normal

### TC10 - Consistent Evaluation
Input: Evaluate the same technically correct answer twice using identical interview context.
Expected: Similar scores and consistent reasoning.
Category: Consistency Test

## Evaluation Record

For each prompt version, record:
- Actual output
- Expected output comparison
- Pass or Fail
- Reason for the result

Do not enter results until the tests have actually been run.
