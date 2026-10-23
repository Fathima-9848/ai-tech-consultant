# AI Tech Consultant

## Overview
AI Tech Consultant is a prototype that combines three AI-assisted workflows:

1. **Knowledge Brain** — answers questions using retrieved knowledge articles.
2. **Inbox Agent** — classifies customer emails and generates suggested replies with knowledge support.
3. **Meeting to Scope** — converts meeting notes into structured project requirements and open questions.

## Technology
- Python and FastAPI for backend APIs
- React and Vite for the frontend
- Ollama for local language-model integration in the Inbox Agent
- A retrieval-based workflow for Knowledge Brain

## Project Structure
- `task1-knowledge-brain/` — Knowledge Brain API and ingestion components
- `task2-inbox-agent/` — Customer email classification and reply suggestions
- `task3-meeting-to-scope/` — Meeting notes to project scope
- `frontend/` — Web interface
- `shared-docs/` — Shared project documents

## Prerequisites
- Python installed
- Node.js and npm installed
- Ollama installed and configured if using the local model
- Any database or other services required by the configured application

## Setup
Open PowerShell in the project root:

```powershell
cd C:\Users\fathi\ai-tech-consultant
.\.venv\Scripts\Activate.ps1
```

Install frontend dependencies if needed:

```powershell
cd frontend
npm install
```

Start the frontend in its own terminal:

```powershell
npm run dev
```

Start each backend in a separate terminal from the project root, with the virtual environment activated. Use the actual module and startup command configured for each task.

- Task 1 API: `http://127.0.0.1:8000/docs`
- Task 2 API: `http://127.0.0.1:8001/docs`
- Task 3 API: `http://127.0.0.1:8002/docs`
- Frontend: `http://localhost:5173/`

## Configuration and Safety
Check the project configuration before running the application. Start required services, including Ollama and the database if configured. Do not commit credentials, passwords, API keys, or private customer data.

## Current Status
The three APIs and frontend have been exercised during development. Run the tests and verify all required services before relying on the application. Features that have not been fully tested should be treated as pending.

## Limitations
Generated answers and project requirements need human review. Output quality depends on retrieved content, model availability, and input quality. Estimates and assumptions should be confirmed with the client before use.

## Documentation
- `DESIGN.md` — Architecture and design decisions
- `EVALS.md` — Evaluation cases and observed results
- `AI_LOG.md` — AI-assisted development notes
