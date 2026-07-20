# Example Project: the-project Portal

> This is an **example/template** project. Every name, system, and
> identifier below is fictional. Copy this folder, replace the
> placeholders, and you have a starting point for your own engagement.

## What it is

A generic internal portal for `the-project` (a fictional org). It exposes a
small REST API, a frontend, and integrates with a messaging bus.

## Tech estate (example)

- Backend: Java 21 + Spring Boot (see `skills/engineering/backend/`).
- Frontend: React + TypeScript (see `skills/engineering/frontend/`).
- Messaging: Kafka (see `skills/engineering/backend/kafka-the-project`).
- Store: PostgreSQL (see `skills/engineering/backend/postgresql`).

## Layout

```
portal/
├── engineering/backend/      # Spring Boot services
├── engineering/frontend/     # React app
└── infra/        # IaC, CI
```

## Notes

- No real client, person, or hostname appears here.
- Swap `the-project` for your org and the example systems for your own.
