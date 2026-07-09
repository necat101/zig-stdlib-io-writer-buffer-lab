const std = @import("std");

pub fn main() !void {
    var buf: [64]u8 = undefined;
    var w = std.Io.Writer.fixed(&buf);
    try w.writeAll("small buffer test data 12345");
    try w.flush();
    std.debug.print("CASE c15_small_writer_buffer_marker PASS end={}\n", .{w.end});
}
