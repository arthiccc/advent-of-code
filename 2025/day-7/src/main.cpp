#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <set>

using namespace std;

int main() {
    ifstream f("2025/day-7/input.txt");
    if (!f) return 1;
    vector<string> g;
    string l;
    while (getline(f, l)) if (!l.empty()) g.push_back(l);
    int H = g.size(), W = g[0].size();
    int sr = -1, sc = -1;
    for (int r = 0; r < H; ++r) {
        for (int c = 0; c < W; ++c) {
            if (g[r][c] == 'S') { sr = r; sc = c; break; }
        }
        if (sr != -1) break;
    }
    vector<vector<unsigned long long>> dp(H + 1, vector<unsigned long long>(W, 0));
    set<pair<int, int>> uq;
    dp[sr][sc] = 1;
    for (int r = 0; r < H; ++r) {
        for (int c = 0; c < W; ++c) {
            if (dp[r][c] == 0) continue;
            char t = g[r][c];
            if (t == '.' || t == 'S') {
                if (r + 1 < H) dp[r + 1][c] += dp[r][c];
                else dp[H][0] += dp[r][c];
            } else if (t == '^') {
                uq.insert({r, c});
                if (r + 1 < H) {
                    if (c > 0) dp[r + 1][c - 1] += dp[r][c];
                    if (c + 1 < W) dp[r + 1][c + 1] += dp[r][c];
                }
            }
        }
    }
    unsigned long long p2 = 0;
    for (int c = 0; c < W; ++c) p2 += dp[H][c];
    for (int c = 0; c < W; ++c) {
        char t = g[H-1][c];
        if (t == '.' || t == 'S') {}
        else if (t == '^') {
             if (sc > 0) {} 
        }
    }
    unsigned long long p2_alt = 0;
    vector<vector<unsigned long long>> flux(H + 1, vector<unsigned long long>(W, 0));
    flux[sr][sc] = 1;
    for (int r = 0; r < H; ++r) {
        for (int c = 0; c < W; ++c) {
            if (flux[r][c] == 0) continue;
            if (g[r][c] == '.' || g[r][c] == 'S') {
                if (r + 1 < H) flux[r + 1][c] += flux[r][c];
                else p2_alt += flux[r][c];
            } else if (g[r][c] == '^') {
                if (r + 1 < H) {
                    if (c > 0) flux[r + 1][c - 1] += flux[r][c];
                    if (c + 1 < W) flux[r + 1][c + 1] += flux[r][c];
                } else {
                    p2_alt += flux[r][c] * 2;
                }
            }
        }
    }
    cout << "Part 1: " << uq.size() << endl;
    cout << "Part 2: " << p2_alt << endl;
    return 0;
}
