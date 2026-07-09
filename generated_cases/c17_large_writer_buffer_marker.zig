const std = @import("std");

pub fn main() !void {
    var buf: [8192]u8 = undefined;
    var w = std.Io.Writer.fixed(&buf);
    try w.writeAll("large buffer");
    try w.flush();
    std.debug.print("CASE c17_large_writer_buffer_marker PASS\n", .{});
}
