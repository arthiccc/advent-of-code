#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <limits.h>

#define MAX_BUTTONS 64

typedef struct {
    uint64_t target;
    uint64_t buttons[MAX_BUTTONS];
    int num_buttons;
} Machine;

int count_set_bits(uint64_t n) {
    int count = 0;
    while (n > 0) {
        n &= (n - 1);
        count++;
    }
    return count;
}

// Function to parse a single line into a Machine structure
int parse_line(char *line, Machine *m) {
    m->num_buttons = 0;
    m->target = 0;
    memset(m->buttons, 0, sizeof(m->buttons));

    char *start = strchr(line, '[');
    char *end = strchr(line, ']');
    if (!start || !end) return 0;

    // Parse target pattern
    for (char *p = start + 1; p < end; p++) {
        if (*p == '#') {
            m->target |= (1ULL << (p - (start + 1)));
        }
    }

    // Parse buttons
    char *curr = end + 1;
    while ((start = strchr(curr, '(')) != NULL) {
        end = strchr(start, ')');
        if (!end) break;
        
        // Check if we hit the joltage part (starts with {)
        char *brace = strchr(curr, '{');
        if (brace && brace < start) break;

        if (m->num_buttons >= MAX_BUTTONS) {
            fprintf(stderr, "Too many buttons!\n");
            break;
        }

        // Parse numbers inside ()
        uint64_t mask = 0;
        char *nums_str = malloc(end - start);
        strncpy(nums_str, start + 1, end - start - 1);
        nums_str[end - start - 1] = '\0';

        char *token = strtok(nums_str, ",");
        while (token) {
            int bit = atoi(token);
            if (bit >= 64) {
                 fprintf(stderr, "Light index too high: %d\n", bit);
            } else {
                mask |= (1ULL << bit);
            }
            token = strtok(NULL, ",");
        }
        free(nums_str);

        m->buttons[m->num_buttons++] = mask;
        curr = end + 1;
    }
    return 1;
}

long solve_machine(Machine *m) {
    int n = m->num_buttons;
    long min_presses = -1;

    // Brute force all subsets
    // If n is large (e.g. > 20), this will be slow. 
    // Given the problem type, n is likely small.
    unsigned long long limit = 1ULL << n;
    
    for (unsigned long long i = 0; i < limit; i++) {
        uint64_t current_state = 0;
        int current_presses = 0;

        for (int b = 0; b < n; b++) {
            if ((i >> b) & 1) {
                current_state ^= m->buttons[b];
                current_presses++;
            }
        }

        if (current_state == m->target) {
            if (min_presses == -1 || current_presses < min_presses) {
                min_presses = current_presses;
            }
        }
    }
    
    return min_presses;
}

void solve() {
    FILE *fp = fopen("input.txt", "r");
    if (fp == NULL) {
        perror("Error opening input.txt");
        return;
    }

    char line[4096];
    long total_presses = 0;
    int count = 0;

    while (fgets(line, sizeof(line), fp)) {
        if (strlen(line) < 3) continue; // Skip empty lines
        Machine m;
        if (parse_line(line, &m)) {
            long res = solve_machine(&m);
            if (res != -1) {
                total_presses += res;
            } else {
                // If no solution found, maybe treat as 0 or error?
                // Problem implies there is a solution or we just sum minimums.
                // Assuming solvable.
                printf("No solution for line %d\n", count + 1);
            }
        }
        count++;
    }

    printf("Total minimum presses: %ld\n", total_presses);

    fclose(fp);
}

int main() {
    solve();
    return 0;
}

