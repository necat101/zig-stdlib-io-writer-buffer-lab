#!/usr/bin/env python3
"""Generate deterministic Zig stdlib IO buffer-contract cases."""
import json, os, pathlib, sys
random_seed = 42

ROOT = pathlib.Path(__file__).parent
CASES_DIR = ROOT / "generated_cases"
CASES_DIR.mkdir(exist_ok=True)

cases = [
    {"id": "c01_local_zig_version_marker", "category": "version_probe", "purpose": "zig version probe", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "hnsafety_word_context", "article_marker": "local_compiler_truth", "version_sensitive": True, "zig_source": "// version probe marker\n"},
    {"id": "c02_zig_env_std_dir_marker", "category": "version_probe", "purpose": "zig env std_dir probe", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "hnsafety_word_context", "article_marker": "local_compiler_truth", "version_sensitive": True, "zig_source": "// env probe\n"},
    {"id": "c03_std_io_namespace_probe_marker", "category": "stdlib_source_probe", "purpose": "probe std.Io namespace existence", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "api_contract", "article_marker": "io_interface_context", "version_sensitive": True},
    {"id": "c04_std_io_reader_exists_marker", "category": "stdlib_source_probe", "purpose": "std.Io.Reader exists", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "api_contract", "article_marker": "io_interface_context", "version_sensitive": True},
    {"id": "c05_std_io_writer_exists_marker", "category": "stdlib_source_probe", "purpose": "std.Io.Writer exists", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "api_contract", "article_marker": "io_interface_context", "version_sensitive": True},
    {"id": "c06_file_writer_buffer_signature_marker", "category": "api_shape", "purpose": "file writer buffer signature observation", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "documentation_vs_contract", "article_marker": "io_interface_context", "version_sensitive": True},
    {"id": "c07_fixed_writer_probe_marker", "category": "api_shape", "purpose": "fixed writer probe", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "api_contract", "article_marker": "writer_buffer_context", "version_sensitive": True},
    {"id": "c08_fixed_reader_probe_marker", "category": "api_shape", "purpose": "fixed reader probe", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "api_contract", "article_marker": "reader_context", "version_sensitive": True},
    {"id": "c09_writer_interface_field_marker", "category": "api_shape", "purpose": "writer interface field observation", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "api_contract", "article_marker": "io_interface_context", "version_sensitive": True},
    {"id": "c10_reader_interface_method_marker", "category": "api_shape", "purpose": "reader interface method observation", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "api_contract", "article_marker": "io_interface_context", "version_sensitive": True},
    {"id": "c11_stream_method_probe_marker", "category": "api_shape", "purpose": "stream method probe", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "api_contract", "article_marker": "stream_context", "version_sensitive": True},
    {"id": "c12_writer_flush_probe_marker", "category": "api_shape", "purpose": "writer flush probe", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "api_contract", "article_marker": "writer_buffer_context", "version_sensitive": True},
    {"id": "c13_empty_writer_buffer_marker", "category": "buffer_observation", "purpose": "empty writer buffer context", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "empty", "hn_marker": "buffer_size_leak", "article_marker": "writer_buffer_context", "version_sensitive": True},
    {"id": "c14_one_byte_writer_buffer_marker", "category": "buffer_observation", "purpose": "1-byte writer buffer", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "1_byte", "hn_marker": "buffer_size_leak", "article_marker": "writer_buffer_context", "version_sensitive": True},
    {"id": "c15_small_writer_buffer_marker", "category": "buffer_observation", "purpose": "small writer buffer (e.g. 8-64B)", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "small", "hn_marker": "buffer_size_leak", "article_marker": "writer_buffer_context", "version_sensitive": True},
    {"id": "c16_kilobyte_writer_buffer_marker", "category": "buffer_observation", "purpose": "kilobyte writer buffer", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "kilobyte", "hn_marker": "buffer_size_leak", "article_marker": "writer_buffer_context", "version_sensitive": True},
    {"id": "c17_large_writer_buffer_marker", "category": "buffer_observation", "purpose": "large writer buffer", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "large", "hn_marker": "buffer_size_leak", "article_marker": "writer_buffer_context", "version_sensitive": True},
    {"id": "c18_writer_buffer_len_visible_runtime_marker", "category": "api_shape", "purpose": "buffer len visible at runtime", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "buffer_size_leak", "article_marker": "writer_buffer_context", "version_sensitive": True},
    {"id": "c19_writer_buffer_len_not_type_contract_marker", "category": "api_shape", "purpose": "buffer len NOT in Writer type contract – HN leaky abstraction theme", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "buffer_size_leak", "article_marker": "io_interface_context", "version_sensitive": True},
    {"id": "c20_zstd_decompress_api_probe_marker", "category": "zstd_context", "purpose": "std.compress.zstd.Decompress API probe", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "bug_vs_interface", "article_marker": "zstd_context", "version_sensitive": True},
    {"id": "c21_zstd_small_buffer_context_marker", "category": "zstd_context", "purpose": "zstd with small output buffer – article context", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "small", "hn_marker": "bug_vs_interface", "article_marker": "zstd_context", "version_sensitive": True},
    {"id": "c22_zstd_larger_buffer_context_marker", "category": "zstd_context", "purpose": "zstd with larger output buffer – article context", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "large", "hn_marker": "bug_vs_interface", "article_marker": "zstd_context", "version_sensitive": True},
    {"id": "c23_zstd_assertion_context_marker", "category": "zstd_context", "purpose": "zstd assertion vs error return – HN assert/error debate", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "assert_vs_error", "article_marker": "zstd_context", "version_sensitive": True},
    {"id": "c24_debug_build_context_marker", "category": "build_mode", "purpose": "debug build context", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "hnsafety_word_context", "article_marker": "local_compiler_truth", "version_sensitive": True},
    {"id": "c25_release_safe_build_context_marker", "category": "build_mode", "purpose": "ReleaseSafe build context", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "hnsafety_word_context", "article_marker": "local_compiler_truth", "version_sensitive": True},
    {"id": "c26_compile_error_capture_marker", "category": "compile_observation", "purpose": "compile error capture", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "api_contract", "article_marker": "local_compiler_truth", "version_sensitive": True},
    {"id": "c27_api_changed_context_marker", "category": "compile_observation", "purpose": "API changed / compile_changed marker", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "pre_1_0_stdlib", "article_marker": "local_compiler_truth", "version_sensitive": True},
    {"id": "c28_docs_context_marker", "category": "docs_context", "purpose": "documentation vs API contract – HN theme", "expected_compile": "n/a", "expected_run": "n/a", "buffer_class": "n/a", "hn_marker": "documentation_vs_contract", "article_marker": "io_interface_context", "version_sensitive": False},
    {"id": "c29_hnsafety_word_context_marker", "category": "hn_context", "purpose": "HN 'unsafe' word pushback context", "expected_compile": "n/a", "expected_run": "n/a", "buffer_class": "n/a", "hn_marker": "hnsafety_word_context", "article_marker": "safety_framing", "version_sensitive": False},
    {"id": "c30_bug_vs_interface_context_marker", "category": "hn_context", "purpose": "bug vs interface design – HN theme (jmull etc)", "expected_compile": "n/a", "expected_run": "n/a", "buffer_class": "n/a", "hn_marker": "bug_vs_interface", "article_marker": "zstd_context", "version_sensitive": False},
    {"id": "c31_documentation_vs_contract_context_marker", "category": "hn_context", "purpose": "documentation vs API contract debate", "expected_compile": "n/a", "expected_run": "n/a", "buffer_class": "n/a", "hn_marker": "documentation_vs_contract", "article_marker": "io_interface_context", "version_sensitive": False},
    {"id": "c32_no_network_tls_marker", "category": "guard", "purpose": "no network / TLS – lab guard", "expected_compile": "n/a", "expected_run": "n/a", "buffer_class": "n/a", "hn_marker": "lab_scope", "article_marker": "lab_scope", "version_sensitive": False},
    {"id": "c33_no_external_zstd_payload_marker", "category": "guard", "purpose": "no external compressed payloads", "expected_compile": "n/a", "expected_run": "n/a", "buffer_class": "n/a", "hn_marker": "lab_scope", "article_marker": "lab_scope", "version_sensitive": False},
    {"id": "c34_no_fuzzing_marker", "category": "guard", "purpose": "no fuzzing frameworks", "expected_compile": "n/a", "expected_run": "n/a", "buffer_class": "n/a", "hn_marker": "lab_scope", "article_marker": "lab_scope", "version_sensitive": False},
    {"id": "c35_no_package_manager_marker", "category": "guard", "purpose": "no package manager / no zig fetch", "expected_compile": "n/a", "expected_run": "n/a", "buffer_class": "n/a", "hn_marker": "lab_scope", "article_marker": "lab_scope", "version_sensitive": False},
    {"id": "c36_no_global_safety_claim_marker", "category": "guard", "purpose": "no global safety claims – lab scope marker", "expected_compile": "n/a", "expected_run": "n/a", "buffer_class": "n/a", "hn_marker": "hnsafety_word_context", "article_marker": "lab_scope", "version_sensitive": False},
    {"id": "c37_local_compiler_truth_marker", "category": "guard", "purpose": "local compiler truth only", "expected_compile": "n/a", "expected_run": "n/a", "buffer_class": "n/a", "hn_marker": "lab_scope", "article_marker": "local_compiler_truth", "version_sensitive": False},
    {"id": "c38_production_io_policy_not_tested_marker", "category": "guard", "purpose": "production I/O policy NOT_TESTED", "expected_compile": "n/a", "expected_run": "n/a", "buffer_class": "n/a", "hn_marker": "lab_scope", "article_marker": "lab_scope", "version_sensitive": False},
    {"id": "c39_article_snippet_compile_observer", "category": "compile_observation", "purpose": "article snippet compile observer – version-sensitive", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "n/a", "hn_marker": "bug_vs_interface", "article_marker": "io_interface_context", "version_sensitive": True},
    {"id": "c40_fixed_reader_stream_small_writer_marker", "category": "buffer_observation", "purpose": "fixed_reader stream to small writer – HN buffer dependency theme", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "small", "hn_marker": "buffer_size_leak", "article_marker": "writer_buffer_context", "version_sensitive": True},
    {"id": "c41_fixed_reader_stream_large_writer_marker", "category": "buffer_observation", "purpose": "fixed_reader stream to large writer", "expected_compile": "version_dependent", "expected_run": "skip", "buffer_class": "large", "hn_marker": "buffer_size_leak", "article_marker": "writer_buffer_context", "version_sensitive": True},
]

# write cases.json
with open(ROOT / "cases.json", "w") as f:
    json.dump(cases, f, indent=2)

# generate simple Zig source stubs for each case
zig_template = """// {case_id} – {purpose}
// Category: {category}
// HN marker: {hn_marker}
// Article marker: {article_marker}
// Buffer class: {buffer_class}
// This is a correctness lab stub – real stdlib API usage is version-sensitive.
// Local Zig compiler validation required – do not assume API stability.
//
// No network, no TLS, no external payloads, no fuzzing.
// No global safety claims – local compiler truth only.

const std = @import("std");

pub fn main() !void {{
    // Case: {case_id}
    // Purpose: {purpose}
    // If std.Io.Reader/Writer API shape has changed in your local Zig version,
    // this file may need updating – that is expected and is recorded as api_changed.
    _ = std;
}}
"""

for case in cases:
    path = CASES_DIR / f"{case['id']}.zig"
    fmt = dict(case)
    fmt["case_id"] = case["id"]
    # ensure all template keys exist
    for k in ["purpose","category","hn_marker","article_marker","buffer_class"]:
        fmt.setdefault(k, "n/a")
    content = zig_template.format(**fmt)
    path.write_text(content)
    case["generated_zig_path"] = f"generated_cases/{case['id']}.zig"
    case["zig_source_bytes"] = len(content.encode())

# rewrite cases.json with paths
with open(ROOT / "cases.json", "w") as f:
    json.dump(cases, f, indent=2)

print(f"Generated {len(cases)} cases in {CASES_DIR}")
print(f"cases.json written")
