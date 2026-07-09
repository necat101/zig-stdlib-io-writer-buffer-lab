const std = @import("std");

pub fn main() !void {
    var r = std.Io.Reader.fixed("abc");
    // check methods exist by calling them
    var tmp: [1]u8 = undefined;
    _ = try r.read(&tmp);
    std.debug.print("CASE c10_reader_interface_method_marker PASS\n", .{});
}
