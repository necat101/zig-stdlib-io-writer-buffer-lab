// c19_writer_buffer_len_not_type_contract_marker – buffer len NOT in Writer type contract – HN leaky abstraction theme
// Category: api_shape
// HN marker: buffer_size_leak
// Article marker: io_interface_context
// Buffer class: n/a
// This is a correctness lab stub – real stdlib API usage is version-sensitive.
// Local Zig compiler validation required – do not assume API stability.
//
// No network, no TLS, no external payloads, no fuzzing.
// No global safety claims – local compiler truth only.

const std = @import("std");

pub fn main() !void {
    // Case: c19_writer_buffer_len_not_type_contract_marker
    // Purpose: buffer len NOT in Writer type contract – HN leaky abstraction theme
    // If std.Io.Reader/Writer API shape has changed in your local Zig version,
    // this file may need updating – that is expected and is recorded as api_changed.
    _ = std;
}
