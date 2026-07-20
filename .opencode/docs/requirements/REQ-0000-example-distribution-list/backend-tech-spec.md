# Backend Tech Spec (example)

## Entities

- `DistributionList`: id, tenantId, name, recipients[].
- `Recipient`: id, email.

## API

| Method | Path         | Purpose        |
|--------|--------------|----------------|
| POST   | /lists       | create         |
| GET    | /lists/{id}  | retrieve       |
| PUT    | /lists/{id}  | update         |
| DELETE | /lists/{id}  | delete (soft)  |

## Stack

Spring Boot + JPA + Postgres. See `skills/engineering/backend/`.
