// c15_small_writer_buffer_marker – small writer buffer (e.g. 8-64B)
// Category: buffer_observation
// HN marker: buffer_size_leak
// Article marker: writer_buffer_context
// Buffer class: small
// This is a correctness lab stub – real stdlib API usage is version-sensitive.
// Local Zig compiler validation required – do not assume API stability.
//
// No network, no TLS, no external payloads, no fuzzing.
// No global safety claims – local compiler truth only.

const std = @import("std");

pub fn main() !void {
    // Case: c15_small_writer_buffer_marker
    // Purpose: small writer buffer (e.g. 8-64B)
    // If std.Io.Reader/Writer API shape has changed in your local Zig version,
    // this file may need updating – that is expected and is recorded as api_changed.
    _ = std;
}
