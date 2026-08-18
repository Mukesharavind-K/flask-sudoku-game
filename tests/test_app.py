"""
Baseline tests for Flask application routes.

Tests the Flask application routes:
- GET / (index page)
- GET /new (generate new puzzle)
- POST /check (check puzzle solution)
"""

import pytest
import sys
import os
import json

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, CURRENT
import sudoku_logic


class TestIndexRoute:
    """Tests for the index route."""
    
    def test_index_route_exists(self, client):
        """
        Test: Index route is accessible
        
        GET / should return a 200 status code.
        """
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_route_returns_html(self, client):
        """
        Test: Index route returns HTML content
        
        GET / should return HTML content (not JSON or empty).
        """
        response = client.get('/')
        assert response.status_code == 200
        assert response.content_type == 'text/html; charset=utf-8'


class TestNewGameRoute:
    """Tests for the new game generation route."""
    
    def test_new_game_route_returns_json(self, client):
        """
        Test: /new returns JSON response
        
        GET /new should return a JSON response.
        """
        response = client.get('/new')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_new_game_route_returns_puzzle(self, client):
        """
        Test: /new returns puzzle in response
        
        The response should contain a 'puzzle' key with a list of lists.
        """
        response = client.get('/new')
        data = json.loads(response.data)
        
        assert 'puzzle' in data
        assert isinstance(data['puzzle'], list)
        assert len(data['puzzle']) == 9
        assert all(len(row) == 9 for row in data['puzzle'])
    
    def test_new_game_route_returns_solution(self, client):
        """
        Test: /new returns solution in response
        
        The response should contain a 'solution' key with a complete valid sudoku board.
        """
        response = client.get('/new')
        data = json.loads(response.data)
        
        assert 'solution' in data
        assert isinstance(data['solution'], list)
        assert len(data['solution']) == 9
        assert all(len(row) == 9 for row in data['solution'])
        # Solution should be completely filled (no zeros)
        for row in data['solution']:
            for cell in row:
                assert cell != 0
    
    def test_new_game_default_clues_35(self, client):
        """
        Test: Default puzzle has 35 clues
        
        Without specifying clues parameter, puzzle should have 35 clues.
        """
        response = client.get('/new')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 35
    
    def test_new_game_custom_clues(self, client):
        """
        Test: Custom clue parameter is respected
        
        Passing clues=40 should generate puzzle with 40 clues.
        """
        response = client.get('/new?clues=40')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 40
    
    def test_new_game_stores_puzzle_in_current(self, client, app_context):
        """
        Test: /new stores puzzle in CURRENT state
        
        After calling /new, CURRENT['puzzle'] should be set.
        """
        response = client.get('/new')
        data = json.loads(response.data)
        
        assert CURRENT['puzzle'] is not None
        assert CURRENT['puzzle'] == data['puzzle']
    
    def test_new_game_stores_solution_in_current(self, client, app_context):
        """
        Test: /new stores solution in CURRENT state
        
        After calling /new, CURRENT['solution'] should be set.
        """
        response = client.get('/new')
        
        assert CURRENT['solution'] is not None
        assert len(CURRENT['solution']) == 9
        assert all(len(row) == 9 for row in CURRENT['solution'])
    
    def test_new_game_multiple_calls_different_puzzles(self, client, app_context):
        """
        Test: Multiple /new calls generate different puzzles
        
        Calling /new multiple times should generate different puzzles
        (due to randomization, with high probability).
        """
        response1 = client.get('/new')
        puzzle1 = json.loads(response1.data)['puzzle']
        
        response2 = client.get('/new')
        puzzle2 = json.loads(response2.data)['puzzle']
        
        # Puzzles should be different (with very high probability)
        assert puzzle1 != puzzle2
    
    def test_new_game_easy_difficulty_40_clues(self, client):
        """
        Test: Easy difficulty generates 40 clues
        
        When difficulty=easy, puzzle should have 40 clues.
        """
        response = client.get('/new?difficulty=easy')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 40
    
    def test_new_game_medium_difficulty_35_clues(self, client):
        """
        Test: Medium difficulty generates 35 clues
        
        When difficulty=medium, puzzle should have 35 clues.
        """
        response = client.get('/new?difficulty=medium')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 35
    
    def test_new_game_hard_difficulty_30_clues(self, client):
        """
        Test: Hard difficulty generates 30 clues
        
        When difficulty=hard, puzzle should have 30 clues.
        """
        response = client.get('/new?difficulty=hard')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 30
    
    def test_new_game_invalid_difficulty_defaults_to_medium(self, client):
        """
        Test: Invalid difficulty parameter defaults to medium (35 clues)
        
        When difficulty is invalid, should default to medium (35 clues).
        """
        response = client.get('/new?difficulty=impossible')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 35
    
    def test_new_game_difficulty_case_insensitive(self, client):
        """
        Test: Difficulty parameter is case insensitive
        
        EASY, Easy, and easy should all work the same.
        """
        response = client.get('/new?difficulty=EASY')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 40
    
    def test_new_game_clues_parameter_backward_compatible(self, client):
        """
        Test: Explicit clues parameter still works (backward compatibility)
        
        When clues parameter is provided, it should override difficulty.
        """
        response = client.get('/new?clues=45')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        clue_count = sum(1 for row in puzzle for cell in row if cell != 0)
        assert clue_count == 45
    
    def test_new_game_easy_has_unique_solution(self, client):
        """
        Test: Easy difficulty puzzle has unique solution
        
        A 40-clue puzzle should have exactly one solution.
        """
        response = client.get('/new?difficulty=easy')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        assert sudoku_logic.count_solutions(puzzle) == 1
    
    def test_new_game_hard_has_unique_solution(self, client):
        """
        Test: Hard difficulty puzzle has unique solution
        
        A 30-clue puzzle should have exactly one solution.
        """
        response = client.get('/new?difficulty=hard')
        data = json.loads(response.data)
        puzzle = data['puzzle']
        assert sudoku_logic.count_solutions(puzzle) == 1


class TestCheckSolutionRoute:
    """Tests for the check solution route."""
    
    def test_check_requires_post(self, client):
        """
        Test: /check requires POST method
        
        GET /check should not be allowed, only POST.
        """
        response = client.get('/check')
        assert response.status_code == 405  # Method Not Allowed
    
    def test_check_without_game_in_progress_error(self, client, app_context):
        """
        Test: /check returns error when no game in progress
        
        POST /check without a game should return error message and 400 status.
        """
        # Clear CURRENT state
        CURRENT['solution'] = None
        
        response = client.post('/check', json={'board': []})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_check_correct_solution_empty_incorrect(self, client, app_context):
        """
        Test: Correct solution returns empty incorrect list
        
        When the board matches the solution, incorrect should be empty.
        """
        # Generate a new game
        client.get('/new')
        solution = CURRENT['solution']
        
        # Submit the solution
        response = client.post('/check', json={'board': solution})
        data = json.loads(response.data)
        
        assert 'incorrect' in data
        assert data['incorrect'] == []
    
    def test_check_incorrect_solution_identifies_wrong_cells(self, client, app_context):
        """
        Test: Incorrect solution identifies wrong cells
        
        When the board has incorrect cells, they should be listed.
        """
        # Generate a new game
        client.get('/new')
        solution = CURRENT['solution']
        
        # Create a modified board (change first cell)
        board = [row[:] for row in solution]  # Deep copy
        original_value = board[0][0]
        board[0][0] = original_value + 1 if original_value < 9 else original_value - 1
        
        # Submit the modified board
        response = client.post('/check', json={'board': board})
        data = json.loads(response.data)
        
        assert 'incorrect' in data
        assert [0, 0] in data['incorrect']
    
    def test_check_multiple_incorrect_cells(self, client, app_context):
        """
        Test: Multiple incorrect cells are all identified
        
        When multiple cells are wrong, all should be listed in incorrect.
        """
        # Generate a new game
        client.get('/new')
        solution = CURRENT['solution']
        
        # Create a modified board (change multiple cells)
        board = [row[:] for row in solution]  # Deep copy
        board[0][0] = (board[0][0] % 9) + 1
        board[5][5] = (board[5][5] % 9) + 1
        
        # Submit the modified board
        response = client.post('/check', json={'board': board})
        data = json.loads(response.data)
        
        assert 'incorrect' in data
        assert [0, 0] in data['incorrect']
        assert [5, 5] in data['incorrect']
    
    def test_check_returns_json(self, client, app_context):
        """
        Test: /check returns JSON response
        
        The response should be valid JSON.
        """
        # Generate a new game first
        client.get('/new')
        solution = CURRENT['solution']
        
        response = client.post('/check', json={'board': solution})
        assert response.content_type == 'application/json'
        
        # Should be parseable JSON
        data = json.loads(response.data)
        assert isinstance(data, dict)
