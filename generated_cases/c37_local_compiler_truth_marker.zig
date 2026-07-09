// c37_local_compiler_truth_marker – local compiler truth only
// Category: guard
// HN marker: lab_scope
// Article marker: local_compiler_truth
// Buffer class: n/a
// This is a correctness lab stub – real stdlib API usage is version-sensitive.
// Local Zig compiler validation required – do not assume API stability.
//
// No network, no TLS, no external payloads, no fuzzing.
// No global safety claims – local compiler truth only.

const std = @import("std");

pub fn main() !void {
    // Case: c37_local_compiler_truth_marker
    // Purpose: local compiler truth only
    // If std.Io.Reader/Writer API shape has changed in your local Zig version,
    // this file may need updating – that is expected and is recorded as api_changed.
    _ = std;
}
