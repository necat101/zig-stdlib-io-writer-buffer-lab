// c32_no_network_tls_marker – no network / TLS – lab guard
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
    // Case: c32_no_network_tls_marker
    // Purpose: no network / TLS – lab guard
    // If std.Io.Reader/Writer API shape has changed in your local Zig version,
    // this file may need updating – that is expected and is recorded as api_changed.
    _ = std;
}
