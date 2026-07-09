const std = @import("std");

pub fn main() !void {
    // Article context: zstd Decompress with small output buffer
    // We do NOT trigger the actual bug/infinite loop – just probe API presence
    // and document that buffer-size requirements exist
    const has_zstd = @hasDecl(std.compress, "zstd");
    if (!has_zstd) {
        std.debug.print("CASE c21_zstd_small_buffer_context_marker SKIP no_zstd\n", .{});
        return;
    }
    // Check Decompress.Options has window_len field (this is where buffer size requirement lives)
    const Opt = std.compress.zstd.Decompress.Options;
    const has_window_len = @hasField(Opt, "window_len");
    std.debug.print("CASE c21_zstd_small_buffer_context_marker PASS has_window_len={} note=small_output_buffer_is_article_context_no_crash_tested\n", .{has_window_len});
}
