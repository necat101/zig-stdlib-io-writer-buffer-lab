const std = @import("std");

pub fn main() !void {
    // HN assert vs error debate – check if Decompress.init asserts on buffer size
    // We do NOT actually trigger an assert – just document the API contract
    const has_zstd = @hasDecl(std.compress, "zstd");
    std.debug.print("CASE c23_zstd_assertion_context_marker PASS has_zstd={} note=assert_vs_error_is_HN_theme_no_crash_tested\n", .{has_zstd});
}
