# AI Learning & Study Assistant

An Agentic AI-style learning assistant built with:

- HTML/CSS/JavaScript frontend
- Python Flask backend
- SQLite memory/progress storage
- RAG using ChromaDB
- Sentence Transformers embeddings
- Ollama local LLM
- Study-plan generation
- Quiz generation
- Progress/memory tracking

## Project flow

Student
  -> HTML UI
  -> Flask backend
  -> Study Agent
  -> RAG / Planner / Quiz
  -> Ollama LLM
  -> SQLite memory
  -> Result shown in HTML

## 1. Install Python

Python 3.11 is recommended.

## 2. Create virtual environment

Windows:

    python -m venv venv
    venv\Scripts\activate

## 3. Install packages

    pip install -r requirements.txt

## 4. Install Ollama

Install Ollama on your computer, then download the model:

    ollama pull llama3.2

Start Ollama if it is not already running:

    ollama serve

## 5. Run the project

    python app.py

Open:

    http://127.0.0.1:5000

## 6. Test the RAG workflow

1. Open Course Material.
2. Upload a PDF or TXT file.
3. Open Study Chat.
4. Ask a question related to the uploaded material.
5. The RAG agent retrieves relevant text.
6. Ollama generates the answer.
7. The interaction is saved in SQLite memory.

## GitHub

Push the whole project folder to GitHub.

Do NOT push:

- venv/
- study_assistant.db
- chroma_db/
- course material PDFs/TXT files
- .env

The included .gitignore handles these files.

### Git commands

    git init
    git add .
    git commit -m "Initial AI Learning Study Assistant"
    git branch -M main
    git remote add origin YOUR_GITHUB_REPOSITORY_URL
    git push -u origin main

## Important deployment note

GitHub is suitable for storing the source code, but GitHub Pages cannot run the Python Flask backend or Ollama.

For a real online deployment, the Flask backend must run on a server. Ollama also needs to be reachable from that server, or the project can be changed to use a hosted LLM API.

The app already supports an OLLAMA_URL environment variable, so the Ollama endpoint can be changed without editing the Python code.

## Main folders

app.py                  -> Flask application
database.py             -> SQLite memory/progress
ollama_service.py       -> Ollama connection
agents/                 -> Agent logic
rag/                    -> RAG document loading/retrieval
tools/                  -> Tool functions
templates/              -> HTML pages
static/                 -> CSS and JavaScript
course_materials/       -> Uploaded learning files
