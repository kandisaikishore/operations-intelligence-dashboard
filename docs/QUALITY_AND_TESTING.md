# Development, Integration Testing, and Operations Guide

The repository describes a Java 17 API, Python analysis service, PostgreSQL, and Docker Compose. Use the actual Compose file and service manifests to confirm service names, ports, commands, and health checks.

## Local setup

```bash
git clone https://github.com/kandisaikishore/operations-intelligence-dashboard.git
cd operations-intelligence-dashboard
```

Inspect the Compose file and service manifests before starting dependencies. Configure local environment variables and database credentials outside version control. Use isolated test data rather than production records.

## Service-boundary testing

For implemented endpoints and service calls, test:
- Valid and invalid request bodies
- Missing resources and unauthorized requests
- PostgreSQL unavailable, query failures, and transaction rollback
- Python analysis timeout, malformed output, and unavailable dependency
- Consistent error shape and appropriate HTTP status codes
- Correlation ID propagation across services, where supported

Avoid returning stack traces, SQL details, credentials, or internal connection strings to clients. Add request IDs to logs to correlate a single request across the Java and Python services.

## Database and migrations

Test migrations on an empty test database and on a representative previous schema when migrations exist. Verify rollback behavior and prevent partial updates. Never run destructive integration tests against production.

## Docker and health checks

Use the repository's declared Compose configuration to start the local stack. Verify each service's health endpoint or documented readiness behavior, inspect logs for startup failures, and tear down the test stack when finished. Do not report successful deployment merely because a container builds.

## Pull-request checklist

- [ ] Run the Java and Python checks defined by their manifests.
- [ ] Test API and service failure paths with mocks or isolated services.
- [ ] Verify database changes and migration behavior where applicable.
- [ ] Record which integration checks ran and which did not.
- [ ] Avoid exposing secrets or sensitive operational data in logs.
