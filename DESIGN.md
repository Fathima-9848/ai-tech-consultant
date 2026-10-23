# AI Tech Consultant — Design Document

## 1. Problem Statement
Customer support and project planning often require teams to search knowledge articles, respond to customer emails, and convert meetings into clear requirements. This prototype brings these workflows into one application.

## 2. System Architecture
The application contains three FastAPI backend services and a React/Vite frontend.

### Task 1: Knowledge Brain
The Knowledge Brain retrieves relevant content from knowledge articles and uses it to answer user questions. The API exposes interactive documentation through FastAPI Swagger UI. Retrieval quality depends on article extraction, chunking, embeddings, and similarity thresholds. Answers should include relevant sources when available.

### Task 2: Inbox Agent
The Inbox Agent receives an email subject and body, classifies the message, identifies its intent and priority, and generates a suggested reply. It calls the Knowledge Brain API to obtain supporting information. The current implementation uses an Ollama chat endpoint with the configured model `qwen3:1.7b`. Generated replies require human review before being sent to customers.

### Task 3: Meeting to Scope
This service converts meeting notes into a structured summary, functional and technical requirements, and open questions. Missing information, such as budget, timeline, or technology choices, should be confirmed with the client instead of being treated as fact.

### Frontend
The React/Vite frontend provides a user interface for interacting with the workflows. Backend APIs are exposed on local ports 8000, 8001, and 8002 during development.

## 3. Design Decisions
- Separate the three workflows into distinct services to make development and debugging easier.
- Use FastAPI to expose HTTP endpoints and Swagger UI for manual API testing.
- Use retrieval-based responses for knowledge questions rather than relying only on a language model's internal knowledge.
- Connect the Inbox Agent to the Knowledge Brain so suggested replies can use retrieved support information.
- Return structured fields for email classification and meeting-to-scope outputs.
- Keep humans responsible for approving customer replies and confirming project scope.

## 4. Model and Retrieval Choices
The Inbox Agent is configured to call Ollama using `qwen3:1.7b`. The Knowledge Brain uses a retrieval workflow with a similarity threshold configured during development. Retrieval quality should be evaluated using representative questions and the correctness of returned sources.

The actual embedding model, database configuration, chunking parameters, and complete ingestion/update behavior should be documented after checking the implementation.

## 5. Error Handling and Safety
- Model or service availability can affect response generation.
- Knowledge-based answers may be incomplete when relevant content is not retrieved.
- Generated replies can contain unsupported claims; they must be reviewed before sending.
- Meeting notes may omit important details. Unanswered questions should remain visible.
- Do not expose secrets or private customer information in logs or submitted files.

## 6. Features Requiring Further Verification
The following requirements need explicit verification before they can be claimed as complete:
- Resumable ingestion and daily incremental updates
- Handling deleted or changed knowledge articles
- Understanding and using article images
- Human escalation for unanswered questions
- A 20-consecutive-approval safeguard and feedback history for the Inbox Agent
- Follow-up change detection and human approval for scope changes
- Automated evaluation coverage for all three tasks

## 7. Limitations
This is a prototype. Its outputs depend on source quality, retrieval behavior, model availability, and the completeness of user input. It should not automatically send customer emails or treat unconfirmed estimates and assumptions as final commitments.

## 8. Next Steps
1. Add or verify automated tests for each service.
2. Evaluate at least 20 representative cases per task.
3. Verify human-review and approval safeguards.
4. Test service failures, missing information, and unsupported questions.
5. Improve setup documentation and provide a reproducible startup workflow.
