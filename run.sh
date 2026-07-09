#!/usr/bin/env bash
set -euo pipefail

# zig-stdlib-io-writer-buffer-lab runner
# https://github.com/necat101/zig-stdlib-io-writer-buffer-lab

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# Find Zig binary: $ZIG_BIN > ./zig > PATH zig > common local paths
find_zig() {
  if [ -n "${ZIG_BIN:-}" ] && [ -x "$ZIG_BIN" ]; then echo "$ZIG_BIN"; return 0; fi
  if [ -x "$ROOT/zig" ]; then echo "$ROOT/zig"; return 0; fi
  if command -v zig >/dev/null 2>&1; then echo "zig"; return 0; fi
  for p in /tmp/zig-x86_64-linux-0.16.0/zig /opt/zig/zig /usr/local/bin/zig; do
    [ -x "$p" ] && echo "$p" && return 0
  done
  return 1
}

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 not found in PATH" >&2
  exit 1
fi

ZIG_BIN="$(find_zig || true)"
if [ -z "$ZIG_BIN" ]; then
  echo "warning: zig not found – compiler validation will be skipped" >&2
  echo "  install Zig 0.16.0+ from https://ziglang.org/download/" >&2
  echo "  or set ZIG_BIN=/path/to/zig" >&2
  echo
else
  echo "Using Zig: $("$ZIG_BIN" version 2>/dev/null || echo "$ZIG_BIN")"
  export ZIG_BIN
fi

echo "==> py_compile generate_cases.py run_lab.py"
python3 -m py_compile generate_cases.py run_lab.py

echo "==> generate_cases.py"
python3 generate_cases.py

# Defensive: fix Zig string literal newline bug in generated output
# (generate_cases.py has a known bug emitting real newlines inside "...")
if [ -f fix_zig_newlines.py ]; then
  echo "==> fix_zig_newlines.py generated_cases"
  python3 fix_zig_newlines.py generated_cases || true
fi

echo "==> run_lab.py"
if [ -n "${ZIG_BIN:-}" ]; then
  ZIG_BIN="$ZIG_BIN" python3 run_lab.py
else
  python3 run_lab.py
fi

echo
echo "Done."
echo "  RESULTS.md"
echo "  results_rows.json / results_rows.csv"
echo "  cases.json"
echo "  generated_cases/*.zig"
echo
echo "To verify a fresh clone:"
echo "  cat VERIFY.md"
