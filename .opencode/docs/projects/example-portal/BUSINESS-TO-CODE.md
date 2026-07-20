# Business to Code (example)

> Worked example of mapping a made-up requirement to code. Fictional.

## Requirement (example)

> As an the-project operator, I want to create a distribution list so that
> alerts reach the right team.

## Mapping

| Requirement concept | Code artifact              |
|---------------------|----------------------------|
| Distribution list   | `DistributionList` entity  |
| Create              | `POST /lists`              |
| Recipients          | `Recipient` child entity   |

## Notes

- This is a template. Replace with your own requirement + entities.
- Keep identifiers generic (`example.com`, `the-project`).
