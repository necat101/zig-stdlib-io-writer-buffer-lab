const std = @import("std");

pub fn main() !void {
    // In std.Io, Writer is a struct with a buffer field, not a generic function
    // Just verify we can construct one
    var buf: [16]u8 = undefined;
    var w = std.Io.Writer.fixed(&buf);
    _ = &w;
    std.debug.print("CASE c06_file_writer_buffer_signature_marker PASS\n", .{});
}
