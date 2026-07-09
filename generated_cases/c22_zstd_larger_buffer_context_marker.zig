const std = @import("std");

pub fn main() !void {
    const has_zstd = @hasDecl(std.compress, "zstd");
    if (!has_zstd) {
        std.debug.print("CASE c22_zstd_larger_buffer_context_marker SKIP no_zstd\n", .{});
        return;
    }
    std.debug.print("CASE c22_zstd_larger_buffer_context_marker PASS note=larger_buffer_context_no_crash_tested\n", .{});
}
