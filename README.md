# Operations Intelligence Dashboard

[![Java 17](https://img.shields.io/badge/Java-17-orange?logo=openjdk)](https://www.java.com/) [![Python 3.11](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/) [![Docker Compose](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://docs.docker.com/compose/) [![Source](https://img.shields.io/badge/Source-GitHub-181717?logo=github)](https://github.com/kandisaikishore/operations-intelligence-dashboard)

An operations-focused dashboard project with a Java API, Python analysis service, PostgreSQL, and Docker Compose. The repository is intended to bring operational signals and service information into one place; verify the current services and endpoints from the checked-in configuration before extending it.

## Project overview

- Organize operational data for easier inspection
- Provide a dashboard and API layer for service workflows
- Use container orchestration for local development
- Establish a foundation for operational analytics and observability

## Technology stack

- Java 17 / Spring Boot
- Python 3.11 / FastAPI
- PostgreSQL
- Docker Compose
- GitHub Actions

## Quick start

```bash
git clone https://github.com/kandisaikishore/operations-intelligence-dashboard.git
cd operations-intelligence-dashboard
docker compose up --build
```

Review `docker-compose.yml` and service configuration for the required environment variables and ports. Configure secrets locally and do not commit credentials. If a service fails to start, inspect the container logs with `docker compose logs --follow`.

## Repository layout

The repository includes a `services/` directory and a `docker-compose.yml` file. Consult the service folders for individual build instructions, routes, and tests.

## Validation

Run the tests documented in each service directory. Also verify that containers reach a healthy state, the dashboard loads, API error responses are understandable, and persistent data behaves as expected across restarts.

## Security and operational considerations

Before production deployment, configure authentication and authorization, secure service-to-service communication, health checks, resource limits, backup/restore, and log redaction. Do not send secrets or sensitive operational logs to external services without an approved policy.

## Contributing

Open issues with reproduction steps and relevant logs after redacting credentials. Pull requests should describe the behaviour changed and the tests performed.

## License

Review the repository's license file before reuse or redistribution.
