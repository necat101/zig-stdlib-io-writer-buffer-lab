const std = @import("std");

pub fn main() !void {
    const has_zstd = @hasDecl(std.compress, "zstd");
    std.debug.print("CASE c20_zstd_decompress_api_probe_marker PASS has_zstd={}\n", .{has_zstd});
    if (has_zstd) {
        const Decompress = std.compress.zstd.Decompress;
        _ = Decompress;
    }
}
