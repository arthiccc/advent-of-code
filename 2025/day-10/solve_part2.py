import sys
import re
from fractions import Fraction
import itertools

def solve_part2():
    try:
        with open('2025/day-10/input.txt', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("input.txt not found")
        return

    total_min_presses = 0

    print(f"Processing {len(lines)} machines...")

    for line_idx, line in enumerate(lines):
        line = line.strip()
        if not line: continue
        
        if (line_idx + 1) % 20 == 0:
            print(f"Processing line {line_idx + 1}...")

        # Parse Targets {a,b,c}
        brace_match = re.search(r'\{([\d,]+)\}', line)
        if not brace_match: continue
        targets = [int(x) for x in brace_match.group(1).split(',')]
        num_eqs = len(targets)
        
        # Parse Buttons
        parts = line.split('{')
        button_part = parts[0]
        button_strings = re.findall(r'\(([\d,]+)\)', button_part)
        
        num_vars = len(button_strings)
        
        # Build Matrix A (num_eqs x num_vars) and Bounds
        matrix = [[Fraction(0)] * num_vars for _ in range(num_eqs)]
        var_bounds = [float('inf')] * num_vars
        var_is_useful = [False] * num_vars

        for col, b_str in enumerate(button_strings):
            affected = [int(x) for x in b_str.split(',')]
            for row in affected:
                if row < num_eqs:
                    matrix[row][col] = Fraction(1)
                    var_is_useful[col] = True
                    # Bound: variable cannot exceed target value it contributes to
                    # strict bound: if A[row][col] == 1, then x[col] <= targets[row]
                    if var_bounds[col] == float('inf') or targets[row] < var_bounds[col]:
                        var_bounds[col] = targets[row]
            
            if not var_is_useful[col]:
                var_bounds[col] = 0
            if var_bounds[col] == float('inf'):
                var_bounds[col] = 0 # Should not happen if useful

        # Augment matrix with targets
        for i in range(num_eqs):
            matrix[i].append(Fraction(targets[i]))

        # Gaussian Elimination to RREF
        pivot_row = 0
        pivots = {} # col -> row (where the leading 1 is)
        pivot_cols = []
        
        for col in range(num_vars):
            if pivot_row >= num_eqs: break
            
            # Find pivot
            sel = -1
            for r in range(pivot_row, num_eqs):
                if matrix[r][col] != 0:
                    sel = r
                    break
            
            if sel == -1: continue
            
            # Swap
            matrix[pivot_row], matrix[sel] = matrix[sel], matrix[pivot_row]
            
            # Normalize
            val = matrix[pivot_row][col]
            for c in range(col, num_vars + 1):
                matrix[pivot_row][c] /= val
            
            # Eliminate
            for r in range(num_eqs):
                if r != pivot_row and matrix[r][col] != 0:
                    factor = matrix[r][col]
                    for c in range(col, num_vars + 1):
                        matrix[r][c] -= factor * matrix[pivot_row][c]
            
            pivots[col] = pivot_row
            pivot_cols.append(col)
            pivot_row += 1

        # Check for consistency
        possible = True
        for r in range(pivot_row, num_eqs):
            if matrix[r][num_vars] != 0:
                possible = False
                break
        
        if not possible:
            print(f"Line {line_idx+1}: Impossible system")
            continue

        # Identify free variables
        free_vars = [c for c in range(num_vars) if c not in pivots]
        
        best_presses = float('inf')
        
        ranges = [range(int(var_bounds[fv]) + 1) for fv in free_vars]
        
        # Iterate free variables
        for free_vals in itertools.product(*ranges):
            valid = True
            current_presses = 0
            
            solution = {}
            # Set free vars
            for i, fv in enumerate(free_vars):
                val = free_vals[i]
                solution[fv] = val
                current_presses += val
            
            # Compute pivot vars
            for pc in pivot_cols:
                r = pivots[pc]
                val = matrix[r][num_vars] # Constant
                for fv in free_vars:
                    val -= matrix[r][fv] * solution[fv]
                
                if val.denominator != 1 or val < 0:
                    valid = False
                    break
                
                # int check (redundant but safe)
                ival = int(val)
                if ival > var_bounds[pc]:
                    valid = False
                    break
                    
                solution[pc] = ival
                current_presses += ival
            
            if valid:
                if current_presses < best_presses:
                    best_presses = current_presses

        if best_presses != float('inf'):
            total_min_presses += best_presses
        else:
            print(f"Line {line_idx+1}: No valid integer solution found")

    print(f"Total Part 2: {total_min_presses}")

if __name__ == "__main__":
    solve_part2()
