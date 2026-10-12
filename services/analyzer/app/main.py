"""Evidence-backed deterministic CI failure analysis API."""
from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="DFIP Analyzer", version="0.1.0",
              description="Explainable CI/CD failure classification from supplied log evidence.")

class AnalyzeRequest(BaseModel):
    repository: str = Field(min_length=1, max_length=250)
    run_id: str = Field(min_length=1, max_length=100)
    log_text: str = Field(min_length=1, max_length=500_000)

class Diagnosis(BaseModel):
    category: Literal["DEPENDENCY", "TEST_FAILURE", "BUILD_CONFIGURATION", "DOCKER", "NETWORK", "UNKNOWN"]
    summary: str
    confidence: float
    evidence: list[str]
    recommended_actions: list[str]
    needs_human_review: bool

RULES = [
    ("DEPENDENCY", ("could not resolve dependencies", "could not find artifact", "dependencyresolutionexception", "npm err! code e", "no matching distribution found"),
     "Dependency resolution failed.", 0.90,
     ["Check dependency coordinates and repository availability.", "Verify lockfiles and package registry credentials without exposing secrets."]),
    ("TEST_FAILURE", ("tests run:", "assertionerror", "failed: test", "there are test failures", "pytest failed"),
     "Automated tests failed.", 0.91,
     ["Inspect the first failing test and its assertion or traceback.", "Reproduce the failure locally before changing application code."]),
    ("BUILD_CONFIGURATION", ("compilation failure", "failed to execute goal", "cannot find symbol", "syntax error", "gradle build failed"),
     "Build configuration or compilation failure detected.", 0.86,
     ["Read the first compiler error above the final build summary.", "Run the project build and tests locally after correcting the earliest source error."]),
    ("DOCKER", ("failed to solve", "docker build", "error response from daemon", "manifest unknown", "no such file or directory: dockerfile"),
     "Container build or image configuration failed.", 0.88,
     ["Check the Dockerfile path, build context, and referenced files.", "Confirm the base image tag exists and inspect the first Docker build error."]),
    ("NETWORK", ("connection timed out", "temporary failure in name resolution", "connection refused", "http 502", "read timed out"),
     "A network or remote-service connection failure is likely.", 0.73,
     ["Check service health, DNS, firewall rules, and endpoint configuration.", "Retry only after confirming the dependency is transient and safe to retry."]),
]

def analyze_log(log_text: str) -> Diagnosis:
    normalized = log_text.lower()
    lines = [line.strip() for line in log_text.splitlines() if line.strip()]
    for category, patterns, summary, confidence, actions in RULES:
        matched = [line[:500] for line in lines if any(p in line.lower() for p in patterns)]
        if matched:
            return Diagnosis(category=category, summary=summary, confidence=confidence,
                             evidence=matched[:5], recommended_actions=actions,
                             needs_human_review=False)
    evidence = [line[:500] for line in lines if "error" in line.lower() or "fail" in line.lower()]
    return Diagnosis(category="UNKNOWN", summary="No known failure signature matched; manual investigation is required.",
                     confidence=0.25, evidence=evidence[:5],
                     recommended_actions=["Inspect the earliest error, not only the final job failure line.",
                                          "Check recent code, dependency, secret, and environment changes."],
                     needs_human_review=True)

@app.get("/health")
def health():
    return {"status": "ok", "service": "dfip-analyzer", "version": "0.1.0"}

@app.post("/analyze", response_model=Diagnosis)
def analyze(request: AnalyzeRequest):
    return analyze_log(request.log_text)
