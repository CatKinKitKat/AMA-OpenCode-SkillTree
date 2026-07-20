# Shell command injection notes

Session finding: a common repo pattern used `execSync()` with template-string shell commands built from user-controlled path or URL fragments.

Observed safe-vs-unsafe split:
- Unsafe: `execSync(`git clone --depth 1 ${repo_url} "${target_dir}"`)`
- Unsafe: `execSync(command)` where `command` was assembled from `codemod`, `source`, and `--jscodeshift` options
- Unsafe: shell metacharacters in path segments such as `$(...)`, `` `...` ``, and `;` survived URL parsing or CLI argument flow and reached the shell intact

Rule of thumb:
- Treat `execSync(string)` as shell injection-prone unless every interpolated value is allowlisted and escaped
- Prefer `execFile`, `spawn`, or `execFileSync` with argv arrays
- For repo/security review, trace input origin to the exact shell boundary, not just to a string builder

Quick checks:
- Search for `execSync(`, `exec(`, `spawn(..., { shell: true })`
- Inspect any template literal that includes a URL, path, branch, codemod name, or option bag
- Confirm whether the input can carry shell metacharacters after parsing/normalization
