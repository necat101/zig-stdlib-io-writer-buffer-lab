const std = @import("std");

pub fn main() !void {
    var buf: [1024]u8 = undefined;
    var w = std.Io.Writer.fixed(&buf);
    try w.writeAll("kilobyte buffer test");
    try w.flush();
    std.debug.print("CASE c16_kilobyte_writer_buffer_marker PASS\n", .{});
}
