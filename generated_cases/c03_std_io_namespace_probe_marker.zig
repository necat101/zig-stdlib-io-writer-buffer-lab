const std = @import("std");

pub fn main() !void {
    const has_io = @hasDecl(std, "Io");
    if (!has_io) @panic("std.Io missing");
    std.debug.print("CASE c03_std_io_namespace_probe_marker PASS has_io=true\n", .{});
}
