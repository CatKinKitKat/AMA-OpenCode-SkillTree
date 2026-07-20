# Security Architecture Review (example)

## Threats considered

- Unauthorized list creation (mitigated: operator role at gateway).
- Injected recipient emails (mitigated: server-side validation).
- IDOR on list id (mitigated: tenant scoping).

## Controls

- AuthN at gateway, AuthZ server-side.
- Input length + format validation.
- Audit log on create/delete.

This is a template. Run a real review per requirement.
