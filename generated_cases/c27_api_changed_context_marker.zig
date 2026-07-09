// c27_api_changed_context_marker – API changed / compile_changed marker
// Category: compile_observation
// HN marker: pre_1_0_stdlib
// Article marker: local_compiler_truth
// Buffer class: n/a
// This is a correctness lab stub – real stdlib API usage is version-sensitive.
// Local Zig compiler validation required – do not assume API stability.
//
// No network, no TLS, no external payloads, no fuzzing.
// No global safety claims – local compiler truth only.

const std = @import("std");

pub fn main() !void {
    // Case: c27_api_changed_context_marker
    // Purpose: API changed / compile_changed marker
    // If std.Io.Reader/Writer API shape has changed in your local Zig version,
    // this file may need updating – that is expected and is recorded as api_changed.
    _ = std;
}
