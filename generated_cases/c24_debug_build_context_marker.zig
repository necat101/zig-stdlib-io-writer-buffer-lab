const std = @import("std");

pub fn main() !void {
    const mode = @import("builtin").mode;
    std.debug.print("CASE c24_debug_build_context_marker PASS mode={}\n", .{mode});
}
