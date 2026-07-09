const std = @import("std");

pub fn main() !void {
    var buf: [16]u8 = undefined;
    var w = std.Io.Writer.fixed(&buf);
    try w.writeAll("x");
    try w.flush();
    std.debug.print("CASE c12_writer_flush_probe_marker PASS end={}\n", .{w.end});
}
