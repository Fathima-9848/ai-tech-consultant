# AI Tech Consultant � Evaluation Report

## 1. Evaluation Approach
The application should be evaluated on correctness, relevance, grounding in source material, structured output, reliability, and handling of missing information.

**Important:** The cases below are a test plan and preliminary development observations. They are not a claim that all 20 cases per task have been executed. Record actual results after running each test.

## 2. Task 1 � Knowledge Brain

| ID | Test input | Expected behavior | Status |
|---|---|---|---|
| KB-01 | Ask how to change an account password | Relevant instructions and sources are returned | Observed working during development |
| KB-02 | Ask about changing a member password | Retrieve relevant article content | Pending formal evaluation |
| KB-03 | Ask about an unrelated topic | Avoid unsupported claims or indicate insufficient evidence | Pending |
| KB-04 | Ask a vague question | Request clarification or provide a cautious answer | Pending |
| KB-05 | Ask a question with no matching article | Avoid inventing an answer | Pending |
| KB-06 | Ask about an article title | Retrieve the relevant article | Pending |
| KB-07 | Ask a question using different wording | Retrieve semantically relevant content | Pending |
| KB-08 | Ask a multi-part question | Address supported parts and identify gaps | Pending |
| KB-09 | Ask about outdated content | Follow the actual indexed source and disclose limitations | Pending |
| KB-10 | Ask about a changed article | Verify updated content is reflected | Pending |
| KB-11 | Ask about a deleted article | Verify deleted content is no longer returned | Pending |
| KB-12 | Search for an image-related answer | Verify image content is actually supported | Pending |
| KB-13 | Ask a question requiring multiple sources | Return relevant supporting sources | Pending |
| KB-14 | Submit an empty question | Validate input and return a suitable error | Pending |
| KB-15 | Submit a very long question | Handle input safely | Pending |
| KB-16 | Stop the knowledge service | Handle service failure gracefully | Pending |
| KB-17 | Use the search endpoint | Return relevant search results | Tested manually during development; full scoring pending |
| KB-18 | Ask about an account setting | Ground the answer in retrieved content | Pending |
| KB-19 | Repeat a question | Check consistency of retrieved sources | Pending |
| KB-20 | Ask an unsupported technical question | Avoid presenting guesses as facts | Pending |

## 3. Task 2 � Inbox Agent

| ID | Test input | Expected behavior | Status |
|---|---|---|---|
| IA-01 | Email: unable to log in | Correct category and useful next steps | Tested manually; improvement needed |
| IA-02 | Email: change account password | Account-related classification and relevant guidance | Tested manually during development |
| IA-03 | Email: payment deducted twice | Billing category, high priority, cautious reply | Tested manually; reply wording needs review |
| IA-04 | Email: refund request | Identify billing/refund intent | Pending |
| IA-05 | Email: account locked | Identify account access issue | Pending |
| IA-06 | Email: product feature question | Use relevant knowledge when available | Pending |
| IA-07 | Email with urgent outage | Recognize urgency | Pending |
| IA-08 | Email with unclear subject | Use body content or flag ambiguity | Pending |
| IA-09 | Empty email body | Validate or request missing details | Pending |
| IA-10 | Email with conflicting details | Avoid unsupported conclusions | Pending |
| IA-11 | Email containing angry language | Use professional, empathetic wording | Pending |
| IA-12 | Email requesting a refund exception | Avoid promising an unverified outcome | Pending |
| IA-13 | Email unrelated to the product | Flag or classify cautiously | Pending |
| IA-14 | Email with multiple issues | Identify the main issue and relevant details | Pending |
| IA-15 | Knowledge Brain unavailable | Handle dependency failure safely | Pending |
| IA-16 | Ollama unavailable | Return a clear failure response | Pending |
| IA-17 | Email containing instruction-like malicious text | Treat email content as untrusted input | Pending |
| IA-18 | Similar emails with different wording | Check classification consistency | Pending |
| IA-19 | Review and edit a generated reply | Ensure a human can review before sending | Pending |
| IA-20 | Track repeated human approvals | Verify the required approval safeguard | Pending |

## 4. Task 3 � Meeting to Scope

| ID | Test input | Expected behavior | Status |
|---|---|---|---|
| MS-01 | Notes for an online shopping website | Generate structured requirements and open questions | Tested manually during development |
| MS-02 | Notes without a budget | Identify budget as unknown | Observed in manual test |
| MS-03 | Notes without a timeline | Identify timeline as unknown | Observed in manual test |
| MS-04 | Notes without a technology stack | Leave the stack to be confirmed | Observed in manual test |
| MS-05 | Notes with explicit functional requirements | Preserve the stated requirements | Pending |
| MS-06 | Notes with technical constraints | Include stated constraints | Pending |
| MS-07 | Notes with contradictory requirements | Flag the contradiction | Pending |
| MS-08 | Very short meeting notes | Avoid inventing missing details | Pending |
| MS-09 | Long meeting notes | Extract key decisions and requirements | Pending |
| MS-10 | Notes with action items | Identify follow-up actions | Pending |
| MS-11 | Notes with user roles | Capture role-specific needs | Pending |
| MS-12 | Notes with integrations | Record integration requirements | Pending |
| MS-13 | Notes with security needs | Capture security requirements | Pending |
| MS-14 | Notes with performance needs | Capture stated performance expectations | Pending |
| MS-15 | Notes with a fixed deadline | Preserve the specified deadline | Pending |
| MS-16 | Notes with a fixed budget | Preserve the specified budget | Pending |
| MS-17 | Notes requesting an unsupported feature | Identify feasibility questions | Pending |
| MS-18 | Follow-up notes changing scope | Detect and summarize changes | Pending |
| MS-19 | Empty meeting notes | Request valid input | Pending |
| MS-20 | Review the generated proposal | Allow human confirmation before treating it as final | Pending |

## 5. Preliminary Observations
- Task 1 returned a useful account-password answer with source references during manual development testing.
- Task 2 returned structured classification and suggested-reply fields in manual API tests. Some reply wording required review to avoid implying that an issue had already been confirmed.
- Task 3 generated a structured scope from online-shopping meeting notes and identified missing budget, timeline, and technology-stack details.

These observations are qualitative. No numerical accuracy, latency, or cost scores are claimed here.

## 6. Evaluation Still Required
- Execute all test cases and record actual outcomes.
- Calculate accuracy for classification and requirement extraction where suitable.
- Check whether answers are supported by retrieved sources.
- Measure response latency and model/service failures.
- Compare model configurations only after running comparable tests.
- Record failures, fixes, and regression-test results.

## Manual API Smoke Tests � 2026-10-23

| Task | Endpoint | Input | Result | Notes |
|---|---|---|---|---|
| Task 1: Knowledge Brain | POST /ask | Account password question | PASS - HTTP 200 | Answer and two source references returned. Verify answer details against source documents. |
| Task 2: Inbox Agent | POST /classify | Duplicate payment complaint | PASS - HTTP 200 | Billing category, High priority, suggested reply, and knowledge result returned. Duplicate-charge guidance was insufficient. |
| Task 3: Meeting to Scope | POST /generate-scope | Online shopping website meeting notes | PASS - HTTP 200 | Summary, six functional requirements, and budget/timeline open question returned. Technical requirements were empty in this test. |

These are three manual API smoke tests, not the complete evaluation suite.
Other evaluation cases remain pending until actually executed.

### Inbox Agent — Suggested Reply Safety Improvement (2026-10-23)

**Test input**

- Subject: `Payment deducted twice`
- Body: `I was charged twice for the same order. Please check and help me get a refund.`

**Expected behavior**
- Classify the email as Billing.
- Assign High priority for a reported duplicate charge.
- Generate a polite reply without promising an unverified refund.
- Explain that the support team will review the transaction and verify whether a duplicate charge occurred.

**Observed result**
- Category: Billing
- Priority: High
- Intent: Duplicate payment and refund request.
- Suggested reply: The support team will review the transaction details, verify whether a duplicate charge occurred, and advise on the applicable refund process if confirmed.

**Result: PASS**

The payment-related reply safety rule was added to `task2-inbox-agent/main.py`. After restarting the backend on port 8001, the frontend returned the updated reply successfully.

This is a manual test of the duplicate-payment scenario. Other payment and refund scenarios still need testing.