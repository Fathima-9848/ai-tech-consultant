# AI-Assisted Development Log

## Project
AI Tech Consultant — Knowledge Brain, Inbox Agent, and Meeting to Scope.

## Useful Prompts

The following prompts summarize the types of assistance used during development. Keep only prompts that accurately reflect the work performed.

1. **Debug API startup**
   "Help me diagnose this FastAPI startup error. Explain the cause in beginner-friendly steps and suggest the smallest safe fix."

2. **Improve knowledge retrieval**
   "Review the retrieval code and explain how the similarity threshold affects relevant results. Suggest a way to test the change without claiming unverified improvements."

3. **Connect the Inbox Agent**
   "Help connect the email-classification API to the Knowledge Brain API. Preserve structured output and handle dependency failures safely."

4. **Improve email reply safety**
   "Review this generated customer reply. Identify claims that are not supported by the email or retrieved knowledge and rewrite it without making promises."

5. **Structure meeting requirements**
   "Convert these meeting notes into functional requirements, technical requirements, assumptions, and open questions. Do not invent missing budget, timeline, or technology decisions."

## Example of Revising AI-Generated Work

During manual testing of the Inbox Agent, a duplicate-payment email produced wording similar to: "We are aware of the issue."

This wording was not safe to use without evidence that the organization had already confirmed the issue. A safer alternative is:

"Hello, thank you for contacting us. We understand that you may have been charged twice for the same transaction. Our support team will review the payment details and assist you with the next steps. We appreciate your patience."

The revised wording acknowledges the customer's concern without claiming that the issue has already been confirmed. A human should review the final reply before sending it.

## Development Principles
- Use AI assistance to understand errors and improve implementation.
- Check suggested changes against the actual code and API behavior.
- Prefer small changes that can be tested.
- Do not treat generated answers as verified facts.
- Do not include passwords, API keys, or private customer information in prompts or submitted logs.

## Transparency
This document is a summary of development activities and prompt patterns. Before submission, ensure that the prompts and example above accurately represent the actual AI-assisted work performed. Do not present paraphrased prompts as exact quotations from a saved conversation.
