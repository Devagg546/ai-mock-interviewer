
import os
import csv
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
PROMPT_DIR = ROOT / "prompts"
OUTPUT_FILE = ROOT / "evaluation" / "raw_outputs.csv"

load_dotenv(ROOT / ".env")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL") or os.getenv("MODEL")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

if not MODEL:
    raise ValueError("GROQ_MODEL or MODEL not found in .env")

client = Groq(api_key=API_KEY)


# --------------------------------------------------
# 2. PROMPT FILES
# --------------------------------------------------

PROMPTS = {
    "V1": PROMPT_DIR / "baseline_v1.txt",
    "V2": PROMPT_DIR / "improved_v2.txt",
    "V3": PROMPT_DIR / "improved_v3.txt",
}


# --------------------------------------------------
# 3. STANDARDIZED TEST CASES
# --------------------------------------------------

TESTS = [
    {
        "id": "TC01",
        "scenario": "Basic Python interview",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Interview type: Technical\n"
                    "Role: Software Development Intern\n"
                    "Level: Beginner\n"
                    "Start the interview and ask the first question."
                )
            }
        ],
    },
    {
        "id": "TC02",
        "scenario": "AI/ML role relevance",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Interview type: Technical\n"
                    "Role: AI/ML Engineer Intern\n"
                    "Level: Intermediate\n"
                    "Start the interview and ask the first question."
                )
            }
        ],
    },
    {
        "id": "TC03",
        "scenario": "HR interview",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Interview type: HR\n"
                    "Role: Software Development Intern\n"
                    "Level: Beginner\n"
                    "Start the interview and ask the first question."
                )
            }
        ],
    },
    {
        "id": "TC04",
        "scenario": "One question at a time",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Start a technical interview for a beginner "
                    "Software Development Intern. Ask your first question."
                )
            }
        ],
    },
    {
        "id": "TC05",
        "scenario": "Incomplete answer",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Interview type: Technical\n"
                    "Question: What is machine learning?\n"
                    "Student answer: It is when computers learn.\n"
                    "Evaluate this answer."
                )
            }
        ],
    },
    {
        "id": "TC06",
        "scenario": "Valid alternative explanation",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Interview type: Technical\n"
                    "Question: What is a Python list?\n"
                    "Student answer: A list is an ordered collection "
                    "that can store multiple values and can be modified.\n"
                    "Evaluate this answer."
                )
            }
        ],
    },
    {
        "id": "TC07",
        "scenario": "Irrelevant answer",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Interview type: Technical\n"
                    "Question: Explain supervised learning.\n"
                    "Student answer: My favourite subject is cricket.\n"
                    "Evaluate this answer fairly."
                )
            }
        ],
    },
    {
        "id": "TC08",
        "scenario": "No previous work experience",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Interview type: HR\n"
                    "Role: Software Development Intern\n"
                    "Question: Tell me about your previous work experience.\n"
                    "Student answer: I do not have formal work experience yet.\n"
                    "Evaluate this answer without assuming any qualifications."
                )
            }
        ],
    },
    {
        "id": "TC09",
        "scenario": "Contextual follow-up",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Interview type: Technical\n"
                    "Previous question: What is overfitting?\n"
                    "Student answer: A model performs well on training "
                    "data but poorly on unseen data.\n"
                    "Evaluate the answer briefly and ask one relevant "
                    "follow-up question."
                )
            }
        ],
    },
    {
        "id": "TC10",
        "scenario": "Scoring consistency",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Interview type: Technical\n"
                    "Question: What is a Python list?\n"
                    "Student answer: A list is an ordered, mutable "
                    "collection that can store multiple elements.\n"
                    "Evaluate this answer and give a score out of 10."
                )
            }
        ],
    },
]


# --------------------------------------------------
# 4. CALL THE MODEL
# --------------------------------------------------

def get_response(system_prompt, user_messages):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            *user_messages
        ],
        temperature=0,
        max_tokens=1000,
    )

    return response.choices[0].message.content.strip()


# --------------------------------------------------
# 5. SAVE RESULTS WITHOUT OVERWRITING OLD RUNS
# --------------------------------------------------

def save_result(row):

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "test_id",
        "prompt_version",
        "scenario",
        "output_1",
        "output_2",
    ]

    records = {}

    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for old_row in reader:
                key = (
                    old_row["test_id"],
                    old_row["prompt_version"]
                )
                records[key] = old_row

    key = (row["test_id"], row["prompt_version"])
    records[key] = row

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records.values())


# --------------------------------------------------
# 6. RUN THE EXPERIMENT
# --------------------------------------------------

if len(sys.argv) != 2:
    print("Usage: python evaluation/run_evaluation.py v1")
    print("Choose v1, v2, v3 or all.")
    sys.exit(1)

selection = sys.argv[1].upper()

if selection == "ALL":
    versions = ["V1", "V2", "V3"]
elif selection in PROMPTS:
    versions = [selection]
else:
    raise ValueError("Choose v1, v2, v3 or all.")


for version in versions:

    prompt_path = PROMPTS[version]

    if not prompt_path.exists():
        raise FileNotFoundError(prompt_path)

    system_prompt = prompt_path.read_text(encoding="utf-8")

    print(f"\nStarting {version} experiment")

    for test in TESTS:

        print(
            f"Running {test['id']}: {test['scenario']}"
        )

        try:
            output_1 = get_response(
                system_prompt,
                test["messages"]
            )

            output_2 = ""

            # Repeat TC10 to examine consistency.
            if test["id"] == "TC10":
                output_2 = get_response(
                    system_prompt,
                    test["messages"]
                )

            save_result({
                "test_id": test["id"],
                "prompt_version": version,
                "scenario": test["scenario"],
                "output_1": output_1,
                "output_2": output_2,
            })

            print("Saved successfully.")

        except Exception as error:
            print(f"ERROR in {test['id']}: {error}")

print("\nExperiment run completed.")
print(f"Raw outputs saved to: {OUTPUT_FILE}")
