import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL") or os.getenv("MODEL")

st.set_page_config(
    page_title="AI Mock Interviewer",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Mock Interviewer")
st.caption("Practice interviews. Improve your answers. Build confidence.")

if not API_KEY:
    st.error("GROQ_API_KEY is missing from your .env file.")
    st.stop()

if not MODEL:
    st.error(
        "Model name not found. Add GROQ_MODEL=your_model_name "
        "to your .env file, using the model name you configured."
    )
    st.stop()

client = Groq(api_key=API_KEY)


def ask_ai(messages):
    """Send messages to Groq and return the model response."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.5,
        max_tokens=1200
    )
    return response.choices[0].message.content.strip()


# Initialize interview state
if "started" not in st.session_state:
    st.session_state.started = False

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "feedback" not in st.session_state:
    st.session_state.feedback = []

if "current_question" not in st.session_state:
    st.session_state.current_question = ""

if "interview_config" not in st.session_state:
    st.session_state.interview_config = {}


# Sidebar: interview configuration
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

    start_button = st.button(
        "Start Interview",
        type="primary",
        use_container_width=True
    )

    reset_button = st.button(
        "Reset Interview",
        use_container_width=True
    )


if reset_button:
    for key in [
        "started",
        "questions",
        "answers",
        "feedback",
        "current_question",
        "interview_config"
    ]:
        st.session_state.pop(key, None)

    st.rerun()


# Start a new interview
if start_button:
    st.session_state.started = False
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.feedback = []
    st.session_state.current_question = ""

    st.session_state.interview_config = {
        "type": interview_type,
        "role": role,
        "experience": experience,
        "total": total_questions
    }

    with st.spinner("Preparing your first interview question..."):
        try:
            question = ask_ai([
                {
                    "role": "system",
                    "content": (
                        "You are a professional mock interviewer. "
                        "Ask one clear interview question at a time. "
                        "Do not provide the answer or evaluation yet. "
                        "Avoid asking multiple questions in one turn."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Interview type: {interview_type}\n"
                        f"Target role: {role}\n"
                        f"Experience level: {experience}\n"
                        "Generate the first appropriate interview question."
                    )
                }
            ])

            st.session_state.current_question = question
            st.session_state.started = True
            st.rerun()

        except Exception as e:
            st.error(
                f"Could not connect to the AI service: {e}"
            )


# Interview interface
if st.session_state.started:
    config = st.session_state.interview_config
    completed = len(st.session_state.answers)
    total = config["total"]

    st.subheader(
        f"{config['type']} Interview — {config['role']}"
    )

    st.progress(completed / total)

    st.write(
        f"**Question {completed + 1} of {total}**"
    )

    st.info(st.session_state.current_question)

    with st.form(
        key=f"answer_form_{completed}"
    ):
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
                    evaluation = ask_ai([
                        {
                            "role": "system",
                            "content": """
You are a fair and constructive interview evaluator.

Evaluate the candidate's answer based on correctness,
relevance, clarity, and completeness.

Accept valid alternative explanations.
Do not invent facts about the candidate.

Return these sections:

SCORE: Give a score from 0 to 10.

STRENGTHS: Explain what was done well.

IMPROVEMENTS: Explain what is missing or incorrect.

SUGGESTED ANSWER: Give an example of a stronger answer.

Keep the feedback specific and constructive.
"""
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Interview type: {config['type']}\n"
                                f"Target role: {config['role']}\n"
                                f"Experience: {config['experience']}\n"
                                f"Question: "
                                f"{st.session_state.current_question}\n"
                                f"Candidate's answer: {answer}"
                            )
                        }
                    ])

                    st.session_state.answers.append({
                        "question": (
                            st.session_state.current_question
                        ),
                        "answer": answer
                    })

                    st.session_state.feedback.append(evaluation)

                    if len(st.session_state.answers) < total:
                        with st.spinner(
                            "Preparing your next question..."
                        ):
                            next_question = ask_ai([
                                {
                                    "role": "system",
                                    "content": (
                                        "You are a professional interviewer. "
                                        "Ask exactly one new interview "
                                        "question. Adapt its difficulty "
                                        "to the candidate's previous "
                                        "answer. Do not give the answer."
                                    )
                                },
                                {
                                    "role": "user",
                                    "content": (
                                        f"Interview type: {config['type']}\n"
                                        f"Target role: {config['role']}\n"
                                        f"Experience level: "
                                        f"{config['experience']}\n"
                                        f"Previous question: "
                                        f"{st.session_state.current_question}\n"
                                        f"Previous answer: {answer}\n"
                                        f"Previous feedback: {evaluation}\n"
                                        "Ask the next relevant question. "
                                        "Avoid repeating the previous one."
                                    )
                                }
                            ])

                            st.session_state.current_question = (
                                next_question
                            )

                    else:
                        st.session_state.started = False

                    st.rerun()

                except Exception as e:
                    st.error(
                        f"Something went wrong: {e}"
                    )


# Display completed interview results
if (
    not st.session_state.started
    and len(st.session_state.answers) > 0
):
    if (
        len(st.session_state.answers)
        == st.session_state.interview_config.get("total", 0)
    ):
        st.success("🎉 Interview completed!")

    st.header("📊 Interview Feedback")

    for i, item in enumerate(st.session_state.answers):
        with st.expander(
            f"Question {i + 1}: {item['question']}"
        ):
            st.write("**Your Answer**")
            st.write(item["answer"])

            st.write("**AI Evaluation**")
            st.markdown(st.session_state.feedback[i])

    st.info(
        "Review your feedback to identify areas for improvement. "
        "AI-generated scores are estimates, not objective measures "
        "of interview performance."
    )

elif not st.session_state.started:
    st.markdown(
        """
        ### How it works

        1. Select your interview type and target role.
        2. Start your interview.
        3. Answer each question.
        4. Receive AI-generated feedback.
        5. Review your results and improve.

        **Ready?** Configure your interview in the sidebar and
        click **Start Interview**.
        """
    )