const std = @import("std");

pub fn main() !void {
    var r = std.Io.Reader.fixed("stream test data");
    var out_buf: [64]u8 = undefined;
    var w = std.Io.Writer.fixed(&out_buf);
    const n = try r.stream(&w, .unlimited);
    try w.flush();
    std.debug.print("CASE c11_stream_method_probe_marker PASS n={}\n", .{n});
}
