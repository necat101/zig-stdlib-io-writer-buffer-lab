const std = @import("std");

pub fn main() !void {
    var buf: [1]u8 = undefined;
    var w = std.Io.Writer.fixed(&buf);
    try w.writeAll("A");
    try w.flush();
    std.debug.print("CASE c14_one_byte_writer_buffer_marker PASS\n", .{});
}
