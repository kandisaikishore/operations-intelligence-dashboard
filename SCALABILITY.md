# Scalability and capacity plan

## Service boundaries
The repository contains Java and Python service components with database/container infrastructure. Keep service contracts explicit and avoid synchronous fan-out across every dashboard request.

## Data path
- Paginate and filter API results at the database/service boundary.
- Move expensive analysis and report generation to bounded background workers.
- Use database connection pools with a per-replica connection budget.
- Add indexes based on measured query plans; avoid indexing every field.
- Use bounded HTTP client pools, connection/read timeouts, and retries only for idempotent transient failures.
- Propagate correlation IDs between Java API, Python analyzer, and database operations.

## Operations
Track per-service request rate, p95/p99 latency, error rate, CPU/memory, DB pool wait, analysis queue depth, worker duration, and dependency failures. Define independent readiness checks for each service and a deployment order compatible with schema migrations.

## Load validation
Test dashboard reads, concurrent analysis jobs, large inputs, database saturation, downstream timeouts, and worker restart/recovery. Record the environment and dataset used.

## Release gates
- [ ] Service contracts and schema migrations are versioned.
- [ ] Worker concurrency and queue backpressure are configured.
- [ ] Integration tests cover downstream failures.
- [ ] Backup/restore and rollback are rehearsed.
- [ ] Load-test results support any replica or pool-size increase.

No live load test is claimed.
