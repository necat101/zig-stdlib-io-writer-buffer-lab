// c35_no_package_manager_marker – no package manager / no zig fetch
// Category: guard
// HN marker: lab_scope
// Article marker: lab_scope
// Buffer class: n/a
// This is a correctness lab stub – real stdlib API usage is version-sensitive.
// Local Zig compiler validation required – do not assume API stability.
//
// No network, no TLS, no external payloads, no fuzzing.
// No global safety claims – local compiler truth only.

const std = @import("std");

pub fn main() !void {
    // Case: c35_no_package_manager_marker
    // Purpose: no package manager / no zig fetch
    // If std.Io.Reader/Writer API shape has changed in your local Zig version,
    // this file may need updating – that is expected and is recorded as api_changed.
    _ = std;
}
