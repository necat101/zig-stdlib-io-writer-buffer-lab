const std = @import("std");

pub fn main() !void {
    // Try to use std.Io.Reader.fixed and stream – basic article API shape
    var r = std.Io.Reader.fixed("test");
    var out_buf: [16]u8 = undefined;
    var w = std.Io.Writer.fixed(&out_buf);
    _ = try r.stream(&w, .unlimited);
    try w.flush();
    std.debug.print("CASE c39_article_snippet_compile_observer PASS\n", .{});
}
