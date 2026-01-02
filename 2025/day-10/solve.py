import sys
import re

def count_set_bits(n):
    return bin(n).count('1')

def solve():
    try:
        with open('2025/day-10/input.txt', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("input.txt not found")
        return

    total_presses = 0

    for line_idx, line in enumerate(lines):
        line = line.strip()
        if not line: continue

        # Parse target
        target_match = re.search(r'\[([.#]+)\]', line)
        if not target_match:
            print(f"Skipping invalid line {line_idx+1}")
            continue
        
        target_str = target_match.group(1)
        target_mask = 0
        for i, char in enumerate(target_str):
            if char == '#':
                target_mask |= (1 << i)

        # Parse buttons
        # The regex finds all occurrences of (num,num,...)
        # We need to be careful not to match things inside the joltage braces if they looked like parens (they don't in the example)
        # But to be safe, we can split by '{' first.
        
        parts = line.split('{')
        button_part = parts[0]
        
        # Regex to find (1,2,3)
        button_strings = re.findall(r'\(([\d,]+)\)', button_part)
        
        buttons = []
        for b_str in button_strings:
            mask = 0
            nums = [int(x) for x in b_str.split(',')]
            for n in nums:
                mask |= (1 << n)
            buttons.append(mask)

        n = len(buttons)
        min_presses = float('inf')
        found = False

        # Brute force all subsets
        # 2^13 is small enough
        for i in range(1 << n):
            current_state = 0
            presses = 0
            
            # Optimization: could precompute bit counts or iterate set bits
            # But for 13 bits, iterating 0..12 is fast
            for b in range(n):
                if (i >> b) & 1:
                    current_state ^= buttons[b]
                    presses += 1
            
            if current_state == target_mask:
                if presses < min_presses:
                    min_presses = presses
                found = True

        if found:
            total_presses += min_presses
        else:
            # If no solution, maybe we shouldn't add anything? 
            # Or maybe it's impossible (shouldn't happen based on problem type usually)
            print(f"No solution for line {line_idx+1}")

    print(f"Total minimum presses: {total_presses}")

if __name__ == "__main__":
    solve()
