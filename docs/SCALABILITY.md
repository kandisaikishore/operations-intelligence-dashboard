# Scalability baseline

Scale this project according to measured demand and its actual stack. Avoid unnecessary distributed infrastructure.

## Priorities
- Profile representative user journeys before optimizing or adding replicas.
- Bound request/input size, concurrency, retries, and resource use.
- Paginate large collections and optimize measured database/query hot paths.
- Keep service instances stateless where possible; externalize shared state before horizontal scaling.
- Add timeouts, health/readiness checks, structured logs, metrics, safe configuration, and graceful shutdown for hosted services.
- Add automated build, unit, integration, security/dependency, and deployment smoke checks appropriate to the repository.

## Capacity validation
Measure throughput, p95/p99 latency, error rate, CPU/memory, database wait time, and queue lag under normal, peak, and burst traffic.

## Release gates
- [ ] Dependency outages are handled predictably.
- [ ] Retries are bounded and state-changing operations are idempotent where needed.
- [ ] Rollback and backup/restore are documented for persistent data.
- [ ] Capacity assumptions and load-test results are recorded.

This checklist is not evidence of completed load testing or production scaling.