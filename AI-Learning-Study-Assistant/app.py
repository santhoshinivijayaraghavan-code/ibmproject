import os
from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_progress
from agents.study_agent import StudyAgent
from rag.document_loader import load_documents
from rag.retriever import RAGRetriever

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

init_db()

retriever = RAGRetriever()
study_agent = StudyAgent(retriever)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("course_file")
    if not file or not file.filename:
        flash("Please select a PDF or TXT file.")
        return redirect(url_for("index"))

    allowed = {".pdf", ".txt"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        flash("Only PDF and TXT files are supported.")
        return redirect(url_for("index"))

    os.makedirs("course_materials", exist_ok=True)
    path = os.path.join("course_materials", file.filename)
    file.save(path)

    chunks = load_documents(path)
    if not chunks:
        flash("No readable text was found in the file.")
        return redirect(url_for("index"))

    retriever.add_documents(chunks, source=file.filename)
    flash(f"{file.filename} added to the study knowledge base.")
    return redirect(url_for("index"))

@app.route("/chat", methods=["GET", "POST"])
def chat():
    answer = None
    question = ""
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            answer = study_agent.answer_question(question)
    return render_template("chat.html", answer=answer, question=question)

@app.route("/plan", methods=["GET", "POST"])
def plan():
    result = None
    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        days = request.form.get("days", "7").strip()
        result = study_agent.create_plan(subject, days)
    return render_template("plan.html", result=result)

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    quiz_data = None
    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        quiz_data = study_agent.generate_quiz(topic)
    return render_template("quiz.html", quiz_data=quiz_data)

@app.route("/progress")
def progress():
    data = get_progress()
    return render_template("progress.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
