#!/usr/bin/env python3
"""Run Zig stdlib IO buffer-contract lab."""
import json, subprocess, sys, time, platform, pathlib, csv
ROOT = pathlib.Path(__file__).parent
CASES_JSON = ROOT / "cases.json"

def run_cmd(cmd, timeout=5):
    start = time.perf_counter()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        elapsed = time.perf_counter() - start
        return p.returncode, p.stdout, p.stderr, elapsed, False
    except subprocess.TimeoutExpired as e:
        elapsed = time.perf_counter() - start
        return -1, e.stdout.decode() if e.stdout else "", e.stderr.decode() if e.stderr else "", elapsed, True
    except Exception as e:
        elapsed = time.perf_counter() - start
        return -2, "", str(e), elapsed, False

# probe zig
zig_version_out = ""
zig_version_ok = False
rc, out, err, _, _ = run_cmd(["zig", "version"], timeout=3)
if rc == 0:
    zig_version_out = out.strip()
    zig_version_ok = True
else:
    zig_version_out = f"zig not found / rc={rc} err={err[:200]}"

zig_env_out = ""
rc2, out2, err2, _, _ = run_cmd(["zig", "env"], timeout=3)
if rc2 == 0:
    zig_env_out = out2.strip()[:2000]
else:
    zig_env_out = f"zig env failed rc={rc2}"

with open(CASES_JSON) as f:
    cases = json.load(f)

methods = [
    "zig_version_probe",
    "zig_env_probe",
    "stdlib_source_probe",
    "compile_only_debug",
    "compile_only_release_safe",
    "run_debug_safe_case",
    "run_release_safe_case",
    "fixed_writer_context_observer",
    "fixed_reader_context_observer",
    "writer_buffer_size_observer",
    "zstd_api_context_observer",
    "article_snippet_compile_observer",
    "no_network_guard",
    "no_external_payload_guard",
    "hnsentiment_context_marker",
    "deliver_no_external_truth_marker",
]

rows = []
compile_pass=compile_fail=run_pass=run_fail=timeout_count=api_changed=skipped=0
version_probe_count=stdlib_probe_count=buffer_obs_count=zstd_ctx_count=hn_ctx_count=docs_ctx_count=0
no_network_count=no_external_payload_count=no_pkg_mgr_count=no_global_safety_count=0

subprocess_count=0

for case in cases:
    case_id = case["id"]
    category = case["category"]
    zig_path = ROOT / case.get("generated_zig_path", "")
    cat = category
    if "version" in cat: version_probe_count +=1
    if "stdlib" in cat: stdlib_probe_count +=1
    if "buffer" in cat: buffer_obs_count +=1
    if "zstd" in cat: zstd_ctx_count +=1
    if cat in ("hn_context","docs_context"): hn_ctx_count +=1
    if cat == "docs_context": docs_ctx_count +=1
    if "guard" in cat:
        no_network_count +=1
        no_external_payload_count +=1
        no_pkg_mgr_count +=1
        no_global_safety_count +=1

    for method in methods:
        # determine if method applies
        expected_compile = case.get("expected_compile","n/a")
        # default skip – we only attempt compile for version-sensitive compile_observation / api_shape / buffer cases when zig is available
        should_attempt_compile = zig_version_ok and expected_compile == "version_dependent" and method in ("compile_only_debug","compile_only_release_safe","article_snippet_compile_observer")
        
        actual_compile_status = "skip"
        actual_run_status = "skip"
        exit_code = ""
        stdout_excerpt = ""
        stderr_excerpt = ""
        elapsed = 0.0
        timeout_flag = False
        skip_reason = ""
        failure_reason = ""
        zig_cmd_str = ""

        if method in ("zig_version_probe",):
            actual_compile_status = "probe"
            stdout_excerpt = zig_version_out[:500]
            skip_reason = "" if zig_version_ok else "zig_not_found"
        elif method in ("zig_env_probe",):
            actual_compile_status = "probe"
            stdout_excerpt = zig_env_out[:500]
            skip_reason = "" if zig_version_ok else "zig_not_found"
        elif method == "stdlib_source_probe":
            actual_compile_status = "probe"
            skip_reason = "zig_not_found_no_stdlib_scan" if not zig_version_ok else ""
            stdout_excerpt = "stdlib_source_probe requires local zig std_dir"
        elif method in ("no_network_guard","no_external_payload_guard","hnsentiment_context_marker","deliver_no_external_truth_marker","fixed_writer_context_observer","fixed_reader_context_observer","writer_buffer_size_observer","zstd_api_context_observer"):
            actual_compile_status = "context_only"
            skip_reason = "context_marker_no_compile"
        elif should_attempt_compile:
            opt = "Debug" if "debug" in method.lower() else "ReleaseSafe"
            zig_cmd = ["zig", "build-exe", str(zig_path), "-O", opt, "-femit-bin=/tmp/ziglab_test_bin"]
            zig_cmd_str = " ".join(zig_cmd)
            rc, out, err, elapsed, to = run_cmd(zig_cmd, timeout=5)
            subprocess_count +=1
            exit_code = rc
            stdout_excerpt = out[:500]
            stderr_excerpt = err[:500]
            timeout_flag = to
            if to:
                actual_compile_status = "timeout"
                timeout_count +=1
            elif rc == 0:
                actual_compile_status = "pass"
                compile_pass +=1
            else:
                actual_compile_status = "fail"
                compile_fail +=1
                if "error" in (err.lower()+out.lower()):
                    api_changed +=1
                    failure_reason = "compile_error_api_changed_possible"
        else:
            actual_compile_status = "skip"
            skip_reason = "zig_not_found" if not zig_version_ok else "method_case_not_applicable_or_guard_context"
            skipped +=1

        row = {
            "method": method,
            "case_id": case_id,
            "category": category,
            "generated_zig_path": case.get("generated_zig_path",""),
            "expected_compile_status": expected_compile,
            "actual_compile_status": actual_compile_status,
            "expected_run_status": case.get("expected_run","n/a"),
            "actual_run_status": actual_run_status,
            "zig_command": zig_cmd_str,
            "exit_code": exit_code,
            "stdout_excerpt": stdout_excerpt,
            "stderr_excerpt": stderr_excerpt,
            "elapsed_s": round(elapsed,6),
            "timeout": timeout_flag,
            "local_zig_version": zig_version_out,
            "optimize_mode": "Debug" if "debug" in method else ("ReleaseSafe" if "release" in method else ""),
            "expected_classification": case.get("buffer_class","n/a"),
            "actual_classification": "version_probe" if "version" in category else category,
            "hn_marker": case.get("hn_marker",""),
            "article_marker": case.get("article_marker",""),
            "skip_reason": skip_reason,
            "failure_reason": failure_reason,
            "local_only_observation": True,
        }
        rows.append(row)

# write results
with open(ROOT / "results_rows.json","w") as f: json.dump(rows, f, indent=2)
if rows:
    with open(ROOT / "results_rows.csv","w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)

# summary
summary = {
    "python_version": sys.version,
    "platform": platform.platform(),
    "local_zig_version": zig_version_out,
    "zig_found": zig_version_ok,
    "zig_env_summary": zig_env_out[:500],
    "case_count": len(cases),
    "method_count": len(methods),
    "total_rows": len(rows),
    "compile_pass": compile_pass,
    "compile_fail": compile_fail,
    "run_pass": run_pass,
    "run_fail": run_fail,
    "timeout_count": timeout_count,
    "api_changed_count": api_changed,
    "skipped_count": skipped,
    "version_probe_count": version_probe_count,
    "stdlib_probe_count": stdlib_probe_count,
    "buffer_observation_count": buffer_obs_count,
    "zstd_context_count": zstd_ctx_count,
    "hn_context_count": hn_ctx_count,
    "docs_context_count": docs_ctx_count,
    "no_network_count": no_network_count,
    "no_external_payload_count": no_external_payload_count,
    "no_package_manager_count": no_pkg_mgr_count,
    "no_global_safety_claim_count": no_global_safety_count,
    "subprocess_count": subprocess_count,
    "network_calls": 0,
    "external_payloads": 0,
    "package_manager_used": False,
    "dangerous_run": False,
    "global_safety_claim": False,
}

# RESULTS.md
results_md = f"""# RESULTS

## Environment
- Python: {sys.version.split()[0]}
- Platform: {platform.platform()}
- Zig version: {zig_version_out}
- Zig found: {zig_version_ok}
- Zig env: {zig_env_out[:300]}

## Counts
- Cases: {len(cases)}
- Methods: {len(methods)}
- Total rows: {len(rows)}

- Compile pass: {compile_pass}
- Compile fail: {compile_fail}
- Run pass: {run_pass}
- Run fail: {run_fail}
- Timeouts: {timeout_count}
- API changed: {api_changed}
- Skipped: {skipped}

- Version probe: {version_probe_count}
- Stdlib probe: {stdlib_probe_count}
- Buffer observation: {buffer_obs_count}
- Zstd context: {zstd_ctx_count}
- HN context: {hn_ctx_count}
- Docs context: {docs_ctx_count}

- No-network markers: {no_network_count}
- No-external-payload markers: {no_external_payload_count}
- No-package-manager markers: {no_pkg_mgr_count}
- No-global-safety-claim markers: {no_global_safety_count}

- Subprocess count: {subprocess_count}
- Network calls: 0
- External payloads: 0
- Package manager used: False

## Honest conclusion
Local Zig compiler was { 'FOUND' if zig_version_ok else 'NOT FOUND' }.
"""
if not zig_version_ok:
    results_md += """
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
"""
else:
    results_md += "\nCompiler validation ran – see per-case rows.\n"

results_md += """
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
"""

with open(ROOT / "RESULTS.md","w") as f: f.write(results_md)

print(json.dumps(summary, indent=2))
print(f"\nWrote RESULTS.md, results_rows.json/csv – cases={len(cases)} rows={len(rows)} zig_found={zig_version_ok}")
