
import { useState } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";

const tools = [
  { id: "brain", number: "01", title: "Knowledge Brain", description: "Ask questions and find answers from support documentation.", icon: "✦" },
  { id: "inbox", number: "02", title: "Inbox Agent", description: "Classify customer emails and generate suggested replies.", icon: "✉" },
  { id: "scope", number: "03", title: "Meeting to Scope", description: "Turn meeting notes into a structured project scope.", icon: "▤" },
];

function App() {
  const [activeTool, setActiveTool] = useState("brain");
  const [question, setQuestion] = useState("");
  const [subject, setSubject] = useState("");
  const [emailBody, setEmailBody] = useState("");
  const [meetingNotes, setMeetingNotes] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");

  const selectedTool = tools.find((tool) => tool.id === activeTool);

  function chooseTool(id) {
    setActiveTool(id);
    setResult(null);
    setError("");
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    let url = "";
    let body = {};

    if (activeTool === "brain") {
      url = "http://127.0.0.1:8000/ask";
      body = { question };
    } else if (activeTool === "inbox") {
      url = "http://127.0.0.1:8001/classify";
      body = { subject, body: emailBody };
    } else {
      url = "http://127.0.0.1:8002/generate-scope";
      body = { meeting_notes: meetingNotes };
    }

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Request failed. Please try again.");
      }

      setResult(data);
    } catch (err) {
      const errorMessage =
        err.message === "Failed to fetch"
          ? "Unable to connect to the AI service. Please ensure the backend server is running and try again."
          : err.message || "Something went wrong. Please try again.";

      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }


  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">A</div>
          <div>
            <strong>AI CONSULTANT</strong>
            <span>TECH WORKSPACE</span>
          </div>
        </div>

        <p className="nav-label">WORKSPACE</p>

        <nav className="tool-nav">
          {tools.map((tool) => (
            <button
              key={tool.id}
              className={`nav-item ${activeTool === tool.id ? "active" : ""}`}
              onClick={() => chooseTool(tool.id)}
            >
              <span className="nav-icon">{tool.icon}</span>
              <span>{tool.title}</span>
              <span className="nav-number">{tool.number}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="status-dot" />
          <div>
            <strong>Local workspace</strong>
            <span>Development mode</span>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <span>Workspace / <strong>{selectedTool.title}</strong></span>
          <span className="environment"><span /> LOCAL ENVIRONMENT</span>
        </header>

        <section className="welcome">
          <div className="eyebrow">YOUR AI-POWERED WORKSPACE</div>
          <h1>Good work starts<br />with a <span>clear answer.</span></h1>
          <p>Three intelligent tools to help you research, support customers, and plan projects.</p>
        </section>

        <section className="tool-cards">
          {tools.map((tool) => (
            <button
              key={tool.id}
              className={`tool-card ${activeTool === tool.id ? "selected" : ""}`}
              onClick={() => chooseTool(tool.id)}
            >
              <div className="card-top">
                <span className="card-icon">{tool.icon}</span>
                <span className="card-number">{tool.number}</span>
              </div>
              <h3>{tool.title}</h3>
              <p>{tool.description}</p>
              <span className="card-action">
                Open tool <span>↗</span>
              </span>
            </button>
          ))}
        </section>

        <section className="workspace-panel">
          <div className="panel-heading">
            <div>
              <div className="eyebrow">AI TOOL · {selectedTool.number}</div>
              <h2>{selectedTool.title}</h2>
              <p>{selectedTool.description}</p>
            </div>
            <span className="ready-label"><span /> READY TO USE</span>
          </div>

          <form onSubmit={handleSubmit} className="tool-form">
            {activeTool === "brain" && (
              <label>
                What would you like to know?
                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="e.g. How can I feature members on the homepage?"
                  required
                  rows={4}
                />
              </label>
            )}

            {activeTool === "inbox" && (
              <>
                <label>
                  Email subject
                  <input
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                    placeholder="e.g. Unable to log in"
                    required
                  />
                </label>
                <label>
                  Customer email
                  <textarea
                    value={emailBody}
                    onChange={(e) => setEmailBody(e.target.value)}
                    placeholder="Paste the customer's email here..."
                    required
                    rows={5}
                  />
                </label>
              </>
            )}

            {activeTool === "scope" && (
              <label>
                Meeting notes
                <textarea
                  value={meetingNotes}
                  onChange={(e) => setMeetingNotes(e.target.value)}
                  placeholder="Describe the client's needs, goals, features, and requirements..."
                  required
                  rows={7}
                />
              </label>
            )}

            <button className="submit-button" type="submit" disabled={loading}>
              
              {loading && (
                  <div className="message loading-message" role="status" aria-live="polite">
                    <span className="loading-spinner" />
                    <span>
                      <strong>AI is working on your request</strong>
                      <small>Please wait while we prepare your result...</small>
                    </span>
                  </div>
                )}

              <span>→</span>
            </button>
          </form>

          {loading && <div className="message loading-message">AI is processing your request. Please wait...</div>}
          {error && <div className="message error-message">{error}</div>}
          {result && (
            <div className="result-panel">
              <div className="eyebrow">RESULT</div>
              <h3>Completed successfully</h3>
              {activeTool === "brain" && (
                <> 
                  <div className="result-answer">
                      <ReactMarkdown>
                        {result.answer
                          .replace(/&#x20;/g, " ")
                          .replace(/\\\*/g, "*")
                          .replace(/\\\./g, ".")}
                      </ReactMarkdown>
                    </div>
                  <h4>Sources</h4>
                  {result.sources?.length ? (
                    <ul className="sources-list">
                      {result.sources.map((source, index) => (
                        <li key={`${source.url}-${index}`}>
                          <a href={source.url} target="_blank" rel="noreferrer">{source.title || source.url}</a>
                          <span>Score: {Number(source.score).toFixed(3)}</span>
                        </li>
                      ))}
                    </ul>
                  ) : <p>No sources were returned for this question.</p>}
                </>
              )}
              {activeTool === "inbox" && (
                <div className="result-grid">
                  <ResultItem label="Category" value={result.category} />
                  <ResultItem label="Priority" value={result.priority} />
                  <ResultItem label="Intent" value={result.intent} />
                  <div className="result-wide">
                    <h4>Suggested reply</h4>
                    <p>{result.suggested_reply}</p>                                        
                    <button
                      type="button"
                      className="copy-button"
                      onClick={async () => {
                        try {
                          await navigator.clipboard.writeText(result.suggested_reply);
                          setToast("Reply copied successfully!");
                          setError("");
                          setTimeout(() => setToast(""), 2500);
                        } catch (err) {
                          setError("Could not copy the reply. Please copy the text manually.");
                        }
                      }}
                    >
                      Copy reply
                    </button>
                  </div>
                </div>
              )}
              {activeTool === "scope" && (
                <div className="scope-results">
                  <h4>Project summary</h4>
                  <p>{result.project_summary}</p>
                  <ResultList title="Functional requirements" items={result.functional_requirements} />
                  <ResultList title="Technical requirements" items={result.technical_requirements} />
                  <ResultList title="Open questions" items={result.open_questions} />
                  <ResultList title="Assumptions" items={result.assumptions} />
                </div>
              )}
            </div>
          )}
        </section>
        
          {toast && (
            <div className="toast-message" role="status" aria-live="polite">
              <span>✓</span>
              {toast}
            </div>
          )}

        <footer>AI Tech Consultant · Capstone Project · Local development</footer>
      </main>
    </div>
  );
}

function ResultItem({ label, value }) {
  return (
    <div className="result-item">
      <span>{label}</span>
      <strong>{value || "Not provided"}</strong>
    </div>
  );
}

function ResultList({ title, items }) {
  return (
    <div className="result-list">
      <h4>{title}</h4>
      {items?.length ? (
        <ul>{items.map((item, index) => <li key={`${title}-${index}`}>{item}</li>)}</ul>
      ) : <p>None provided.</p>}
    </div>
  );
}

export default App;
