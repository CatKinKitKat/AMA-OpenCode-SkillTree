# Know-How (example)

Generic lessons for the example the-project portal. Nothing client-specific.

## Gotchas

- Kafka topic names need a prefix ACL or they collide.
- Postgres connection pools: size them, don't guess.
- Frontend: validate on the server too, never trust the client.

## Patterns

- CQRS-lite: write path separate from read path.
- Outbox pattern for reliable event publishing.

See `skills/` for the reusable versions of these.
