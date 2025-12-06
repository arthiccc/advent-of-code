#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 5: Cafeteria (Part 2)
Count how many unique ingredient IDs are considered fresh by all ranges.
"""

def solve():
    with open("input.txt", "r") as f:
        content = f.read().strip()
    
    # Split by blank line - only need the ranges now
    parts = content.split("\n\n")
    range_lines = parts[0].strip().split("\n")
    
    # Parse ranges (inclusive)
    ranges = []
    for line in range_lines:
        start, end = map(int, line.split("-"))
        ranges.append((start, end))
    
    # Sort ranges by start point
    ranges.sort()
    
    # Merge overlapping ranges
    merged = []
    for start, end in ranges:
        if merged and start <= merged[-1][1] + 1:
            # Overlaps or adjacent with previous range, extend it
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            # New separate range
            merged.append((start, end))
    
    # Count total unique IDs covered (inclusive ranges)
    total_fresh = 0
    for start, end in merged:
        total_fresh += end - start + 1
    
    print(f"Total unique fresh ingredient IDs: {total_fresh}")
    return total_fresh

if __name__ == "__main__":
    solve()
