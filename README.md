# AMA: Amaro's Master Archive

Yeah, another agent repo. Sue me.

AMA is a public, client-neutral **shared skill & agent tree** for
OpenCode. Reusable AI agent definitions, skills, slash-commands, and
documentation templates. All of it meant to be owned by the community:
no proprietary code, no client names, no internal hostnames, no secrets.
I'm the guy who stuffs it in here so the legacy jungle stops fighting back.

## What's inside

```
AMA-OpenCode-SkillTree/
├── .opencode/
│   ├── AGENTS.md            # agent guidance (project instructions)
│   ├── COMPLIANCE.md        # license compliance requirements + audit policy
│   ├── opencode.json        # project config (permissions for optional MCP servers)
│   ├── agents/             # specialized agents (security, engineering, operations, ...)
│   ├── skills/             # reusable SKILL.md files — by corporate division
│   │   ├── engineering/    # backend(310), frontend(4), data-ai(20), devtooling(600)
│   │   ├── security/       # offensive(773), compliance(26), defensive(3)
│   │   ├── infrastructure/ # systems(11), cloud(2)
│   │   ├── governance/     # methodology(32), requirements(6)
│   │   ├── research/       # intelligence(73), media(14)
│   │   ├── operations/     # github(9), product(15)
│   │   └── CATALOG.md      # full skill catalog with area descriptions
│   ├── commands/           # slash commands (complete-development, security-audit, ...)
│   ├── hooks/              # git hooks (skill lint, cleanup)
│   └── docs/               # generic templates + example requirement workflows
├── README.md
├── LICENSE                 # GNU Affero General Public License v3 (AGPL-3.0)
└── .gitignore
```

### Agents (`agents/`)
35 specialized subagents with OpenCode frontmatter.
Covers backend/frontend architects, security defenders, pentest operators,
test suites, product owner, and a skill-tree curator.

### Skills (`skills/`)
Drop-in `SKILL.md` files, organized by corporate division > area:

```
skills/
├── engineering/
│   ├── backend/          # Java, Spring, Go, Python, databases, APIs, finance
│   ├── frontend/         # React, TypeScript, UI frameworks
│   ├── data-ai/          # ML, PyTorch, evaluation, audiocraft
│   └── devtooling/       # CI/CD, agents, testing, Docker, Git, MCP
├── security/
│   ├── offensive/        # pentest, red team, AD attacks, network recon
│   ├── compliance/       # SOC2, ISO27001, GDPR, FDA, quality
│   └── defensive/        # ZTNA, SIEM, runtime testing, supply-chain
├── infrastructure/
│   ├── systems/          # Linux, macOS, terminal, packages
│   └── cloud/            # AWS, Azure architecture
├── governance/
│   ├── methodology/      # planning, debugging, code review, verification
│   └── requirements/     # specification, clarification, validation
├── research/
│   ├── intelligence/     # deep research, OSINT, competitive analysis
│   └── media/            # creative visual, content, STE100 writing
└── operations/
    ├── github/           # repo management, kanban, issues, CI
    └── product/          # product management, marketing, career
```

Honestly the governance/requirements set is the part I'm proudest of,
don't tell the others. Steal whatever's useful.

### Commands (`commands/`)
- `/complete-development <req-id>`: full clarify → specify → architect →
  implement → test → secure → tag loop.
- `/curate-skills [theme]`: browse and manage the skill catalog.
- `/generate-docs`: generate documentation from the docs tree.
- `/init-skill <theme> <name>`: scaffold a new OpenCode skill from AMA template.
- `/security-audit [path-or-domain]`: audit the codebase across security domains.
- `/triage-incident`: emergency incident triage.

## Using AMA with OpenCode

OpenCode auto-discovers `.opencode/` vendors from the project root, so
just open the folder:

```bash
opencode                       # launch the TUI in this directory
# or
opencode run "use the backend-architect agent to design feature X"
```

Want AMA everywhere (all your projects)? Copy or symlink `.opencode/`
into `~/.config/opencode/`. Begone, pesky per-project setup.

## Contributing

PRs are welcome: new agents, skills, commands, or improved docs.
**Rule of the repo:** keep it client-neutral and openly licensable. Spot a
real identifier that slipped through? Generify it. I take the engineering
seriously. The rest is just for fun.

## License

Licensed under the **GNU Affero General Public License v3 (AGPL-3.0)**,
the most copyleft FOSS license there is. If you run a modified version
of this tree as a service over a network, you must publish your
modified source under the same license. That's the whole point: keep
it free for everyone, always.

Full text: [./LICENSE](./LICENSE). SPDX: `AGPL-3.0-or-later`.

Steal it, fork it, ship it, improve it, and feed the improvements back.
That's the deal. No ego, no secrets.
