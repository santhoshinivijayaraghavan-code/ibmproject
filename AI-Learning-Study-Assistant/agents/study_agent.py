from ollama_service import generate
from database import save_memory
from agents.rag_agent import RAGAgent
from agents.planner_agent import PlannerAgent
from agents.quiz_agent import QuizAgent

class StudyAgent:
    def __init__(self, retriever):
        self.rag = RAGAgent(retriever)
        self.planner = PlannerAgent()
        self.quiz = QuizAgent()

    def answer_question(self, question):
        context = self.rag.get_context(question)

        prompt = f"""
You are an AI Learning and Study Assistant.
Answer the student's question clearly and simply.

Use the course-material context when it is relevant.
If the context does not contain the answer, say that the answer is not found
in the uploaded material and then provide a general explanation if possible.

Course material context:
{context}

Student question:
{question}

Give a concise, student-friendly answer.
"""
        answer = generate(prompt)
        save_memory("Question", f"Q: {question} | A: {answer}")
        return answer

    def create_plan(self, subject, days):
        return self.planner.create(subject, days)

    def generate_quiz(self, topic):
        return self.quiz.generate(topic)
