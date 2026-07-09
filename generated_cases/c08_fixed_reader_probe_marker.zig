const std = @import("std");

pub fn main() !void {
    const data = "hello zig";
    var r = std.Io.Reader.fixed(data);
    var tmp: [5]u8 = undefined;
    const n = try r.read(&tmp);
    std.debug.print("CASE c08_fixed_reader_probe_marker PASS n={}\n", .{n});
}
