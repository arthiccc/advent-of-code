#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 4: Printing Department (Part 2)
Repeatedly remove accessible rolls (fewer than 4 adjacent) until none remain accessible.
Count total rolls removed.
"""

def solve():
    with open("input.txt", "r") as f:
        grid = [list(line.rstrip('\n')) for line in f]
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # 8 directions: N, NE, E, SE, S, SW, W, NW
    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    
    total_removed = 0
    
    while True:
        # Find all accessible rolls in this iteration
        to_remove = []
        
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    # Count adjacent rolls
                    adjacent_rolls = 0
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                            adjacent_rolls += 1
                    
                    # Accessible if fewer than 4 adjacent rolls
                    if adjacent_rolls < 4:
                        to_remove.append((r, c))
        
        # If no rolls can be removed, we're done
        if not to_remove:
            break
        
        # Remove all accessible rolls at once
        for r, c in to_remove:
            grid[r][c] = '.'
        
        total_removed += len(to_remove)
        print(f"Removed {len(to_remove)} rolls this iteration")
    
    print(f"\nTotal rolls removed by forklifts: {total_removed}")
    return total_removed

if __name__ == "__main__":
    solve()
