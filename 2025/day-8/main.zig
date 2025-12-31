const std = @import("std");

const Box = struct {
    x: f64,
    y: f64,
    z: f64,
    id: usize,
};

const Connection = struct {
    a: usize,
    b: usize,
    dist_sq: f64,
};

const DSU = struct {
    parent: []usize,
    size: []usize,
    allocator: std.mem.Allocator,

    fn init(allocator: std.mem.Allocator, n: usize) !DSU {
        const parent = try allocator.alloc(usize, n);
        const size = try allocator.alloc(usize, n);
        for (0..n) |i| {
            parent[i] = i;
            size[i] = 1;
        }
        return DSU{ .parent = parent, .size = size, .allocator = allocator };
    }

    fn deinit(self: *DSU) void {
        self.allocator.free(self.parent);
        self.allocator.free(self.size);
    }

    fn find(self: *DSU, i: usize) usize {
        if (self.parent[i] == i) return i;
        self.parent[i] = self.find(self.parent[i]);
        return self.parent[i];
    }

    fn unite(self: *DSU, i: usize, j: usize) bool {
        var root_i = self.find(i);
        var root_j = self.find(j);
        if (root_i != root_j) {
            if (self.size[root_i] < self.size[root_j]) std.mem.swap(usize, &root_i, &root_j);
            self.parent[root_j] = root_i;
            self.size[root_i] += self.size[root_j];
            return true;
        }
        return false;
    }
};

fn compareConnections(context: void, a: Connection, b: Connection) bool {
    _ = context;
    return a.dist_sq < b.dist_sq;
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    defer _ = gpa.deinit();

    const file = try std.fs.cwd().openFile("2025/day-8/input.txt", .{});
    defer file.close();

    var buf_reader = std.io.bufferedReader(file.reader());
    var in_stream = buf_reader.reader();

    var boxes = std.ArrayList(Box).init(allocator);
    defer boxes.deinit();

    var buf: [1024]u8 = undefined;
    var id_counter: usize = 0;
    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        var it = std.mem.tokenizeAny(u8, line, ", \t\r");
        const x = try std.fmt.parseFloat(f64, it.next() orelse continue);
        const y = try std.fmt.parseFloat(f64, it.next() orelse continue);
        const z = try std.fmt.parseFloat(f64, it.next() orelse continue);
        try boxes.append(.{ .x = x, .y = y, .z = z, .id = id_counter });
        id_counter += 1;
    }

    const n = boxes.items.len;
    var connections = std.ArrayList(Connection).init(allocator);
    defer connections.deinit();

    for (0..n) |i| {
        for (i + 1..n) |j| {
            const dx = boxes.items[i].x - boxes.items[j].x;
            const dy = boxes.items[i].y - boxes.items[j].y;
            const dz = boxes.items[i].z - boxes.items[j].z;
            const d2 = dx * dx + dy * dy + dz * dz;
            try connections.append(.{ .a = i, .b = j, .dist_sq = d2 });
        }
    }

    std.sort.pdq(Connection, connections.items, {}, compareConnections);

    var dsu = try DSU.init(allocator, n);
    defer dsu.deinit();

    var conn_count: usize = 0;
    for (connections.items) |conn| {
        if (dsu.unite(conn.a, conn.b)) {
            conn_count += 1;
            if (conn_count == 1000) {
                var sizes = std.ArrayList(usize).init(allocator);
                defer sizes.deinit();
                for (0..n) |i| {
                    if (dsu.parent[i] == i) try sizes.append(dsu.size[i]);
                }
                std.sort.pdq(usize, sizes.items, {}, std.sort.desc(usize));
                const p1 = sizes.items[0] * sizes.items[1] * sizes.items[2];
                try std.io.getStdOut().writer().print("Part 1: {}\n", .{p1});
            }
            if (conn_count == n - 1) {
                const p2 = @as(i64, @intFromFloat(boxes.items[conn.a].x)) * @as(i64, @intFromFloat(boxes.items[conn.b].x));
                try std.io.getStdOut().writer().print("Part 2: {}\n", .{p2});
                break;
            }
        }
    }
}
