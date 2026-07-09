// c21_zstd_small_buffer_context_marker – zstd with small output buffer – article context
// Category: zstd_context
// HN marker: bug_vs_interface
// Article marker: zstd_context
// Buffer class: small
// This is a correctness lab stub – real stdlib API usage is version-sensitive.
// Local Zig compiler validation required – do not assume API stability.
//
// No network, no TLS, no external payloads, no fuzzing.
// No global safety claims – local compiler truth only.

const std = @import("std");

pub fn main() !void {
    // Case: c21_zstd_small_buffer_context_marker
    // Purpose: zstd with small output buffer – article context
    // If std.Io.Reader/Writer API shape has changed in your local Zig version,
    // this file may need updating – that is expected and is recorded as api_changed.
    _ = std;
}
