const std = @import("std");

pub fn main() !void {
    const has_reader = @hasDecl(std.Io, "Reader");
    if (!has_reader) @panic("Reader missing");
    std.debug.print("CASE c04_std_io_reader_exists_marker PASS\n", .{});
}
