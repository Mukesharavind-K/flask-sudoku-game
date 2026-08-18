#!/usr/bin/env python
"""Direct test with file output"""

import sys
sys.path.insert(0, '.')

with open('test_results.txt', 'w') as f:
    f.write("Starting tests...\n")
    
    try:
        import sudoku_logic
        f.write("✓ Module imported successfully\n\n")
        
        # Test 1
        f.write("Test 1: Complete board should have 1 solution\n")
        board = sudoku_logic.create_empty_board()
        sudoku_logic.fill_board(board)
        result = sudoku_logic.count_solutions(board)
        f.write(f"  Result: {result}\n")
        f.write(f"  Status: {'PASS' if result == 1 else 'FAIL'}\n\n")
        
        # Test 2
        f.write("Test 2: Board with 1 empty cell should have 1 solution\n")
        board[0][0] = sudoku_logic.EMPTY
        result = sudoku_logic.count_solutions(board)
        f.write(f"  Result: {result}\n")
        f.write(f"  Status: {'PASS' if result == 1 else 'FAIL'}\n\n")
        
        # Test 3
        f.write("Test 3: Ambiguous board should have 2+ solutions\n")
        board = sudoku_logic.create_empty_board()
        board[0][0] = 1
        board[0][1] = 2
        result = sudoku_logic.count_solutions(board)
        f.write(f"  Result: {result}\n")
        f.write(f"  Status: {'PASS' if result == 2 else 'FAIL'}\n\n")
        
        # Test 4
        f.write("Test 4: Invalid board should have 0 solutions\n")
        board = sudoku_logic.create_empty_board()
        board[0][0] = 5
        board[0][1] = 5
        result = sudoku_logic.count_solutions(board)
        f.write(f"  Result: {result}\n")
        f.write(f"  Status: {'PASS' if result == 0 else 'FAIL'}\n\n")
        
        # Test 5
        f.write("Test 5: Generate puzzle with 35 clues\n")
        puzzle, solution = sudoku_logic.generate_puzzle(clues=35)
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        f.write(f"  Clues in puzzle: {clue_count}\n")
        solution_count = sudoku_logic.count_solutions(puzzle)
        f.write(f"  Solutions: {solution_count}\n")
        f.write(f"  Status: {'PASS' if clue_count == 35 and solution_count == 1 else 'FAIL'}\n\n")
        
        f.write("All manual tests completed!\n")
    except Exception as e:
        f.write(f"ERROR: {e}\n")
        import traceback
        f.write(traceback.format_exc())

print("Test results written to test_results.txt")
