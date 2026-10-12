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
