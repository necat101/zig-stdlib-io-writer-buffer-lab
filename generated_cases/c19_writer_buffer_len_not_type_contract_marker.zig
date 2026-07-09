const std = @import("std");

pub fn main() !void {
    // Writer type does NOT encode buffer length in its type – this is the HN "leaky abstraction" point
    // Demonstrate: two writers with different buffer sizes have the SAME type
    var buf1: [1]u8 = undefined;
    var buf2: [4096]u8 = undefined;
    var w1 = std.Io.Writer.fixed(&buf1);
    var w2 = std.Io.Writer.fixed(&buf2);
    const T1 = @TypeOf(w1);
    const T2 = @TypeOf(w2);
    const same_type = T1 == T2;
    std.debug.print("CASE c19_writer_buffer_len_not_type_contract_marker PASS same_type={} len1={} len2={}\n", .{same_type, w1.buffer.len, w2.buffer.len});
}
