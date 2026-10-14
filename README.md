# DevOps Failure Intelligence Platform

[![CI](https://github.com/saikishore2410/operations-intelligence-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/saikishore2410/operations-intelligence-dashboard/actions/workflows/ci.yml) ![Java](https://img.shields.io/badge/Java-17-orange?logo=openjdk) ![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python) ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker) [![Issues](https://img.shields.io/github/issues/saikishore2410/operations-intelligence-dashboard)](https://github.com/saikishore2410/operations-intelligence-dashboard/issues)

**Turn noisy CI/CD failures into evidence-backed diagnoses and practical next steps.**

DFIP combines a Java Spring Boot API, a Python FastAPI analyzer, and PostgreSQL persistence to classify common pipeline failures, show supporting log evidence, and help teams track incident patterns.

## Why it matters
Build and deployment failures often require engineers to scan long logs and repeat the same investigation. DFIP shortens the first diagnostic pass while keeping recovery decisions under human control.

## Key capabilities
- Deterministic classification for dependency, test, compilation/build, Docker, network, and unknown failures.
- Relevant log evidence, confidence information, suggested actions, and human-review guidance.
- Incident history with repository/run deduplication.
- Analytics for totals, category counts, review counts, confidence, and recent trends.
- Responsive dashboard with KPIs, incident history, category distribution, and manual log analysis.
- Optional LLM explanations grounded in deterministic diagnosis.
- GitHub Actions checks and Docker Compose orchestration.

## Architecture
    Dashboard / GitHub Actions
              |
              v
    Spring Boot API ------> PostgreSQL
              |
              v
    Python FastAPI Analyzer
      |-- deterministic classification
      |-- log evidence and redaction
      +-- optional LLM explanation

## Stack
Java 17, Spring Boot, Python 3.11, FastAPI, PostgreSQL, Docker Compose, GitHub Actions, optional OpenAI-compatible LLM endpoint.

## Quick start
    git clone https://github.com/saikishore2410/operations-intelligence-dashboard.git
    cd operations-intelligence-dashboard
    docker compose up --build

Local endpoints:
- Dashboard/API: http://localhost:8080/
- API health: http://localhost:8080/api/v1/health
- Incident history: http://localhost:8080/api/v1/incidents
- Analytics: http://localhost:8080/api/v1/analytics
- Analyzer docs: http://localhost:8001/docs

## Tests
    cd services/analyzer
    pip install -r requirements.txt
    pytest -q
    cd ../api
    mvn test

## Limitations and safety
Diagnostics are advisory; review recommendations before changing production workloads. Unknown failures need human investigation. Signed GitHub webhook ingestion and authenticated automatic log retrieval are not yet implemented. Redaction is best-effort; never submit secrets or sensitive logs. A live deployment URL is not included because one has not been verified.

## Roadmap
1. Signed webhook ingestion with least-privilege permissions.
2. Stronger redaction before persistence or model calls.
3. Evaluation datasets and classification regression thresholds.
4. Recovery outcome tracking and operational SLO reporting.

## Contributing
Include reproduction steps, expected behaviour, and test results with proposed changes.

## License
MIT
