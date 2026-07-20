# Common Tasks

Generic how-tos for the AMA tree. No client-specific steps.

## Create a new skill

```bash
mkdir -p .opencode/skills/<theme>/<name>
cat > .opencode/skills/<theme>/<name>/SKILL.md <<'EOF'
---
name: <name>
description: <one-line, when to use>
model: <model>
permission:
  read: [".opencode/skills/**"]
  write: []
---

# <Name>

<What this skill does, generically.>
EOF
```

## Run the development loop

`/complete-development <req-id>` walks: clarify → specify → architect →
implement → test → secure → tag.

## Audit for leaks

```bash
# flag uppercase codename / agency domain / internal host markers
grep -rEn "(?<![a-z])PROPRIETARY_TOKEN|consultancy\.example\.com|europa\.example" .opencode
```

Any hit means scrub before commit.
