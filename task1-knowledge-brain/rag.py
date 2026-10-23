
import requests

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3:1.7b"


SEARCH_URL = "http://127.0.0.1:8000/search"

# Keep only search results with this minimum similarity score.
SIMILARITY_THRESHOLD = 0.45


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    try:
        # Search the knowledge base
        search_response = requests.get(
            SEARCH_URL,
            params={"q": question, "top_k": 3},
            timeout=60
        )
        search_response.raise_for_status()

        search_data = search_response.json()
        results = search_data.get("results", [])

        # Filter results using the similarity threshold
        results = [
            item for item in results
            if item.get("score", 0) >= SIMILARITY_THRESHOLD
        ]

        if not results:
            return {
                "question": question,
                "answer": (
                    "I could not find enough information "
                    "in the available documents."
                ),
                "sources": []
            }

        # Build context from retrieved documents
        context_parts = []

        for item in results:
            context_parts.append(
                f"Title: {item.get('title', '')}\n"
                f"Source: {item.get('url', '')}\n"
                f"Content: {item.get('text', '')}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are a careful technical support assistant.

Answer the user's question using only facts explicitly
supported by the context below.

Do not invent menu paths, features, settings, CSS classes,
SQL queries, or instructions.

A search similarity score does not prove that a statement
is true. Check whether the context actually supports the answer.

If the context does not clearly answer the question, say:
"I could not find enough information in the available documents."

If the context only partially answers the question, explain
what is supported and what information is missing.

Context:
{context}

User question:
{question}
"""

        # Ask the local Ollama model
        ai_response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False
            },
            timeout=180
        )
        ai_response.raise_for_status()

        answer = ai_response.json()["message"]["content"]

        # Return unique source URLs only
        sources = []
        seen_urls = set()

        for item in results:
            url = item.get("url", "")

            if url and url not in seen_urls:
                seen_urls.add(url)

                sources.append({
                    "title": item.get("title", ""),
                    "url": url,
                    "score": item.get("score", 0)
                })

        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }

    except HTTPException:
        raise

    except requests.RequestException as error:
        raise HTTPException(
            status_code=502,
            detail=f"Search or AI service error: {str(error)}"
        )

    except (KeyError, ValueError) as error:
        raise HTTPException(
            status_code=502,
            detail=f"Invalid response from AI service: {str(error)}"
        )
