import json
import re
from ollama_service import generate

class QuizAgent:
    def generate(self, topic):
        prompt = f"""
Create exactly 5 multiple-choice questions about: {topic}

Return ONLY valid JSON in this format:
[
  {{
    "question": "Question text",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Do not add markdown or explanation outside JSON.
"""
        raw = generate(prompt)

        match = re.search(r"\[[\s\S]*\]", raw)
        if not match:
            return {"error": "Could not generate quiz. Please try again."}

        try:
            data = json.loads(match.group(0))
            return {"topic": topic, "questions": data}
        except json.JSONDecodeError:
            return {"error": "Quiz format was invalid. Please try again."}
