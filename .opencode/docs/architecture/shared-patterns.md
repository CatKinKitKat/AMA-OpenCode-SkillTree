# Shared Patterns (generic)

Reusable architecture patterns, no client specifics.

## Outbox

Service writes business row + outbox row in one tx. A relay publishes
the outbox to the bus. Guarantees at-least-once delivery.

## Prefix ACLs on Kafka

Topics use a `tenant.` prefix. ACLs scope producers/consumers per
tenant. Prevents cross-tenant publish.

## Server-side trust

Never trust client input. Validate at the boundary, authorize on every
request, audit mutations.

## Schema evolution

AVRO schemas are backward-compatible. Add fields with defaults. Don't
remove required ones. Consumers tolerate unknown fields.
