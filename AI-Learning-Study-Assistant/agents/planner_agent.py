from ollama_service import generate
from database import save_memory

class PlannerAgent:
    def create(self, subject, days):
        prompt = f"""
Create a realistic study plan for a college student.

Subject: {subject}
Number of days: {days}

For each day include:
1. Topic
2. Learning activity
3. Short revision task
4. Approximate study time

Keep it simple and practical.
"""
        result = generate(prompt)
        save_memory(subject, f"Study plan for {days} days:\n{result}")
        return result
