#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <fstream>
#include <string>
#include <sstream>

using namespace std;

struct Box {
    long long x, y, z;
    int id;
};

struct Connection {
    int a, b;
    long long dist_sq;
};

struct DSU {
    vector<int> parent;
    vector<int> size;
    DSU(int n) {
        parent.resize(n);
        size.assign(n, 1);
        for (int i = 0; i < n; ++i) parent[i] = i;
    }
    int find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent[i]);
    }
    bool unite(int i, int j) {
        int root_i = find(i);
        int root_j = find(j);
        if (root_i != root_j) {
            if (size[root_i] < size[root_j]) swap(root_i, root_j);
            parent[root_j] = root_i;
            size[root_i] += size[root_j];
            return true;
        }
        return false;
    }
};

int main() {
    ifstream f("2025/day-8/input.txt");
    vector<Box> boxes;
    string line;
    int id = 0;
    while (getline(f, line)) {
        if (line.empty()) continue;
        for (auto& c : line) if (c == ',') c = ' ';
        stringstream ss(line);
        long long x, y, z;
        if (ss >> x >> y >> z) {
            boxes.push_back({x, y, z, id++});
        }
    }

    int n = boxes.size();
    vector<Connection> conns;
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            long long dx = boxes[i].x - boxes[j].x;
            long long dy = boxes[i].y - boxes[j].y;
            long long dz = boxes[i].z - boxes[j].z;
            conns.push_back({i, j, dx*dx + dy*dy + dz*dz});
        }
    }

    sort(conns.begin(), conns.end(), [](const Connection& a, const Connection& b) {
        return a.dist_sq < b.dist_sq;
    });

    // Part 1
    DSU dsu1(n);
    int target = min(1000, (int)conns.size());
    for (int k = 0; k < target; ++k) {
        dsu1.unite(conns[k].a, conns[k].b);
    }
    vector<int> sizes;
    for (int i = 0; i < n; ++i) {
        if (dsu1.parent[i] == i) sizes.push_back(dsu1.size[i]);
    }
    sort(sizes.rbegin(), sizes.rend());
    long long p1 = 1;
    for (int i = 0; i < min(3, (int)sizes.size()); ++i) p1 *= sizes[i];
    cout << "Part 1: " << p1 << endl;

    // Part 2
    DSU dsu2(n);
    int merges = 0;
    for (const auto& c : conns) {
        if (dsu2.unite(c.a, c.b)) {
            merges++;
            if (merges == n - 1) {
                long long p2 = (long long)boxes[c.a].x * boxes[c.b].x;
                cout << "Part 2: " << p2 << endl;
                break;
            }
        }
    }

    return 0;
}