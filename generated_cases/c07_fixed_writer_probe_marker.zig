const std = @import("std");

pub fn main() !void {
    var buf: [32]u8 = undefined;
    var w = std.Io.Writer.fixed(&buf);
    try w.writeAll("hello");
    try w.flush();
    std.debug.print("CASE c07_fixed_writer_probe_marker PASS wrote={}\n", .{w.end});
}
