# NON-FUNCTIONAL REQUIREMENTS

## Performance
- NFR-PERF-001: Summary generation <15s for <=5000 words (95% of requests).
- NFR-PERF-002: Search query top-20 results <=2s.

## Scalability
- NFR-SCAL-001: Horizontal scaling for API and workers.
- NFR-SCAL-002: Support 10k concurrent users in Year 1 via autoscaling.

## Availability
- NFR-AVAIL-001: Core features availability >= 99.9% monthly.
- NFR-AVAIL-002: Graceful degradation and fallback activation on AI outages.

## Reliability
- NFR-REL-001: Transactional storage for assignments and state changes.
- NFR-REL-002: Retries and dead-letter queues for background jobs.

## Security
- NFR-SEC-001: TLS 1.2+ for data in transit.
- NFR-SEC-002: Encryption at rest for customer data.
- NFR-SEC-003: Role-based access control and admin controls.
- NFR-SEC-004: Sensitive operation logging and restricted access.

## Privacy & Compliance
- NFR-PRIV-001: Consent workflows and PII redaction support.
- NFR-PRIV-002: GDPR/CCPA deletion and export flows.

## Usability
- NFR-UX-001: Onboard users in under 3 minutes via guided tour.
- NFR-UX-002: Editable summaries and explainability features.

## Accessibility
- NFR-ACC-001: WCAG 2.1 AA for core flows.
- NFR-ACC-002: Screen-reader compatibility and keyboard navigation.

## Maintainability
- NFR-MNT-001: Modular architecture and documented APIs.
- NFR-MNT-002: Automated tests for critical paths.

## Portability
- NFR-PORT-001: Dockerized services deployable to major clouds.

## Logging & Monitoring
- NFR-LOG-001: Centralized structured logging with retention.
- NFR-MON-001: Instrumentation for latency and error metrics.
- NFR-ALERT-001: Alerts for degradation, queue backlogs, and AI failures.

## Backup & Recovery
- NFR-BKR-001: Daily DB snapshots; RPO <=24h; RTO <=4h for core services.
- NFR-BKR-002: Disaster recovery runbook and drills.

## Browser Compatibility
- NFR-BROWSE-001: Support latest two versions of Chrome, Firefox, Edge, Safari.

## Compliance (Enterprise)
- NFR-COMP-001: Exportable audit logs; retention policy enforcement.
- NFR-COMP-002: Plan for SOC2 readiness in post-MVP phases.

(End of Non-Functional Requirements)
