// c30_bug_vs_interface_context_marker – bug vs interface design – HN theme (jmull etc)
// Category: hn_context
// HN marker: bug_vs_interface
// Article marker: zstd_context
// Buffer class: n/a
// This is a correctness lab stub – real stdlib API usage is version-sensitive.
// Local Zig compiler validation required – do not assume API stability.
//
// No network, no TLS, no external payloads, no fuzzing.
// No global safety claims – local compiler truth only.

const std = @import("std");

pub fn main() !void {
    // Case: c30_bug_vs_interface_context_marker
    // Purpose: bug vs interface design – HN theme (jmull etc)
    // If std.Io.Reader/Writer API shape has changed in your local Zig version,
    // this file may need updating – that is expected and is recorded as api_changed.
    _ = std;
}
