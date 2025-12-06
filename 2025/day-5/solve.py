#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 5: Cafeteria
Determine how many available ingredient IDs are fresh (fall within any range).
"""

def solve():
    with open("input.txt", "r") as f:
        content = f.read().strip()
    
    # Split by blank line
    parts = content.split("\n\n")
    range_lines = parts[0].strip().split("\n")
    id_lines = parts[1].strip().split("\n")
    
    # Parse ranges (inclusive)
    ranges = []
    for line in range_lines:
        start, end = map(int, line.split("-"))
        ranges.append((start, end))
    
    # Parse available ingredient IDs
    ingredient_ids = [int(line.strip()) for line in id_lines]
    
    # Count how many IDs are fresh (fall within ANY range)
    fresh_count = 0
    for ing_id in ingredient_ids:
        for start, end in ranges:
            if start <= ing_id <= end:
                fresh_count += 1
                break  # Only count once per ID
    
    print(f"Number of fresh ingredient IDs: {fresh_count}")
    return fresh_count

if __name__ == "__main__":
    solve()
