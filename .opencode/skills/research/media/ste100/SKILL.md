---
name: ste100
description: Apply ASD-STE100 Issue 9 (Simplified Technical English), modified flavored version, to all repo text. Use when writing or editing docs, skills, agent prompts, or READMEs in this tree.
---

# STE100: ASD-STE100 Issue 9 (Simplified Technical English)

Enforce ASD-STE100 Issue 9 as the writing standard for every text file in
this repository. Adapted from woosal1337's "the cure for AI slop" (ep01),
which forked and explained the standard for AI-generated docs. Original
source: https://github.com/woosal1337/blog (videos/ep01-the-cure-for-ai-slop).
Attribution retained. License of this skill node: AGPL-3.0 (matches repo).

This is the **modified flavored version**: the mechanical slop-removal rules
apply always, but the strict dictionary lockdown and hard length caps are
relaxed so the text keeps enough range to read naturally. There is no
strict/flavored switch: this flavored form is the only mode.

## When to use

- Writing or editing any `.md`, `.adoc`, `.txt`, `.rst`, `.org` file here.
- Authoring agent prompts, skill files, or command docs.
- Reviewing PRs that touch prose.

## Hard rules (mechanical, always apply)

1. **No em-dashes (: ).** Replace with `: ` or a new sentence. The repo
   owner sweeps with `re.sub(r'\s*\u2014\s*', ': ', text)` before publish.
2. **No semicolons in prose.** Split into two sentences. Capitalize the
   first word after the split.
3. **No contractions.** `do not` not `don't`, `it is` not `it's`.
4. **One idea per sentence.** Short, direct, active voice preferred.
   Long sentences are kept only when they read better. There is no hard
   word cap.

## Slop to avoid (from woosal1337)

- Banned words: leverage, utilize, seamless, robust, actionable, synergy,
  deep-dive, cutting-edge, best-in-class, empower, supercharge, unlock,
  elevate, streamline.
- Phrasal fixes: reach out -> contact, set up -> create, spin up -> start,
  circle back -> return, ramp up -> increase.
- No corporate-speak, no buzzword salads, no LinkedIn-influencer energy.

## Checker

Run `scripts/ste-lint.py` on a file or directory. It reports violations
(em-dash count, long sentences, passive, contractions, banned words). Use
it to verify before committing prose changes.

## Reference

- ASD-STE100 Issue 9, ASD, 2025-01-15.
- woosal1337/blog ep01 "the cure for AI slop" (forked source of this skill).

Note: the original two-mode form (strict + flavored) was dropped. The
strict mode is gone. The modified flavored version, with em-dash removal
added, is the standing standard.
