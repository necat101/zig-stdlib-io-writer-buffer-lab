const std = @import("std");

pub fn main() !void {
    var r = std.Io.Reader.fixed("hello world with large writer buffer");
    var large_buf: [4096]u8 = undefined;
    var w = std.Io.Writer.fixed(&large_buf);
    const n = try r.stream(&w, .unlimited);
    try w.flush();
    std.debug.print("CASE c41_fixed_reader_stream_large_writer_marker PASS n={} buf_len={}\n", .{n, large_buf.len});
}
