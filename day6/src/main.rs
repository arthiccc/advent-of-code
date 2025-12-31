use std::fs;
use std::path::Path;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let input_path = Path::new("input.txt");
    let input = fs::read_to_string(input_path)?;

    let lines: Vec<&str> = input.lines().collect();
    if lines.is_empty() {
        return Ok(());
    }

    let max_len = lines.iter().map(|l| l.len()).max().unwrap_or(0);
    let grid: Vec<Vec<char>> = lines
        .iter()
        .map(|line| {
            let mut chars: Vec<char> = line.chars().collect();
            while chars.len() < max_len {
                chars.push(' ');
            }
            chars
        })
        .collect();

    let p1 = solve_part1(&grid);
    println!("Part 1 Grand Total: {}", p1);

    let p2 = solve_part2(&grid);
    println!("Part 2 Grand Total: {}", p2);

    Ok(())
}

fn solve_part1(grid: &[Vec<char>]) -> u64 {
    let rows = grid.len();
    let cols = grid[0].len();
    let mut grand_total: u64 = 0;
    let mut current_block_cols: Vec<usize> = Vec::new();

    // Scan Left to Right for Part 1 (natural reading order for horizontal numbers)
    for c in 0..cols {
        if is_col_empty(grid, c) {
            if !current_block_cols.is_empty() {
                grand_total += process_block_part1(grid, &current_block_cols);
                current_block_cols.clear();
            }
        } else {
            current_block_cols.push(c);
        }
    }
    if !current_block_cols.is_empty() {
        grand_total += process_block_part1(grid, &current_block_cols);
    }

    grand_total
}

fn solve_part2(grid: &[Vec<char>]) -> u64 {
    let rows = grid.len();
    let cols = grid[0].len();
    let mut grand_total: u64 = 0;
    let mut current_block_cols: Vec<usize> = Vec::new();

    // Scan Right to Left for Part 2
    for c in (0..cols).rev() {
        if is_col_empty(grid, c) {
            if !current_block_cols.is_empty() {
                grand_total += process_block_part2(grid, &current_block_cols);
                current_block_cols.clear();
            }
        } else {
            current_block_cols.push(c);
        }
    }
    if !current_block_cols.is_empty() {
        grand_total += process_block_part2(grid, &current_block_cols);
    }

    grand_total
}

fn is_col_empty(grid: &[Vec<char>], col: usize) -> bool {
    for r in 0..grid.len() {
        if grid[r][col] != ' ' {
            return false;
        }
    }
    true
}

fn process_block_part1(grid: &[Vec<char>], col_indices: &[usize]) -> u64 {
    let mut numbers: Vec<u64> = Vec::new();
    let mut operator: Option<char> = None;

    for r in 0..grid.len() {
        let mut row_str = String::new();
        for &c in col_indices {
            row_str.push(grid[r][c]);
        }
        
        let mut current_num_str = String::new();
        for ch in row_str.chars() {
            if ch.is_ascii_digit() {
                current_num_str.push(ch);
            } else {
                if !current_num_str.is_empty() {
                    if let Ok(n) = current_num_str.parse::<u64>() {
                        numbers.push(n);
                    }
                    current_num_str.clear();
                }
                if ch == '+' || ch == '*' {
                    operator = Some(ch);
                }
            }
        }
        if !current_num_str.is_empty() {
             if let Ok(n) = current_num_str.parse::<u64>() {
                numbers.push(n);
            }
        }
    }

    calculate(numbers, operator)
}

fn process_block_part2(grid: &[Vec<char>], col_indices: &[usize]) -> u64 {
    let mut numbers: Vec<u64> = Vec::new();
    let mut operator: Option<char> = None;

    for &c in col_indices {
        let mut col_digits = String::new();
        for r in 0..grid.len() {
            let ch = grid[r][c];
            if ch.is_ascii_digit() {
                col_digits.push(ch);
            } else if ch == '+' || ch == '*' {
                operator = Some(ch);
            }
        }
        if !col_digits.is_empty() {
            if let Ok(n) = col_digits.parse::<u64>() {
                numbers.push(n);
            }
        }
    }

    calculate(numbers, operator)
}

fn calculate(numbers: Vec<u64>, operator: Option<char>) -> u64 {
    if numbers.is_empty() {
        return 0;
    }
    let op = operator.unwrap_or('+');
    let mut res = numbers[0];
    for &num in &numbers[1..] {
        match op {
            '+' => res += num,
            '*' => res *= num,
            _ => {},
        }
    }
    res
}