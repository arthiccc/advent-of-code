from shapely.geometry import Polygon

def solve():
    with open('input.txt', 'r') as f:
        coords = [tuple(map(int, line.strip().split(','))) for line in f if line.strip()]

    # Part 1: Largest rectangle with two opposite corners as red tiles
    # Red tiles are the coordinates in input
    max_area_p1 = 0
    set(coords)
    
    # We can pick any two red tiles (x1, y1) and (x2, y2) as opposite corners.
    # Area = |x1 - x2| * |y1 - y2|
    # However, for Part 1, the description usually implies the coordinates form a bounding box?
    # Actually, Part 1 says "largest possible rectangle ... two of its opposite corners must be occupied by red tiles".
    # This is a classic O(N^2) or O(N log N). Given ~200 points, O(N^2) is fine.
    
    n = len(coords)
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = coords[i]
            x2, y2 = coords[j]
            area = abs(x1 - x2) * abs(y1 - y2)
            if area > max_area_p1:
                max_area_p1 = area
                
    # Part 2: Loop constraint
    # Red tiles are connected in sequence to form a closed loop.
    poly = Polygon(coords)
    
    max_area_p2 = 0
    # A rectangle (x1, y1) to (x2, y2) is valid if all its points are in the polygon (red/green).
    # Since it's a grid, we should check if the bounding box of the rectangle is within the polygon.
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = coords[i]
            x2, y2 = coords[j]
            
            # Skip if area is smaller than current max
            area = abs(x1 - x2) * abs(y1 - y2)
            if area <= max_area_p2:
                continue
            
            # Check if all four corners are within or on the polygon
            # And then check if the rectangle is contained.
            # For a polygon, if corners are inside and no edges intersect the boundary, it's inside.
            # But the polygon might be concave.
            
            from shapely.geometry import box
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            rect = box(min_x, min_y, max_x, max_y)
            
            if poly.contains(rect) or poly.equals(rect):
                max_area_p2 = area

    print(f"Part 1: {max_area_p1}")
    print(f"Part 2: {max_area_p2}")

if __name__ == '__main__':
    solve()