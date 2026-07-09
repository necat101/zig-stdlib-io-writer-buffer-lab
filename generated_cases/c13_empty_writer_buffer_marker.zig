const std = @import("std");

pub fn main() !void {
    var empty_buf: [0]u8 = .{};
    var w = std.Io.Writer.fixed(&empty_buf);
    // empty buffer writer should still be constructible (unbuffered mode)
    std.debug.print("CASE c13_empty_writer_buffer_marker PASS buffer_len={}\n", .{w.buffer.len});
}
