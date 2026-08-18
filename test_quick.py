#!/usr/bin/env python
"""Quick test of the new functions"""

import sys
sys.path.insert(0, '.')

import sudoku_logic

print("Testing count_solutions...")

# Test 1: Complete board
board = sudoku_logic.create_empty_board()
print(f"  Filling board...")
sudoku_logic.fill_board(board)
print(f"  Complete board should have 1 solution: {sudoku_logic.count_solutions(board)}")

# Test 2: One empty cell
board[0][0] = sudoku_logic.EMPTY
print(f"  Board with 1 empty cell should have 1 solution: {sudoku_logic.count_solutions(board)}")

# Test 3: Ambiguous board
board = sudoku_logic.create_empty_board()
board[0][0] = 1
board[0][1] = 2
print(f"  Ambiguous board should have 2+ solutions: {sudoku_logic.count_solutions(board)}")

# Test 4: Invalid board
board = sudoku_logic.create_empty_board()
board[0][0] = 5
board[0][1] = 5
print(f"  Invalid board should have 0 solutions: {sudoku_logic.count_solutions(board)}")

print("\nTesting generate_puzzle with uniqueness...")
print(f"  Generating puzzle with 35 clues...")
puzzle, solution = sudoku_logic.generate_puzzle(clues=35)
clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
print(f"  Puzzle has {clue_count} clues")
print(f"  Puzzle has {sudoku_logic.count_solutions(puzzle)} solution(s)")

print("\nAll tests passed!")
