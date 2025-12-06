#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 4: Printing Department
Count rolls of paper that can be accessed by a forklift (fewer than 4 adjacent rolls).
"""

def solve():
    with open("input.txt", "r") as f:
        grid = [line.rstrip('\n') for line in f]
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # 8 directions: N, NE, E, SE, S, SW, W, NW
    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    
    accessible_count = 0
    
    for r in range(rows):
        for c in range(cols):
            # Only check cells with rolls of paper
            if grid[r][c] == '@':
                # Count adjacent rolls
                adjacent_rolls = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                        adjacent_rolls += 1
                
                # Accessible if fewer than 4 adjacent rolls
                if adjacent_rolls < 4:
                    accessible_count += 1
    
    print(f"Rolls accessible by forklift: {accessible_count}")
    return accessible_count

if __name__ == "__main__":
    solve()
