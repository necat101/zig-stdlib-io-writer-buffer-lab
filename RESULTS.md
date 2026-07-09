# RESULTS

## Environment
- Python: 3.12.3
- Platform: Linux-6.17.0-1009-aws-x86_64-with-glibc2.39
- Zig version: zig not found / rc=-2 err=[Errno 2] No such file or directory: 'zig'
- Zig found: False
- Zig env: zig env failed rc=-2

## Counts
- Cases: 41
- Methods: 16
- Total rows: 656

- Compile pass: 0
- Compile fail: 0
- Run pass: 0
- Run fail: 0
- Timeouts: 0
- API changed: 0
- Skipped: 205

- Version probe: 2
- Stdlib probe: 3
- Buffer observation: 7
- Zstd context: 4
- HN context: 4
- Docs context: 1

- No-network markers: 7
- No-external-payload markers: 7
- No-package-manager markers: 7
- No-global-safety-claim markers: 7

- Subprocess count: 0
- Network calls: 0
- External payloads: 0
- Package manager used: False

## Honest conclusion
Local Zig compiler was NOT FOUND.

Compiler validation could NOT run – zig binary not present in PATH.
All compile/run rows are marked skip with skip_reason=zig_not_found.
This is an honest skip, not a fake result.

The lab still provides:
- deterministic generated Zig case stubs (41 cases)
- HN thread evidence artifacts
- API-shape observation markers
- version-probe scaffolding ready for a local Zig install

Do NOT claim Zig IO is safe/unsafe based on this skipped run.
Do NOT claim the article is right/wrong – no local compiler evidence was collected.

## Artifacts
- cases.json
- generated_cases/*.zig
- results_rows.json
- results_rows.csv

## Scope guards
- No network / TLS
- No external compressed payloads
- No fuzzing
- No package manager / zig fetch
- No global safety claims
- Local compiler truth only
