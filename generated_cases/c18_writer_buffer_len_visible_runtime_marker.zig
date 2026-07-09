const std = @import("std");

pub fn main() !void {
    var buf: [123]u8 = undefined;
    var w = std.Io.Writer.fixed(&buf);
    const len = w.buffer.len;
    std.debug.print("CASE c18_writer_buffer_len_visible_runtime_marker PASS buffer_len={}\n", .{len});
}
