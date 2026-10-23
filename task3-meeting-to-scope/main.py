
import requests
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AI Tech Consultant - Meeting to Scope")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3:1.7b"


class MeetingRequest(BaseModel):
    meeting_notes: str


@app.get("/")
def home():
    return {
        "message": "AI Tech Consultant Meeting to Scope is running!"
    }


@app.post("/generate-scope")
def generate_scope(request: MeetingRequest):
    meeting_notes = request.meeting_notes.strip()

    if not meeting_notes:
        raise HTTPException(
            status_code=400,
            detail="Please provide meeting notes."
        )

    prompt = f"""
You are an experienced technical consultant.

Convert the customer's meeting notes into a clear project scope.

Return ONLY a valid JSON object with these keys:
project_summary, functional_requirements,
technical_requirements, open_questions, assumptions.

Rules:
- Use only information supported by the meeting notes.
- Do not invent confirmed customer decisions.
- Put missing information under open_questions.
- List reasonable but unconfirmed details under assumptions.
- Write the requirements in simple, clear language.
- functional_requirements and technical_requirements
  must be JSON arrays of strings.
- open_questions and assumptions must be JSON arrays of strings.

Meeting notes:
{meeting_notes}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False,
                "format": "json"
            },
            timeout=180
        )

        response.raise_for_status()

        result = response.json()["message"]["content"]
        scope = __import__("json").loads(result)

        return {
            "project_summary": scope.get("project_summary", ""),
            "functional_requirements": scope.get(
                "functional_requirements", []
            ),
            "technical_requirements": scope.get(
                "technical_requirements", []
            ),
            "open_questions": scope.get("open_questions", []),
            "assumptions": scope.get("assumptions", [])
        }

    except requests.RequestException as error:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama AI service error: {str(error)}"
        )

    except (KeyError, ValueError):
        raise HTTPException(
            status_code=502,
            detail="Could not process the AI response. Please try again."
        )
