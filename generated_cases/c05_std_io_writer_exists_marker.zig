const std = @import("std");

pub fn main() !void {
    const has_writer = @hasDecl(std.Io, "Writer");
    if (!has_writer) @panic("Writer missing");
    std.debug.print("CASE c05_std_io_writer_exists_marker PASS\n", .{});
}
