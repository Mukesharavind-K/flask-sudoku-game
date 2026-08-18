#!/usr/bin/env python
"""Simple verification that the code is syntactically correct"""

import sys
import os

# Change to the project directory
os.chdir(r'c:\Users\Admin\github-copilot-python\starter')
sys.path.insert(0, '.')

print("=" * 70)
print("VERIFICATION SCRIPT - Testing Implementation")
print("=" * 70)

# Step 1: Import the module
print("\n[1] Importing sudoku_logic module...")
try:
    import sudoku_logic
    print("    ✓ Module imported successfully")
except Exception as e:
    print(f"    ✗ Import failed: {e}")
    sys.exit(1)

# Step 2: Verify functions exist
print("\n[2] Verifying functions exist...")
functions = ['count_solutions', 'remove_cells_with_uniqueness', 'generate_puzzle']
for func_name in functions:
    if hasattr(sudoku_logic, func_name):
        print(f"    ✓ {func_name}() exists")
    else:
        print(f"    ✗ {func_name}() NOT FOUND")

# Step 3: Test count_solutions with complete board
print("\n[3] Testing count_solutions() with complete board...")
try:
    board = sudoku_logic.create_empty_board()
    sudoku_logic.fill_board(board)
    result = sudoku_logic.count_solutions(board)
    print(f"    Solution count: {result}")
    if result == 1:
        print("    ✓ Complete board correctly has 1 solution")
    else:
        print(f"    ✗ Expected 1, got {result}")
except Exception as e:
    print(f"    ✗ Error: {e}")

# Step 4: Test generate_puzzle
print("\n[4] Testing generate_puzzle() with 35 clues...")
try:
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)
    clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
    print(f"    Clues generated: {clue_count}")
    print(f"    Testing uniqueness (this may take 30-60 seconds)...")
    solution_count = sudoku_logic.count_solutions(puzzle)
    print(f"    Solution count: {solution_count}")
    if clue_count == 35 and solution_count == 1:
        print("    ✓ Puzzle has 35 clues with unique solution")
    else:
        print(f"    ✗ Expected 35 clues and 1 solution, got {clue_count} and {solution_count}")
except Exception as e:
    print(f"    ✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)
