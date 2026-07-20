# Architecture (generic)

High-level, vendor-neutral architecture notes for the example the-project
portal. No real system names.

## Layers

- **Edge:** gateway does AuthN + routing.
- **Domain:** services own their data.
- **Integration:** events on a bus (Kafka, example AVRO schemas under
  `kafka/avro/`).
- **Store:** per-service databases (Postgres example).

## Shared patterns

See `shared-patterns.md`. The Kafka section (`kafka/`) shows topic
naming, AVRO schema versioning, and a sample Java producer (generic).
