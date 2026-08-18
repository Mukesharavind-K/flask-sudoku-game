"""
Baseline tests for sudoku_logic module.

Tests the core Sudoku logic functions:
- Board creation and copying
- Cell validation (is_safe)
- Board filling algorithm
- Puzzle generation
"""

import pytest
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sudoku_logic


class TestBoardCreation:
    """Tests for board creation functions."""
    
    def test_create_empty_board_dimensions(self):
        """
        Test: Empty board is 9x9
        
        An empty board should be created with dimensions 9x9 (SIZE x SIZE)
        and all cells should contain EMPTY (0).
        """
        board = sudoku_logic.create_empty_board()
        assert len(board) == 9
        assert all(len(row) == 9 for row in board)
        assert all(board[i][j] == 0 for i in range(9) for j in range(9))
    
    def test_create_empty_board_all_zeros(self):
        """
        Test: All cells in empty board are zero
        
        Every cell should be EMPTY (0) when first created.
        """
        board = sudoku_logic.create_empty_board()
        for row in board:
            for cell in row:
                assert cell == sudoku_logic.EMPTY


class TestDeepCopy:
    """Tests for board copying functionality."""
    
    def test_deep_copy_creates_independent_copy(self):
        """
        Test: Deep copy creates independent copy
        
        Modifying the copied board should not affect the original board.
        """
        original = sudoku_logic.create_empty_board()
        original[0][0] = 5
        
        copied = sudoku_logic.deep_copy(original)
        copied[0][0] = 7
        
        assert original[0][0] == 5
        assert copied[0][0] == 7
    
    def test_deep_copy_has_same_values(self):
        """
        Test: Deep copy initially has same values
        
        A newly created copy should have the same values as the original
        before any modifications.
        """
        original = sudoku_logic.create_empty_board()
        original[2][3] = 8
        original[5][7] = 3
        
        copied = sudoku_logic.deep_copy(original)
        
        assert copied[2][3] == 8
        assert copied[5][7] == 3


class TestIsSafe:
    """Tests for the is_safe validation function."""
    
    def test_is_safe_empty_board_all_numbers_valid(self):
        """
        Test: All numbers are valid on empty board
        
        On an empty board, any number 1-9 should be safe to place in any cell.
        """
        board = sudoku_logic.create_empty_board()
        for num in range(1, 10):
            assert sudoku_logic.is_safe(board, 0, 0, num) is True
    
    def test_is_safe_rejects_duplicate_in_row(self):
        """
        Test: Rejects duplicate number in same row
        
        is_safe should return False when trying to place a number that
        already exists in the same row.
        """
        board = sudoku_logic.create_empty_board()
        board[0][0] = 5
        assert sudoku_logic.is_safe(board, 0, 5, 5) is False
    
    def test_is_safe_rejects_duplicate_in_column(self):
        """
        Test: Rejects duplicate number in same column
        
        is_safe should return False when trying to place a number that
        already exists in the same column.
        """
        board = sudoku_logic.create_empty_board()
        board[0][0] = 5
        assert sudoku_logic.is_safe(board, 5, 0, 5) is False
    
    def test_is_safe_rejects_duplicate_in_3x3_box(self):
        """
        Test: Rejects duplicate number in 3x3 box
        
        is_safe should return False when trying to place a number that
        already exists in the same 3x3 box.
        """
        board = sudoku_logic.create_empty_board()
        board[0][0] = 5
        # Try to place 5 in the same 3x3 box (rows 0-2, cols 0-2)
        assert sudoku_logic.is_safe(board, 1, 1, 5) is False
    
    def test_is_safe_allows_different_number_in_row(self):
        """
        Test: Allows different number in same row
        
        is_safe should return True when placing a different number
        in the same row.
        """
        board = sudoku_logic.create_empty_board()
        board[0][0] = 5
        assert sudoku_logic.is_safe(board, 0, 5, 3) is True
    
    def test_is_safe_allows_same_number_different_box(self):
        """
        Test: Allows same number in different 3x3 box
        
        The same number can appear in different 3x3 boxes.
        """
        board = sudoku_logic.create_empty_board()
        board[0][0] = 5  # Top-left 3x3 box
        # Try to place 5 in a different 3x3 box (rows 3-5, cols 3-5)
        assert sudoku_logic.is_safe(board, 3, 3, 5) is True


class TestFillBoard:
    """Tests for the board filling algorithm."""
    
    def test_fill_board_returns_true_on_success(self):
        """
        Test: fill_board returns True on successful completion
        
        When fill_board successfully completes, it should return True.
        """
        board = sudoku_logic.create_empty_board()
        result = sudoku_logic.fill_board(board)
        assert result is True
    
    def test_fill_board_all_cells_filled(self):
        """
        Test: All cells are filled after fill_board
        
        After fill_board completes, every cell should contain a number 1-9,
        not EMPTY (0).
        """
        board = sudoku_logic.create_empty_board()
        sudoku_logic.fill_board(board)
        
        for i in range(9):
            for j in range(9):
                assert board[i][j] != sudoku_logic.EMPTY
                assert 1 <= board[i][j] <= 9
    
    def test_fill_board_valid_sudoku(self):
        """
        Test: Filled board is a valid Sudoku solution
        
        After fill_board completes, all rows, columns, and 3x3 boxes
        should have no duplicates (valid Sudoku).
        """
        board = sudoku_logic.create_empty_board()
        sudoku_logic.fill_board(board)
        
        # Check rows have no duplicates
        for row in board:
            assert len(set(row)) == 9
        
        # Check columns have no duplicates
        for col in range(9):
            column = [board[row][col] for row in range(9)]
            assert len(set(column)) == 9
        
        # Check 3x3 boxes have no duplicates
        for box_row in range(3):
            for box_col in range(3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(board[box_row * 3 + i][box_col * 3 + j])
                assert len(set(box)) == 9


class TestCountSolutions:
    """Tests for the solution counter function."""
    
    def test_count_solutions_complete_board_has_one_solution(self):
        """
        Test: Completely filled board has exactly one solution
        
        A valid, completely filled Sudoku board should have
        exactly one solution (itself).
        """
        # Generate a complete valid board
        board = sudoku_logic.create_empty_board()
        sudoku_logic.fill_board(board)
        
        # Count solutions
        solution_count = sudoku_logic.count_solutions(board)
        assert solution_count == 1
    
    def test_count_solutions_one_empty_cell_one_solution(self):
        """
        Test: Board with one empty cell has exactly one solution
        
        When a valid Sudoku has exactly one empty cell,
        there should be exactly one number that can fill it.
        """
        # Generate a complete valid board
        board = sudoku_logic.create_empty_board()
        sudoku_logic.fill_board(board)
        
        # Blank one cell
        board[0][0] = sudoku_logic.EMPTY
        
        # Should have one solution
        solution_count = sudoku_logic.count_solutions(board)
        assert solution_count == 1
    
    def test_count_solutions_ambiguous_board_returns_two(self):
        """
        Test: Ambiguous board with multiple solutions returns 2
        
        A board with multiple valid solutions should return 2
        (stops searching after finding 2, doesn't count all).
        """
        # Create an ambiguous board with multiple solutions
        # Example: 2x2 cells in top-left filled, rest empty
        board = sudoku_logic.create_empty_board()
        board[0][0] = 1
        board[0][1] = 2
        board[1][0] = 3
        board[1][1] = 4
        
        # This board has multiple solutions
        solution_count = sudoku_logic.count_solutions(board)
        assert solution_count == 2  # At least 2 solutions
    
    def test_count_solutions_invalid_board_returns_zero(self):
        """
        Test: Invalid board with contradictions has no solutions
        
        A board with impossible constraints (e.g., duplicate in row)
        should have zero solutions.
        """
        # Create an invalid board by filling most of it validly,
        # then creating a contradiction
        board = sudoku_logic.create_empty_board()
        sudoku_logic.fill_board(board)
        # Now create a contradiction by setting two cells in same row to same value
        board[0][0] = 5
        board[0][1] = 5  # Duplicate in same row - now invalid
        
        # Should have zero solutions
        solution_count = sudoku_logic.count_solutions(board)
        assert solution_count == 0


class TestGeneratePuzzle:
    """Tests for the puzzle generation function."""
    
    def test_generate_puzzle_returns_tuple(self):
        """
        Test: generate_puzzle returns a tuple
        
        generate_puzzle should return a tuple of (puzzle, solution).
        """
        result = sudoku_logic.generate_puzzle()
        assert isinstance(result, tuple)
        assert len(result) == 2
    
    def test_generate_puzzle_default_clues(self):
        """
        Test: Default puzzle has 35 clues
        
        When called without arguments, generate_puzzle should create
        a puzzle with 35 clues (35 non-empty cells).
        """
        puzzle, solution = sudoku_logic.generate_puzzle()
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 35
    
    def test_generate_puzzle_custom_clues(self):
        """
        Test: Custom clue count is respected
        
        When called with a custom clue count, the puzzle should have
        that many clues.
        """
        clues = 40
        puzzle, solution = sudoku_logic.generate_puzzle(clues=clues)
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == clues
    
    def test_generate_puzzle_solution_is_valid(self):
        """
        Test: Generated solution is a valid Sudoku
        
        The solution returned should be a completely filled valid Sudoku board.
        """
        puzzle, solution = sudoku_logic.generate_puzzle()
        
        # Check solution is completely filled
        for row in solution:
            assert all(cell != 0 for cell in row)
        
        # Check solution is valid (no duplicates in rows)
        for row in solution:
            assert len(set(row)) == 9
    
    def test_generate_puzzle_clues_are_correct(self):
        """
        Test: Puzzle clues match solution values
        
        Every clue in the puzzle should match the corresponding cell
        in the solution.
        """
        puzzle, solution = sudoku_logic.generate_puzzle()
        
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:  # If there's a clue
                    assert puzzle[i][j] == solution[i][j]
    
    def test_generate_puzzle_puzzle_has_empty_cells(self):
        """
        Test: Puzzle has empty cells
        
        The puzzle should have some empty cells (not completely filled).
        """
        puzzle, solution = sudoku_logic.generate_puzzle(clues=35)
        has_empty = any(cell == 0 for row in puzzle for cell in row)
        assert has_empty is True
    
    def test_generate_puzzle_puzzle_less_than_solution(self):
        """
        Test: Puzzle has fewer clues than solution
        
        The puzzle should have fewer filled cells than the complete solution.
        """
        puzzle, solution = sudoku_logic.generate_puzzle(clues=35)
        
        puzzle_clues = sum(1 for row in puzzle for cell in row if cell != 0)
        solution_clues = sum(1 for row in solution for cell in row if cell != 0)
        
        assert puzzle_clues < solution_clues
        assert puzzle_clues == 35
        assert solution_clues == 81
    
    def test_generate_puzzle_30_clues_unique_solution(self):
        """
        Test: Generated puzzle with 30 clues has exactly one solution
        
        A puzzle with 30 clues should have a unique solution.
        """
        puzzle, solution = sudoku_logic.generate_puzzle(clues=30)
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 30
        assert sudoku_logic.count_solutions(puzzle) == 1
    
    def test_generate_puzzle_35_clues_unique_solution(self):
        """
        Test: Generated puzzle with 35 clues has exactly one solution
        
        A puzzle with 35 clues should have a unique solution.
        """
        puzzle, solution = sudoku_logic.generate_puzzle(clues=35)
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 35
        assert sudoku_logic.count_solutions(puzzle) == 1
    
    def test_generate_puzzle_40_clues_unique_solution(self):
        """
        Test: Generated puzzle with 40 clues has exactly one solution
        
        A puzzle with 40 clues should have a unique solution.
        """
        puzzle, solution = sudoku_logic.generate_puzzle(clues=40)
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 40
        assert sudoku_logic.count_solutions(puzzle) == 1
    
    def test_multiple_generated_puzzles_all_unique(self):
        """
        Test: Multiple generated puzzles all have unique solutions
        
        Each generated puzzle should have exactly one solution.
        """
        for _ in range(3):
            puzzle, solution = sudoku_logic.generate_puzzle(clues=35)
            assert sudoku_logic.count_solutions(puzzle) == 1
