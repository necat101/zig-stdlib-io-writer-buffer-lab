# zig-stdlib-io-writer-buffer-lab

A tiny, reproducible, local correctness / compiler-validation lab about Zig stdlib IO buffer-contract footguns – `std.Io.Reader`, `std.Io.Writer`, writer buffer sizes, and the `std.compress.zstd.Decompress` context from the "Is Zig's new writer unsafe?" debate.

**This lab does NOT prove Zig is safe or unsafe. It validates local compiler behavior only.**

## Hacker News thread access

The Hacker News thread https://news.ycombinator.com/item?id=45313597 ("Is Zig's new writer unsafe?") was read via the Hacker News Firebase API using the bundled `hackernews` CLI **before** writing this README. See `hn_thread_evidence.md`, `hn_comments_sanitized.json`, and `hn_nodes_sanitized.json` for auditable evidence.

Do not treat the linked blog post or Zig docs alone as the source for the sentiment summary below – the summary reflects the actual HN discussion.

## What Hacker News users were actually debating

**"Unsafe" framing pushback:** Multiple commenters pushed back on calling the issue "unsafe". tialaramex: "maybe unwise but I can't see how it's unsafe ?" jmull: "just a bug … not a general safety problem". fp64: failed to convince that the new Writer was "inherently unsafe by design" – criticism was "a bug in the implementation and not a conceptual issue".

**Bug vs interface design:** jmull argued Decompress's Reader shouldn't depend on the writer buffer size passed to its stream implementation – "that's a bug in the Decompress Reader implementation. The article confuses a bug in a specific Reader implementation with a problem with the Writer interface generally. If a reader really wants to impose some chunking limitation … then it should return an error … not go into an infinite loop." thayne asked how Decompress Reader *should* be implemented correctly, noting "the API … lends itself to implementations that have this kind of bug, where they depend on the buffer being a certain size." kiitos: "the new zig io interfaces conflate behavior (read/write) with implementation (buffer size(s))".

**Leaky abstraction / buffer-size dependency:** bheadmaster: "abstraction itself is leaky – in that the length of the buffer is an implicit dependency which cannot be known from the type alone."

**Assertions vs errors:** latch agreed it's not unsafe but "still a shame that it has to be a runtime error … leaves lot of friction and edge cases", curious "why they asserted instead of erroring in the first place".

**Documentation vs API contract:** Thread theme: should buffer-size requirements be in the type system, a documented contract, or returned as runtime errors?

**Blog post vs GitHub issue:** preommr / casey2: "feels like it should've been a git issue rather than a blog post", "Who cares? seems like something for the issue tracker". Counterpoint from kaoD / flykespice / bastawhiz: writing investigation posts takes effort, blog is valid, "I don't want to post through a channel where I'll get a snide, terse response from a maintainer", Andrew Kelley's response felt dismissive to some.

**Pre-1.0 stdlib status:** fp64 noted the feature/refactor "was already advertised as complex and not fully implemented or verified". General sentiment: Zig's stdlib is evolving pre-1.0, judge accordingly.

**Zig value proposition subthread:** Significant off-topic discussion about Zig as "better C", allocators, comptime, etc. – not directly relevant to IO safety.

Andrew Kelley (Zig creator) replied on lobste.rs – link was shared in thread.

**Bottom line from HN:** the reported behavior looked like a specific decompressor Reader bug to many commenters, not a fundamental Writer unsafety. But the API design does make buffer-size requirements implicit (leaky abstraction), and assertions vs returned errors matter. Documentation alone shouldn't carry the whole burden. This lab only validates local compiler behavior instead of settling the design debate.

## Linked articles

- "Is Zig's new writer unsafe?" – https://www.openmymind.net/Is-Zigs-New-Io-Unsafe/
- "Zig's New Writer" – https://www.openmymind.net/Zigs-New-Writer/
- "I'm Too Dumb For Zig's New IO Interface" – https://www.openmymind.net/Im-Too-Dumb-For-Zigs-New-IO-Interface/
- Zig: https://ziglang.org/

The article frames the new Zig Writer/Reader APIs as possibly unsafe because a Reader can depend on a Writer buffer size that is not visible in the Writer type alone.

## Lab scope

- **DO:** local Zig compiler validation, stdlib source probing, API-shape observation, buffer-size context markers, zstd decompress API context, HN sentiment markers
- **DO NOT:** prove Zig safe/unsafe, attack Zig, run network TLS, download Zig, benchmark all I/O systems, fuzz zstd, generate malformed compressed data, claim universal stdlib conclusions, turn one blog post into a broad language verdict

## Cases (41 total)

version_probe: local_zig_version_marker, zig_env_std_dir_marker  
stdlib_source_probe: std_io_namespace_probe, std_io_reader_exists, std_io_writer_exists  
api_shape: file_writer_buffer_signature, fixed_writer_probe, fixed_reader_probe, writer_interface_field, reader_interface_method, stream_method_probe, writer_flush_probe, writer_buffer_len_visible_runtime, writer_buffer_len_not_type_contract  
buffer_observation: empty_writer_buffer, one_byte_writer_buffer, small_writer_buffer, kilobyte_writer_buffer, large_writer_buffer, fixed_reader_stream_small_writer, fixed_reader_stream_large_writer  
zstd_context: zstd_decompress_api_probe, zstd_small_buffer_context, zstd_larger_buffer_context, zstd_assertion_context  
build_mode: debug_build_context, release_safe_build_context  
compile_observation: compile_error_capture, api_changed_context, article_snippet_compile_observer  
docs/hn_context: docs_context, hnsafety_word_context, bug_vs_interface_context, documentation_vs_contract_context  
guards: no_network_tls, no_external_zstd_payload, no_fuzzing, no_package_manager, no_global_safety_claim, local_compiler_truth, production_io_policy_not_tested

## Methods

zig_version_probe, zig_env_probe, stdlib_source_probe, compile_only_debug, compile_only_release_safe, run_debug_safe_case, run_release_safe_case, fixed_writer_context_observer, fixed_reader_context_observer, writer_buffer_size_observer, zstd_api_context_observer, article_snippet_compile_observer, no_network_guard, no_external_payload_guard, hnsentiment_context_marker, deliver_no_external_truth_marker

## Running

Quick start:

**Linux / macOS:**
```bash
./run.sh
```

**Windows:**
```cmd
run.bat
```

Manual:
```bash
python3 -m py_compile generate_cases.py run_lab.py
python3 generate_cases.py
python3 fix_zig_newlines.py generated_cases   # works around a known generator bug
ZIG_BIN=/path/to/zig python3 run_lab.py
```

`run_lab.py` records Python version, platform, Zig version, zig env, case/method counts, compile/run/skip counts, timeout counts, api_changed counts, HN-thread-access status, network/package-manager guards, and whether outputs were generated.

## Results

See `RESULTS.md`, `results_rows.json`, `results_rows.csv`, `cases.json`.

**v2 (2026-07-09):** Generated Zig files are **real** stdlib API probes – `std.Io.Reader` / `Writer`, fixed buffers, `stream()`, `flush()`, buffer-size 0B/1B/64B/1KB/8KB, buffer-len type-contract check, `std.compress.zstd.Decompress` API probe, etc. – validated on Zig **0.16.0** locally.

The initial v1 commit intentionally shipped with stub Zig files and `zig_not_found` skip results to prove honest skip handling – see git history (`e6b9df2` and earlier). v2 replaces stubs with real API probes.

Do NOT claim Zig IO is safe/unsafe based on a skipped run. Do NOT claim the article is right/wrong without local compiler evidence.

## Version-specific caveats

- Uses **local zig binary only** – detected via `zig version` / `zig env`
- No downloads, no apt/brew/choco/sudo/Docker/nix/curl installers
- If Zig is missing: clear skip artifacts, no fake validation
- If local Zig version doesn't expose the exact APIs from the article: generate version-probe artifacts, mark `compile_skip` / `api_changed` with compiler errors
- API shape in `std.Io` is pre-1.0 and evolving – expect breakage across versions
- Debug vs ReleaseSafe behavior may differ
- "this compiled locally" ≠ "I understand the stdlib contract"

## Safety scope

- No network / TLS
- No external compressed payloads
- No fuzzing
- No package manager / `zig fetch`
- No global safety claims
- Local compiler truth only
- Production I/O policy NOT_TESTED

## Verify

See `VERIFY.md` for fresh-clone verification transcript.
