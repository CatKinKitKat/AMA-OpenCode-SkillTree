# Lightspark withdrawal validation default-off note

Session finding:
- `spark/so/chain/tokens/withdraw.go:422-454` validates owner signatures only when `spark.so.tokens.enforce_withdrawal_signature_validation > 0`.
- `docker/operator.config.yaml:74` and `so.template.config.yaml:84` ship that knob as `0`.
- In this state, a zeroed or otherwise invalid `OwnerSignature` can still be accepted by `HandleTokenWithdrawals` if all other checks pass.

Verification notes:
- Unit tests in `spark/so/chain/tokens/withdraw_test.go` include a happy-path case with `ownerSignature := make([]byte, 64)`.
- Local `go test` on the cloned repo hit an environment dependency gap: `exec: "atlas": executable file not found in $PATH` during DB migration setup.

Use this note when auditing withdrawal/signature flows: always verify the effective runtime knob and shipped defaults, not only the presence of a validator function or a test helper that constructs a signature payload.
