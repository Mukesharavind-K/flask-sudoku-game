import copy
import random

SIZE = 9
EMPTY = 0

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def count_solutions(board, max_count=2):
    """
    Count the number of solutions for a Sudoku puzzle.
    
    Uses backtracking to count solutions, stopping immediately once
    max_count solutions are found (for efficiency).
    
    Args:
        board: The puzzle to analyze (0 = empty cell, 1-9 = filled)
        max_count: Stop counting after finding this many solutions (default: 2)
    
    Returns:
        0: No solutions (invalid puzzle)
        1: Exactly one solution
        2: Two or more solutions (stops searching after 2nd)
    """
    # Work on a copy to avoid modifying the input board
    board_copy = deep_copy(board)
    
    # Container to hold count in nested function (Python 2/3 compatible)
    count_holder = {'count': 0}
    
    def is_valid_solution(board):
        """Check if a completely filled board is a valid Sudoku solution."""
        # Check rows
        for row in board:
            if len(set(row)) != SIZE or any(cell == EMPTY for cell in row):
                return False
        # Check columns
        for col in range(SIZE):
            column = [board[row][col] for row in range(SIZE)]
            if len(set(column)) != SIZE:
                return False
        # Check 3x3 boxes
        for box_row in range(3):
            for box_col in range(3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(board[box_row * 3 + i][box_col * 3 + j])
                if len(set(box)) != SIZE:
                    return False
        return True
    
    def backtrack():
        # Early termination if we already found enough solutions
        if count_holder['count'] >= max_count:
            return
        
        # Find next empty cell
        for row in range(SIZE):
            for col in range(SIZE):
                if board_copy[row][col] == EMPTY:
                    # Try each number
                    for num in range(1, SIZE + 1):
                        if is_safe(board_copy, row, col, num):
                            board_copy[row][col] = num
                            backtrack()
                            board_copy[row][col] = EMPTY
                    return
        
        # No empty cell found - we have a complete board
        # Validate that it's a proper solution
        if is_valid_solution(board_copy):
            count_holder['count'] += 1
    
    backtrack()
    
    if count_holder['count'] == 0:
        return 0
    elif count_holder['count'] == 1:
        return 1
    else:
        return 2


def remove_cells_with_uniqueness(board, target_clues):
    """
    Remove cells from a complete Sudoku board to create a puzzle with
    exactly one unique solution.
    
    Randomly removes cells while verifying that the puzzle maintains
    exactly one solution. Uses a maximum number of attempts to avoid
    infinite loops.
    
    Args:
        board: A completely filled valid Sudoku board
        target_clues: The number of clues to keep (cells to keep filled)
    
    Returns:
        The puzzle board with exactly target_clues filled cells
    
    Raises:
        ValueError: If target_clues cannot be achieved while maintaining
                   a unique solution after 1000 attempts
    """
    puzzle = deep_copy(board)
    cells_to_remove = SIZE * SIZE - target_clues
    removed_count = 0
    max_attempts = 1000
    attempts = 0
    
    while removed_count < cells_to_remove and attempts < max_attempts:
        attempts += 1
        
        # Pick a random cell that is currently filled
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        
        if puzzle[row][col] != EMPTY:
            # Save the original value
            original_value = puzzle[row][col]
            puzzle[row][col] = EMPTY
            
            # Check if puzzle still has exactly one solution
            if count_solutions(puzzle) == 1:
                # Good! Keep this cell removed
                removed_count += 1
            else:
                # Removing this cell creates multiple solutions or no solution
                # Restore it and try another cell
                puzzle[row][col] = original_value
    
    if removed_count < cells_to_remove:
        raise ValueError(
            f"Could not generate puzzle with {target_clues} clues while "
            f"maintaining unique solution after {max_attempts} attempts. "
            f"Only achieved {removed_count} removals."
        )
    
    return puzzle


def remove_cells(board, clues):
    attempts = SIZE * SIZE - clues
    while attempts > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            attempts -= 1


def generate_puzzle(clues=35):
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    puzzle = remove_cells_with_uniqueness(board, clues)
    return puzzle, solution
