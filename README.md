# DevOps Failure Intelligence Platform (DFIP)

[![CI](https://github.com/saikishore2410/operations-intelligence-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/saikishore2410/operations-intelligence-dashboard/actions/workflows/ci.yml) ![Java](https://img.shields.io/badge/Java-17-orange) ![Python](https://img.shields.io/badge/Python-3.11-blue) ![License](https://img.shields.io/badge/License-MIT-green)

**Turn failed CI/CD runs into actionable, evidence-backed fixes.**

## Live Demo

**Deployment URL:** Not verified yet. Add a public URL here once the dashboard service is deployed and checked.

## Problem and solution

CI failures produce noisy logs and repeated investigations. DFIP classifies common failure types, shows matching evidence, recommends safe next steps, stores incidents, and exposes analytics. Deterministic rules remain the classification source; optional LLM explanations provide a grounded narrative without replacing the diagnosis.

## Features

- Classifies dependency, test, build/compilation, Docker, network and unknown failures.
- Returns matching log evidence, confidence, recommended actions and human-review routing.
- Persists incidents with repository/run ID deduplication.
- Incident history: `GET /api/v1/incidents?limit=50` (maximum 200).
- Analytics: `GET /api/v1/analytics` (totals, review count, average confidence, category counts and 30-day trend).
- Responsive dashboard at `http://localhost:8080/` with incident KPIs, 30-day activity, category distribution, recent incidents and a manual log-analysis form.
- Optional LLM explanation grounded in the deterministic diagnosis and redacted log text.
- GitHub Actions CI tests for Python and Java; Docker Compose for local orchestration.

## Architecture

```text
Client / GitHub Actions
       |
       v
Spring Boot API ------> PostgreSQL incident history
       |
       +--------------> Python FastAPI analyzer
                              |-- deterministic classification
                              |-- secret redaction
                              +-- optional OpenAI-compatible LLM explanation
```

## Quick start

```bash
docker compose up --build
```

- Dashboard: http://localhost:8080/
- Analyzer docs: http://localhost:8001/docs
- API health: http://localhost:8080/api/v1/health
- Actuator health: http://localhost:8080/actuator/health
- Incident history: http://localhost:8080/api/v1/incidents
- Analytics: http://localhost:8080/api/v1/analytics

## Optional LLM explanations

The analyzer works without an LLM key. To enable the optional explanation endpoint, set these variables before starting Compose:

```bash
export LLM_API_KEY="your-provider-key"
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL="gpt-4o-mini"
docker compose up --build
```

Call `POST http://localhost:8001/explain` with `log_text` and the `diagnosis` object returned by `/analyze`. Common bearer tokens, API keys, passwords, GitHub tokens and OpenAI-style keys are redacted before forwarding text. Redaction is best-effort, not a guarantee; never submit secrets or sensitive production logs. Without a key, `/explain` returns HTTP 503 and deterministic analysis still works.

## Analyze a failure

```bash
curl -X POST http://localhost:8001/analyze -H "Content-Type: application/json" \
  -d '{"repository":"demo/service","run_id":"123","log_text":"[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin"}'
```

## Tests

```bash
cd services/analyzer
pip install -r requirements.txt
pytest -q
cd ../api
mvn test
```

## Safety and limitations

- Diagnosis is advisory. Do not auto-rerun or alter production deployments based only on generated advice.
- Unknown errors require human review.
- LLM explanations can be inaccurate; deterministic classification and evidence remain available.
- Signed GitHub webhook ingestion and authenticated automatic log retrieval are not implemented yet.
- Set a strong `POSTGRES_PASSWORD` for shared or deployed environments; the default is for local development only.

## Roadmap

1. Signed GitHub webhook ingestion and least-privilege permissions.
2. Secret scanning/redaction before persistence and LLM calls.
3. Deploy with managed PostgreSQL, TLS, authentication and a secret manager.
4. Add evaluation datasets and regression thresholds to measure classification accuracy.
5. Add verified recovery outcomes and operational SLO tracking.

## License

MIT