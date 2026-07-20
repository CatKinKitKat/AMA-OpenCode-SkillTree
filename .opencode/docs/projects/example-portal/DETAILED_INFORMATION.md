# Detailed Information (example)

Deeper notes on the example the-project portal. Fictional, anonymized.

## Services

- `gateway`: edge, auth, routing.
- `lists`: distribution list domain.
- `notifications`: sends to the bus.

## Data flow (example)

```
client -> gateway -> lists (postgres) -> notifications -> kafka -> consumers
```

## Integration contract

Events use AVRO schemas under `architecture/kafka/avro/` (example set).
Schemas are versioned. Consumers tolerate unknown fields.
