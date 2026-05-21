from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Example MCQ
question = """
Which of the following best explains why lipids,
despite having molecular weights less than 1000 Da,
are classified under the acid insoluble fraction?

A) Lipids form large polymers
B) Lipids aggregate into insoluble complexes
C) Lipids contain nitrogen bases
D) Lipids are highly water soluble

Correct Answer: B
"""

# Student Response
student_answer = "A"

# Educational Context
context = """
Lipids are water insoluble and occur in the
acid insoluble fraction despite low molecular weight.
They aggregate into membrane and structural complexes.
"""

# Evaluation Prompt
prompt = f"""
You are an expert NEET Biology tutor.

Evaluate the student's answer.

Rules:
1. Tell whether answer is correct or incorrect.
2. Explain WHY.
3. Explain the biological concept clearly.
4. Identify misconception if answer is wrong.
5. Give a short remediation explanation.
6. Encourage conceptual understanding.

Question:
{question}

Student Answer:
{student_answer}

Educational Context:
{context}
"""

# Generate Evaluation
response = client.chat.completions.create(
    model="gpt-4.1-mini",

    messages=[
        {
            "role": "system",
            "content": (
                "You are an expert NEET Biology evaluator."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ],

    temperature=0.3
)

evaluation = response.choices[0].message.content

print("\n--- ANSWER EVALUATION ---\n")

print(evaluation)