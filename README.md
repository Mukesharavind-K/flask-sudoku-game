# Sudoku Flask Application

A Flask-based Sudoku puzzle generator and validator.

## Features

- Generate random Sudoku puzzles with configurable difficulty (number of clues)
- Validate user solutions against the generated solution
- Web-based interface for playing Sudoku

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the Flask development server:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Running Tests

This project uses **pytest** for testing. The baseline test suite contains **35 passing tests** covering:

- Sudoku logic validation and board generation
- Flask route functionality and HTTP responses

To run the complete test suite:

```bash
pytest -v
```

The `-v` flag provides verbose output showing each test result.

## Project Structure

- `app.py` - Flask application and routes
- `sudoku_logic.py` - Core Sudoku game logic
- `requirements.txt` - Project dependencies
- `tests/` - Test suite with pytest tests
  - `test_sudoku_logic.py` - Tests for Sudoku logic
  - `test_app.py` - Tests for Flask routes
  - `conftest.py` - Pytest configuration and fixtures
- `templates/` - HTML templates
- `static/` - CSS and JavaScript files
