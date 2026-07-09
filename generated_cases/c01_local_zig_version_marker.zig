const std = @import("std");

pub fn main() !void {
    const v = @import("builtin").zig_version;
    std.debug.print("CASE c01_local_zig_version_marker PASS zig={}.{}.{}\n", .{v.major, v.minor, v.patch});
}
