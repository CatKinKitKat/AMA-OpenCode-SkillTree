# AMA Docs

This folder holds **generic, example-only** documentation for the AMA
(OpenCode Skill & Agent Tree). Nothing here references a real client,
person, hostname, or contract. Use it as a template: copy a folder,
replace the placeholders (`EXAMPLE`, `the-project`, `example.com`), and you have
a starting point for your own engagement.

## Layout

- `guides/`: getting-started + common-tasks for working in this repo.
- `projects/`: one folder per **example** project. Every file is a
  anonymized template (`_TEMPLATE.md` is the blank starting point).
- `requirements/`: example requirement lifecycle folders (clarify →
  specify → architect → implement → test → secure → tag).
- `architecture/`: generic architecture notes + an example Kafka/AVRO
  schema set.
- `rules/`: the business-rule catalog (generic).

## Rule of thumb

If a doc names a real org, person, or system, it does not belong here.
Scrub it before it lands.
