# DevOps Failure Intelligence Platform (DFIP)

[![CI](https://github.com/saikishore2410/operations-intelligence-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/saikishore2410/operations-intelligence-dashboard/actions/workflows/ci.yml) ![Java](https://img.shields.io/badge/Java-17-orange) ![Python](https://img.shields.io/badge/Python-3.11-blue) ![License](https://img.shields.io/badge/License-MIT-green)

**Turn failed CI/CD runs into actionable, evidence-backed fixes.**

## The problem

Developers often lose time investigating failed GitHub Actions runs: logs are noisy, error messages are scattered, and teams repeatedly rediscover the same root causes. DFIP ingests build-failure evidence, classifies common failure modes, recommends practical remediation steps, and records incidents for follow-up.

## What works in this repository

- **Python analysis service** — FastAPI endpoint classifies Maven/Gradle, test, dependency, Docker, network, and generic failures with deterministic rules.
- **Evidence-backed output** — every diagnosis includes the matching log evidence, confidence, and next steps; unknown errors are explicitly marked for manual investigation.
- **Spring Boot API foundation** — Java 17 service exposes health and incident APIs and delegates analysis to the Python service.
- **PostgreSQL schema** — incident and diagnosis tables with indexes and JSONB evidence storage.
- **CI workflow** — runs Python unit tests and Java Maven tests on pushes and pull requests.
- **Docker Compose** — local orchestration for PostgreSQL, analyzer, and API.

## Architecture

```text
GitHub Actions / Webhook
        |
        v
Spring Boot API -----> PostgreSQL (incident history)
        |
        +------------> Python FastAPI Analyzer
                             |
                             v
                  Rules + evidence + remediation
```

The current implementation is intentionally deterministic-first: no LLM key is required, and diagnosis output is derived from matching log evidence. An LLM can be added later behind the same interface without making it the source of truth.

## Quick start

### Python analyzer

```bash
cd services/analyzer
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Try it:

```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"repository":"demo/service","run_id":"123","log_text":"[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin"}'
```

### Full stack

```bash
docker compose up --build
```

- Analyzer: http://localhost:8001/docs
- Spring Boot API: http://localhost:8080/actuator/health
- PostgreSQL: localhost:5432

## API contract

`POST /analyze`

Request:
```json
{"repository":"owner/repo","run_id":"123","log_text":"...failed build log..."}
```

Response:
```json
{
  "category":"BUILD_CONFIGURATION",
  "summary":"Build configuration or compilation failure detected.",
  "confidence":0.86,
  "evidence":["Failed to execute goal ..."],
  "recommended_actions":["Read the first compiler error above the final Maven failure summary.","Run ./mvnw -q test locally and fix the earliest source error."],
  "needs_human_review":false
}
```

## Testing

```bash
cd services/analyzer && pip install -r requirements.txt && pytest -q
cd ../../services/api && mvn test
```

## Security and limitations

- Do not submit secrets, tokens, customer data, or unredacted private logs.
- The first version accepts log text directly; GitHub webhook signature validation and authenticated log retrieval are planned hardening tasks.
- Rules are explainable heuristics, not a guarantee of root cause. Low-confidence or unknown failures are routed to human review.
- Never automatically rerun or modify production deployments based solely on a diagnosis.

## Roadmap

1. GitHub App/webhook ingestion with signature verification.
2. Durable incident persistence and deduplication.
3. Redaction pipeline for credentials and personal data.
4. Dashboard with incident trends and verified recovery status.
5. Optional LLM-assisted explanation grounded only in retrieved log evidence.

## License

MIT
