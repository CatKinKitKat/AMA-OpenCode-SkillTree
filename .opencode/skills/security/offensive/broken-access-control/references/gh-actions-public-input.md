# GitHub Actions public-input note

Session finding:
- Workflows triggered by `issues` or `issue_comment` with `allowed_non_write_users: "*"` expand the attack surface from authenticated repo users to public issue authors.
- If the job also exposes `GITHUB_TOKEN`, provider API keys, or a model action such as `anthropics/coding-agent-action@v1`, treat the path as privileged automation driven by untrusted input.
- Verify the effective tool surface, not just the declared wrapper. The relevant question is whether model output can reach any action outside the intended `CLAUDE_CODE_SCRIPT_CAPS` or trigger follow-on jobs.
- Audit downstream scripts for comment/label/dispatch side effects, and confirm those scripts do not accept free-form shell fragments or unsafe repo selectors.
- For model-driven actions, classify findings explicitly:
  - confirmed: public input reaches an unintended write/comment/dispatch/secret sink.
  - high-risk design: non-write users can trigger privileged automation, but wrappers/tool caps still constrain impact.
  - false lead: suspicious static asymmetry is blocked by downstream platform semantics.
- False-lead example to remember: `github-file-ops-server.ts` validated paths for `commit_files` but not `delete_files`. Local Git tree construction rejects slash-containing traversal paths such as `../evil.txt`, so this alone is not enough for a report without GitHub API proof.
- Prefix checks like `filePath.startsWith(cwd)` are still worth noting, but usually become weak/low-impact unless they let an attacker delete a meaningful in-repo path or bypass a documented boundary.