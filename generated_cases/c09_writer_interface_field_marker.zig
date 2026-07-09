const std = @import("std");

pub fn main() !void {
    var buf: [8]u8 = undefined;
    var w = std.Io.Writer.fixed(&buf);
    // Writer has .buffer, .end fields – check they exist at compile time
    _ = w.buffer;
    _ = w.end;
    std.debug.print("CASE c09_writer_interface_field_marker PASS buffer_len={}\n", .{w.buffer.len});
}
