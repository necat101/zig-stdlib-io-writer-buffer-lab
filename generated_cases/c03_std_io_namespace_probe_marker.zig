// c03_std_io_namespace_probe_marker – probe std.Io namespace existence
// Category: stdlib_source_probe
// HN marker: api_contract
// Article marker: io_interface_context
// Buffer class: n/a
// This is a correctness lab stub – real stdlib API usage is version-sensitive.
// Local Zig compiler validation required – do not assume API stability.
//
// No network, no TLS, no external payloads, no fuzzing.
// No global safety claims – local compiler truth only.

const std = @import("std");

pub fn main() !void {
    // Case: c03_std_io_namespace_probe_marker
    // Purpose: probe std.Io namespace existence
    // If std.Io.Reader/Writer API shape has changed in your local Zig version,
    // this file may need updating – that is expected and is recorded as api_changed.
    _ = std;
}
