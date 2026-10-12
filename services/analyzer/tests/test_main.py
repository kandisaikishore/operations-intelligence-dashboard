from fastapi.testclient import TestClient
from app.main import app, analyze_log, redact_secrets

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_dependency_failure_has_evidence():
    result = analyze_log("[ERROR] Could not resolve dependencies for project demo")
    assert result.category == "DEPENDENCY"
    assert result.evidence
    assert result.needs_human_review is False

def test_test_failure_classification():
    result = analyze_log("Tests run: 10, Failures: 1\njava.lang.AssertionError: expected 2")
    assert result.category == "TEST_FAILURE"

def test_unknown_routes_to_human():
    result = analyze_log("runner exited unexpectedly")
    assert result.category == "UNKNOWN"
    assert result.needs_human_review is True
    assert result.confidence < 0.5

def test_analyze_endpoint_validates_input():
    response = client.post("/analyze", json={"repository":"demo/api","run_id":"42","log_text":"[ERROR] cannot find symbol"})
    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "BUILD_CONFIGURATION"
    assert body["recommended_actions"]

def test_redacts_common_secrets():
    value = redact_secrets("Authorization: Bearer abcdefghijklmnop password=supersecret ghp_abcdefghijklmnopqrstuvwxyz123456")
    assert "supersecret" not in value
    assert "ghp_abcdefghijklmnopqrstuvwxyz123456" not in value
    assert "[REDACTED]" in value

def test_explain_requires_key_when_disabled(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    diagnosis = analyze_log("Tests run: 2, Failures: 1")
    response = client.post("/explain", json={"log_text":"Tests run: 2, Failures: 1", "diagnosis":diagnosis.model_dump()})
    assert response.status_code == 503

def test_analyze_endpoint_redacts_secrets_before_returning_evidence():
    response = client.post("/analyze", json={
        "repository": "demo/api",
        "run_id": "secret-check",
        "log_text": "ERROR password=supersecret"
    })
    assert response.status_code == 200
    assert "supersecret" not in response.text
    assert "[REDACTED]" in response.text


def test_explain_recomputes_diagnosis_and_sends_only_redacted_logs(monkeypatch):
    import json
    from app import main

    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": "Likely cause: tests failed."}}]}

    def fake_post(url, **kwargs):
        captured["payload"] = kwargs["json"]
        return FakeResponse()

    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setattr(main.httpx, "post", fake_post)
    client_supplied_diagnosis = analyze_log("runner exited unexpectedly").model_dump()
    response = client.post("/explain", json={
        "log_text": "Tests run: 2, Failures: 1\\npassword=supersecret",
        "diagnosis": client_supplied_diagnosis
    })

    assert response.status_code == 200
    assert response.json()["classification_source"] == "deterministic"
    prompt = captured["payload"]["messages"][1]["content"]
    assert '"category":"TEST_FAILURE"' in prompt
    assert "supersecret" not in prompt
