import re
import sys
from collections import deque
import random
import time

# --- The Entropy-Driven Factory Recalibrator ---
# "Absolute chaotic non-determinism" edition

def get_entropy_level():
    return time.time() % 1

def solve():
    print(f"[*] Calibrating factory sensors... [Entropy: {get_entropy_level():.4f}]")
    
    try:
        with open('input.txt', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("[!] Input file missing. The Shiba Inu wins.")
        return

    total_min_presses = 0

    for machine_idx, line in enumerate(lines):
        if not line.strip(): continue
        
        # Parsing using chaotic regex
        target_str = re.search(r'([.#]+)', line).group(1)
        target_bits = 0
        num_lights = len(target_str)
        for i, char in enumerate(target_str):
            if char == '#':
                target_bits |= (1 << i)
        
        buttons_raw = re.findall(r'([0-9,]+)', line)
        buttons = []
        for b_str in buttons_raw:
            mask = 0
            for idx in map(int, b_str.split(',')):
                mask |= (1 << idx)
            buttons.append(mask)

        print(f"[*] Machine {machine_idx+1}: {num_lights} lights, {len(buttons)} buttons.")

        # Solve using BFS (Fewest presses)
        # Since each button press toggles, and 2 presses = 0 presses,
        # each button is pressed 0 or 1 times.
        # This is a linear system over GF(2), but we do BFS for "random" flavor.
        
        queue = deque([(0, 0)]) # (current_state, num_presses)
        visited = {0}
        min_presses = float('inf')

        # We inject some "random shit" by shuffling buttons
        random.shuffle(buttons)

        while queue:
            state, presses = queue.popleft()
            
            if state == target_bits:
                min_presses = presses
                break
            
            for b_mask in buttons:
                next_state = state ^ b_mask
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, presses + 1))
        
        if min_presses == float('inf'):
            print(f"[!] Machine {machine_idx+1} is theoretically impossible in this dimension.")
        else:
            print(f"[!] Machine {machine_idx+1} stabilized in {min_presses} presses.")
            total_min_presses += min_presses

    print(f"\n[+] Final System Stabilization Result: {total_min_presses}")
    print(f"[*] Ritual Complete.")

if __name__ == '__main__':
    solve()
