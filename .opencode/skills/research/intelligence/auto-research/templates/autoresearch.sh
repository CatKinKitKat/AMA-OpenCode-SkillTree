#!/usr/bin/env bash
set -euo pipefail

# Copy this file into the target repo as ./autoresearch.sh and replace the body.
# Emit at least one structured line:
#   METRIC duration_ms=1234
# Optional extra metrics:
#   METRIC rss_mb=512
#   METRIC accuracy=0.913

# Fast precheck first. Keep it cheap.
# Example:
# python3 -m py_compile src/*.py >/dev/null

run_once() {
  # Replace this with the real workload.
  # Print only the numeric primary metric.
  local start end duration_ms
  start=$(python3 - <<'PY'
import time
print(time.perf_counter_ns())
PY
)

  # --- workload begins ---
  "$@"
  # --- workload ends ---

  end=$(python3 - <<'PY'
import time
print(time.perf_counter_ns())
PY
)
  duration_ms=$(python3 - <<'PY' "$start" "$end"
import sys
start = int(sys.argv[1])
end = int(sys.argv[2])
print((end - start) / 1_000_000)
PY
)
  printf '%s\n' "$duration_ms"
}

# Slow workloads: one run is enough.
# primary=$(run_once your benchmark command here)

# Fast/noisy workloads: run several times and report the median.
vals=()
for _ in 1 2 3 4 5; do
  vals+=("$(run_once true)")
done
primary=$(printf '%s\n' "${vals[@]}" | python3 - <<'PY'
import statistics, sys
vals = [float(line.strip()) for line in sys.stdin if line.strip()]
print(statistics.median(vals))
PY
)

printf 'METRIC duration_ms=%s\n' "$primary"
