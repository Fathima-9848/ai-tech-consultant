from fastapi.testclient import TestClient
import importlib


task1 = importlib.import_module("task1-knowledge-brain.main")
task2 = importlib.import_module("task2-inbox-agent.main")
task3 = importlib.import_module("task3-meeting-to-scope.main")

client1 = TestClient(task1.app)
client2 = TestClient(task2.app)
client3 = TestClient(task3.app)


def test_task1_home():
    response = client1.get("/")
    assert response.status_code == 200
    assert "running" in response.json()["message"].lower()


def test_task2_home():
    response = client2.get("/")
    assert response.status_code == 200
    assert "running" in response.json()["message"].lower()


def test_task2_rejects_empty_email():
    response = client2.post(
        "/classify",
        json={"subject": " ", "body": " "}
    )
    assert response.status_code == 400


def test_task3_home():
    response = client3.get("/")
    assert response.status_code == 200
    assert "running" in response.json()["message"].lower()


def test_task3_rejects_empty_notes():
    response = client3.post(
        "/generate-scope",
        json={"meeting_notes": " "}
    )
    assert response.status_code == 400


def test_task2_duplicate_payment_priority():
    response = client2.post(
        "/classify",
        json={
            "subject": "Payment deducted twice",
            "body": (
                "My account was charged twice for the same order. "
                "Please help me with this duplicate payment."
            )
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["category"] == "Billing"
    assert result["priority"] == "High"
    assert result["suggested_reply"].strip() != ""


def test_task3_generates_project_scope():
    response = client3.post(
        "/generate-scope",
        json={
            "meeting_notes": (
                "The customer wants an online shopping website. "
                "Customers should be able to view products, "
                "add products to a cart, and log in. "
                "The website should work on mobile phones "
                "and computers."
            )
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["project_summary"].strip() != ""
    assert isinstance(result["functional_requirements"], list)
    assert len(result["functional_requirements"]) > 0
    assert isinstance(result["open_questions"], list)


def test_task1_health():
    response = client1.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_task1_search_rejects_short_question():
    response = client1.get(
        "/search",
        params={"q": "a"}
    )

    assert response.status_code == 422


def test_task1_search_returns_results():
    response = client1.get(
        "/search",
        params={
            "q": "How can I feature members on the homepage?",
            "top_k": 3
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["query"] == (
        "How can I feature members on the homepage?"
    )
    assert "results" in result
    assert isinstance(result["results"], list)
    assert len(result["results"]) > 0

    first_result = result["results"][0]

    assert "title" in first_result
    assert "url" in first_result
    assert "text" in first_result
    assert "score" in first_result



def test_task1_ask_rejects_empty_question():
    response = client1.post(
        "/ask",
        json={"question": " "}
    )

    assert response.status_code == 400


def test_task1_ask_returns_answer_and_sources():
    response = client1.post(
        "/ask",
        json={
            "question": "How can I feature members on the homepage?"
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["question"] == (
        "How can I feature members on the homepage?"
    )
    assert isinstance(result["answer"], str)
    assert result["answer"].strip() != ""
    assert isinstance(result["sources"], list)

    for source in result["sources"]:
        assert "title" in source
        assert "url" in source
        assert "score" in source
