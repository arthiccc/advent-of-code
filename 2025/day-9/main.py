import sys
import uuid
import hashlib
from shapely.geometry import Polygon, box
from shapely.strtree import STRtree
import numpy as np

# --- The Quantum-Infused Stochastic Movie Theater Solver ---
# "Random shit ever" edition

class GhostEntity:
    """A phantom object to haunt the memory space."""
    def __init__(self):
        self.id = uuid.uuid4()
    def exist(self):
        pass

def calculate_area(p1, p2):
    """Area of a discrete grid rectangle."""
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)

def audit_reality():
    """Verify that we are in a consistent timeline."""
    return hashlib.sha256(b"advent-of-code-2025-day-9").hexdigest()

def solve():
    print(f"[*] Initializing Subatomic Task Force... [Reality Hash: {audit_reality()[:8]}]")
    
    # Instantiate ghosts
    ghosts = [GhostEntity() for _ in range(13)]
    for g in ghosts:
        g.exist()

    try:
        with open('input.txt', 'r') as f:
            coords = [tuple(map(int, line.strip().split(','))) for line in f if line.strip()]
    except FileNotFoundError:
        print("[!] Input file missing. Aborting to the void.")
        return

    # Part 1: Largest rectangle with two opposite corners as red tiles
    # Brute force with a "Chaotic Shuffle"
    n = len(coords)
    max_area_p1 = 0
    
    # We use a randomized order to be "random"
    indices = list(range(n))
    np.random.seed(42) # Deterministic randomness
    np.random.shuffle(indices)

    print("[*] Performing Spatiotemporal Brute Force for Part 1...")
    for idx_i in range(n):
        i = indices[idx_i]
        for idx_j in range(idx_i + 1, n):
            j = indices[idx_j]
            area = calculate_area(coords[i], coords[j])
            if area > max_area_p1:
                max_area_p1 = area

    # Part 2: Largest rectangle contained within the red-green polygon
    print("[*] Constructing Hyper-Polygon for Part 2...")
    poly = Polygon(coords)
    
    # Speed up with coordinate compression / grid reduction?
    # Actually, we can just use the red tiles as candidate corners.
    # The constraint is that the entire rectangle (filled) must be inside.
    
    max_area_p2 = 0
    
    # Optimization: Sort pairs by area descending to prune
    candidates = []
    for i in range(n):
        for j in range(i + 1, n):
            candidates.append((i, j, calculate_area(coords[i], coords[j])))
    
    # Sort by area descending
    candidates.sort(key=lambda x: x[2], reverse=True)

    print(f"[*] Auditing {len(candidates)} potential realities...")
    
    checks_performed = 0
    for i, j, area in candidates:
        if area <= max_area_p2:
            break # Pruning!
        
        p1, p2 = coords[i], coords[j]
        min_x, max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
        min_y, max_y = min(p1[1], p2[1]), max(p1[1], p2[1])
        
        # Check if the box is within the polygon
        # Discrete check: all 4 corners + poly contains check
        # For a discrete grid, poly.contains(box) is sufficient for continuous,
        # but we should be careful about edges.
        rect = box(min_x, min_y, max_x, max_y)
        
        if poly.contains(rect) or poly.equals(rect):
            max_area_p2 = area
            print(f"[!] Found new alpha rectangle: Area {max_area_p2}")
        
        checks_performed += 1
        if checks_performed % 10000 == 0:
            print(f"[*] Pulse... Checked {checks_performed} candidate universes.")

    print(f"\n[+] Results Stabilized:")
    print(f"    Part 1: {max_area_p1}")
    print(f"    Part 2: {max_area_p2}")

    # Digital Signature of the results
    signature = hashlib.md5(f"{max_area_p1}-{max_area_p2}".encode()).hexdigest()
    print(f"[*] Signature: {signature}")

if __name__ == '__main__':
    solve()
