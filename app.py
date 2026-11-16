
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from groq import Groq


# ============================================================
# 1. CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent

load_dotenv(ROOT / ".env")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL") or os.getenv("MODEL")

PROMPT_FILES = {
    "V1": ROOT / "prompts" / "baseline_v1.txt",
    "V2": ROOT / "prompts" / "improved_v2.txt",
    "V3": ROOT / "prompts" / "improved_v3.txt",
}

st.set_page_config(
    page_title="AI Mock Interviewer",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# 2. API VALIDATION
# ============================================================

st.title("🎯 AI Mock Interviewer")
st.caption("Practice interviews. Improve your answers. Build confidence.")

if not API_KEY:
    st.error("GROQ_API_KEY is missing from your .env file.")
    st.stop()

if not MODEL:
    st.error("GROQ_MODEL is missing from your .env file.")
    st.stop()

client = Groq(api_key=API_KEY)


# ============================================================
# 3. PROMPT MANAGEMENT
# ============================================================

def load_prompt(version):
    """Load the selected prompt from the prompts directory."""

    if version not in PROMPT_FILES:
        raise ValueError(f"Invalid prompt version: {version}")

    prompt_path = PROMPT_FILES[version]

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_path}"
        )

    return prompt_path.read_text(encoding="utf-8")


def build_system_prompt(version, stage):
    """
    Combine the selected experimental prompt with
    instructions specific to the current interview stage.
    """

    base_prompt = load_prompt(version)

    stage_instructions = {

        "question": """
INTERVIEW STAGE: INITIAL QUESTION GENERATION

Your task in this stage is ONLY to generate the first
interview question.

Instructions:
1. Generate exactly ONE interview question.
2. Consider the interview type, target role and experience level.
3. Make the question relevant to the selected role.
4. Match its difficulty to the candidate's experience.
5. Do not evaluate an answer.
6. Do not provide a suggested answer.
7. Do not generate multiple questions.

Return only the interview question.
""",

        "evaluation": """
INTERVIEW STAGE: ANSWER EVALUATION

Your task in this stage is ONLY to evaluate the
candidate's submitted answer.

Instructions:
1. Evaluate correctness, relevance, clarity and completeness.
2. Accept valid alternative explanations.
3. Do not penalize candidates for using different wording.
4. Never invent qualifications, projects or experience.
5. Do not assume information that the candidate has not provided.
6. Give a score out of 10 with a clear justification.
7. Provide constructive and specific feedback.

Return the following sections:

SCORE: Score out of 10.

JUSTIFICATION: Explain the score.

STRENGTHS: Explain what the candidate did well.

IMPROVEMENTS: Explain missing or incorrect concepts.

SUGGESTED ANSWER: Provide an example of a stronger answer.

Do not ask another interview question in this stage.
""",

        "next_question": """
INTERVIEW STAGE: NEXT QUESTION GENERATION

Your task in this stage is ONLY to generate the next
interview question.

Instructions:
1. Ask exactly ONE new interview question.
2. Consider the previous question and candidate's answer.
3. Use previous feedback to guide the next question.
4. Adapt difficulty to the candidate's demonstrated understanding.
5. Maintain relevance to the selected interview type and role.
6. Avoid repeating previous questions.
7. Do not evaluate the previous answer again.
8. Do not provide the answer.

Return only the next interview question.
"""
    }

    if stage not in stage_instructions:
        raise ValueError(f"Invalid interview stage: {stage}")

    return (
        base_prompt
        + "\n\nIMPORTANT: The following stage-specific "
        "instructions take priority over conflicting "
        "instructions above.\n\n"
        + stage_instructions[stage]
    )


# ============================================================
# 4. GROQ API FUNCTION
# ============================================================

def ask_ai(messages):
    """Send conversation messages to Groq."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.5,
        max_tokens=1200
    )

    return response.choices[0].message.content.strip()


# ============================================================
# 5. SESSION STATE INITIALIZATION
# ============================================================

DEFAULTS = {
    "started": False,
    "questions": [],
    "answers": [],
    "feedback": [],
    "current_question": "",
    "interview_config": {}
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, list) else value


# ============================================================
# 6. SIDEBAR - INTERVIEW CONFIGURATION
# ============================================================

with st.sidebar:

    st.header("Interview Setup")

    interview_type = st.selectbox(
        "Interview Type",
        ["Technical", "HR"]
    )

    role = st.selectbox(
        "Target Role",
        [
            "Software Development Intern",
            "AI/ML Engineer Intern",
            "Data Analyst Intern",
            "Web Developer Intern"
        ]
    )

    experience = st.selectbox(
        "Experience Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    total_questions = st.slider(
        "Number of Questions",
        min_value=3,
        max_value=10,
        value=5
    )

    prompt_version = st.selectbox(
        "AI Interviewer Version",
        ["V1", "V2", "V3"],
        index=1
    )

    st.caption(
        "V1: Baseline | V2: Rubric-based | V3: Adaptive"
    )

    start_button = st.button(
        "Start Interview",
        type="primary",
        use_container_width=True
    )

    reset_button = st.button(
        "Reset Interview",
        use_container_width=True
    )


# ============================================================
# 7. RESET INTERVIEW
# ============================================================

if reset_button:

    for key, value in DEFAULTS.items():
        st.session_state[key] = (
            value.copy() if isinstance(value, list) else value
        )

    st.rerun()


# ============================================================
# 8. START INTERVIEW
# ============================================================

if start_button:

    # Verify prompt file before starting.
    try:
        load_prompt(prompt_version)

    except Exception as error:
        st.error(f"Prompt loading failed: {error}")
        st.stop()

    st.session_state.started = False
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.feedback = []
    st.session_state.current_question = ""

    st.session_state.interview_config = {
        "type": interview_type,
        "role": role,
        "experience": experience,
        "total": total_questions,
        "prompt_version": prompt_version
    }

    with st.spinner("Preparing your first interview question..."):

        try:

            question = ask_ai([
                {
                    "role": "system",
                    "content": build_system_prompt(
                        prompt_version,
                        "question"
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Interview type: {interview_type}\n"
                        f"Target role: {role}\n"
                        f"Experience level: {experience}\n"
                        "Generate the first interview question."
                    )
                }
            ])

            st.session_state.current_question = question
            st.session_state.questions.append(question)
            st.session_state.started = True

            st.rerun()

        except Exception as error:
            st.error(f"Could not start interview: {error}")


# ============================================================
# 9. INTERVIEW INTERFACE
# ============================================================

if st.session_state.started:

    config = st.session_state.interview_config

    completed = len(st.session_state.answers)
    total = config["total"]

    st.subheader(
        f"{config['type']} Interview — {config['role']}"
    )

    st.caption(
        f"Prompt Version: {config['prompt_version']}"
    )

    st.progress(completed / total)

    st.write(f"**Question {completed + 1} of {total}**")

    st.info(st.session_state.current_question)

    with st.form(key=f"answer_form_{completed}"):

        answer = st.text_area(
            "Your Answer",
            placeholder="Type your answer here...",
            height=180
        )

        submitted = st.form_submit_button(
            "Submit Answer",
            type="primary"
        )

    if submitted:

        if not answer.strip():

            st.warning("Please enter an answer first.")

        else:

            with st.spinner("Evaluating your answer..."):

                try:

                    # ----------------------------------------
                    # 9A. EVALUATE CANDIDATE ANSWER
                    # ----------------------------------------

                    evaluation = ask_ai([
                        {
                            "role": "system",
                            "content": build_system_prompt(
                                config["prompt_version"],
                                "evaluation"
                            )
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Interview type: {config['type']}\n"
                                f"Target role: {config['role']}\n"
                                f"Experience: {config['experience']}\n"
                                f"Question: {st.session_state.current_question}\n"
                                f"Candidate's answer: {answer}"
                            )
                        }
                    ])

                    # Generate next question before saving
                    # so a failed API request doesn't duplicate
                    # the submitted answer on retry.

                    next_question = None

                    # ----------------------------------------
                    # 9B. GENERATE NEXT QUESTION
                    # ----------------------------------------

                    if completed + 1 < total:

                        with st.spinner(
                            "Preparing your next question..."
                        ):

                            next_question = ask_ai([
                                {
                                    "role": "system",
                                    "content": build_system_prompt(
                                        config["prompt_version"],
                                        "next_question"
                                    )
                                },
                                {
                                    "role": "user",
                                    "content": (
                                        f"Interview type: {config['type']}\n"
                                        f"Target role: {config['role']}\n"
                                        f"Experience: {config['experience']}\n"
                                        f"Previous question: "
                                        f"{st.session_state.current_question}\n"
                                        f"Previous answer: {answer}\n"
                                        f"Previous feedback: {evaluation}\n"
                                        "Generate the next relevant question."
                                    )
                                }
                            ])

                    # ----------------------------------------
                    # 9C. SAVE INTERVIEW DATA
                    # ----------------------------------------

                    st.session_state.answers.append({
                        "question": st.session_state.current_question,
                        "answer": answer
                    })

                    st.session_state.feedback.append(evaluation)

                    if next_question:

                        st.session_state.current_question = next_question

                        st.session_state.questions.append(
                            next_question
                        )

                    else:

                        st.session_state.started = False

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Something went wrong: {error}"
                    )


# ============================================================
# 10. DISPLAY INTERVIEW RESULTS
# ============================================================

if (
    not st.session_state.started
    and len(st.session_state.answers) > 0
):

    config = st.session_state.interview_config

    if len(st.session_state.answers) == config.get("total", 0):

        st.success("🎉 Interview completed!")

    st.header("📊 Interview Feedback")

    st.write(
        f"**Interview Type:** {config.get('type', '')}"
    )

    st.write(
        f"**Target Role:** {config.get('role', '')}"
    )

    st.write(
        f"**Prompt Version:** {config.get('prompt_version', '')}"
    )

    for i, item in enumerate(st.session_state.answers):

        with st.expander(
            f"Question {i + 1}: {item['question']}"
        ):

            st.write("**Your Answer**")
            st.write(item["answer"])

            st.write("**AI Evaluation**")

            st.markdown(
                st.session_state.feedback[i]
            )

    st.info(
        "Review your feedback to identify areas for improvement. "
        "AI-generated scores are estimates, not objective measures "
        "of interview performance."
    )


# ============================================================
# 11. HOME PAGE
# ============================================================

elif not st.session_state.started:

    st.markdown(
        """
        ### How it works

        1. Select your interview type and target role.
        2. Choose your preferred AI prompt version.
        3. Start your interview.
        4. Answer each question.
        5. Receive AI-generated feedback.
        6. Review your results and improve.

        **Ready?** Configure your interview in the sidebar
        and click **Start Interview**.
        """
    )
