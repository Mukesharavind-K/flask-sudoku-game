# Copilot Instructions — Sudoku Flask Application

## 1. Project Overview

This project is a Flask-based Sudoku application written in Python. The application generates Sudoku puzzles, validates solutions, and provides a web-based interface for playing the game.

The project is organized so that:

* `app.py` contains the Flask application and HTTP routes.
* `sudoku_logic.py` contains the core Sudoku generation, validation, solving, and uniqueness logic.
* `templates/` contains the HTML templates for the web interface.
* `static/` contains CSS and JavaScript files used by the frontend.
* `tests/` contains automated tests for the Sudoku logic and Flask routes.
* `requirements.txt` contains the required Python dependencies.
* `README.md` contains installation, execution, testing, and project structure information.

Copilot should preserve this architecture instead of unnecessarily moving logic between files.

---

## 2. Coding Style

Follow clean, readable, and maintainable Python code.

### Python Naming Conventions

* Use `snake_case` for functions and variables.
* Use `UPPER_CASE` for constants.
* Use descriptive names instead of short or ambiguous variable names.
* Use clear function names that describe their purpose.

Examples:

```python
def generate_puzzle(clues=35):
    ...
```

```python
SIZE = 9
EMPTY = 0
```

Avoid unclear names such as:

```python
def f(x):
    ...
```

unless the variable is used only in a very small and obvious scope.

### Formatting

* Follow standard Python formatting conventions.
* Use consistent indentation.
* Keep functions focused on one responsibility.
* Add comments when logic is non-obvious.
* Avoid unnecessary duplicate code.
* Preserve existing comments when they explain important project behavior.
* Prefer readable code over unnecessarily compact code.

---

## 3. Flask Architecture

The project uses Flask as its web framework.

The Flask application should remain in `app.py`.

Routes should:

* Receive HTTP requests.
* Validate request data where necessary.
* Call appropriate functions from `sudoku_logic.py`.
* Return HTML or JSON responses.
* Avoid containing complex Sudoku-solving algorithms directly.

The Sudoku algorithms should remain in `sudoku_logic.py`.

For example, the `/new` route should obtain the requested difficulty, determine the required clue count, generate the puzzle, store the current puzzle and solution, and return the required data.

The existing difficulty mapping is:

* Easy: 40 clues
* Medium: 35 clues
* Hard: 30 clues

Do not change these values unless the project requirements explicitly require different values.

---

## 4. Sudoku Logic Rules

The Sudoku board is a standard 9 × 9 Sudoku grid.

The project uses:

```python
SIZE = 9
EMPTY = 0
```

Sudoku rules must always be respected:

* Each row must contain numbers 1–9 without duplicates.
* Each column must contain numbers 1–9 without duplicates.
* Each 3 × 3 box must contain numbers 1–9 without duplicates.
* Empty cells are represented by `0`.

The existing `is_safe()` function should be reused for Sudoku validity checks instead of creating duplicate validation logic.

---

## 5. Puzzle Generation

Puzzles should be generated from a complete valid Sudoku board.

The project uses:

1. An empty 9 × 9 board.
2. A backtracking algorithm to fill the board.
3. A copy of the completed board as the solution.
4. Controlled cell removal to create the playable puzzle.
5. Solution counting to ensure the generated puzzle has exactly one solution.

The existing `generate_puzzle()` function should remain the main entry point for puzzle generation.

Do not replace the uniqueness-based generation process with simple random cell removal.

The existing project includes `remove_cells_with_uniqueness()`, which removes cells only when the resulting puzzle continues to have exactly one solution.

---

## 6. Unique Solution Requirement

Every generated Sudoku puzzle must have exactly one valid solution.

Use the existing:

```python
count_solutions()
```

function to verify uniqueness.

The function uses a maximum solution count of 2 so that it can distinguish between:

* `0` → no valid solution
* `1` → exactly one valid solution
* `2` → two or more solutions

Do not treat a puzzle with multiple solutions as valid.

When modifying puzzle-generation logic, maintain the uniqueness guarantee.

---

## 7. Difficulty Requirement

The application must support three difficulty levels:

* Easy
* Medium
* Hard

Difficulty should control the number of pre-filled cells.

The current project uses:

```text
Easy   = 40 clues
Medium = 35 clues
Hard   = 30 clues
```

The frontend should send the selected difficulty to the Flask backend.

The backend should determine the appropriate clue count and generate a new puzzle.

Do not allow difficulty selection to modify the underlying Sudoku rules.

---

## 8. Frontend Requirements

The frontend should provide a clear and responsive Sudoku interface.

The interface should support:

* Sudoku board
* Difficulty selector
* New Game functionality
* Hint button
* Check button
* Timer
* Dark Mode toggle
* Player name input where required
* Completion message
* Top 10 leaderboard

The UI must work on both desktop and mobile screen sizes.

The Sudoku board should remain usable on smaller screens without causing horizontal overflow.

---

## 9. Sudoku Board Styling

The Sudoku board must visually distinguish the nine 3 × 3 boxes.

Use alternating styling for the 3 × 3 Sudoku squares so that the board structure is immediately understandable.

Ensure that:

* Cell borders are clear.
* Numbers are easy to read.
* Selected cells are visually distinguishable.
* Fixed/pre-filled cells are visually distinguishable from user-entered cells.
* Hint-filled cells remain locked.
* Incorrect entries can be clearly highlighted.
* The board remains readable in both light and dark modes.

---

## 10. Hint Functionality

The Hint button must fill one currently empty cell with the correct value from the puzzle's solution.

A hinted cell must become locked so that the player cannot edit it afterward.

The hint must:

* Use the current puzzle solution.
* Fill only an appropriate empty cell.
* Never insert an incorrect value.
* Mark the cell as fixed/locked after the hint.
* Provide clear visual feedback to the player.

Do not expose the complete solution to the player through the UI.

---

## 11. Check Functionality

The Check button should compare the player's current entries against the correct solution.

Incorrect entries should be highlighted clearly.

Correct entries should not be incorrectly marked as errors.

The check operation should not automatically reveal the complete solution.

The backend already provides a `/check` endpoint that compares the submitted board against the current solution. Preserve this behavior when extending the application. 

---

## 12. Immediate Move Validation

The application should provide immediate feedback when a player enters an invalid Sudoku move.

A move should be considered invalid when it violates the Sudoku rules for:

* The current row
* The current column
* The current 3 × 3 box

Invalid entries should receive clear visual feedback.

Immediate validation should improve the user experience without automatically solving the puzzle.

---

## 13. Timer

The game must include a timer that tracks how long the player takes to solve the current puzzle.

The timer should:

* Start when a new puzzle begins.
* Continue while the player is solving.
* Stop when the puzzle is successfully completed.
* Reset when a new puzzle starts.
* Record the final solving time for the leaderboard.

Do not use the timer value as the source of truth for Sudoku correctness.

---

## 14. Dark Mode

Provide a Dark Mode toggle.

Dark Mode must update the complete application interface rather than only the Sudoku board.

Ensure that the following remain readable in dark mode:

* Text
* Buttons
* Sudoku cells
* Borders
* Input fields
* Difficulty selector
* Timer
* Messages
* Leaderboard

The styling should remain consistent between light and dark themes.

---

## 15. Completion Handling

When the player correctly completes the Sudoku:

1. Verify that the board is a valid complete Sudoku solution.
2. Stop the timer.
3. Display a clear completion message.
4. Record the player's name, solving time, and difficulty.
5. Update the Top 10 leaderboard.

Do not display a successful completion message when the board contains incorrect or incomplete values.

---

## 16. Top 10 Leaderboard

The application must maintain a Top 10 list using browser `localStorage`.

Each leaderboard entry should contain:

* Player name
* Solving time
* Difficulty level

The leaderboard should:

* Persist after refreshing the browser.
* Sort players by solving time.
* Keep only the best 10 results.
* Preserve the difficulty associated with each result.
* Update after successful puzzle completion.

Do not use server-side storage when the project requirement specifically calls for browser `localStorage`.

---

## 17. JavaScript Guidelines

Frontend game behavior should be implemented in the project's JavaScript files under `static/`.

JavaScript should be responsible for client-side interactions such as:

* Updating the Sudoku board.
* Handling cell input.
* Difficulty selection.
* Timer management.
* Hint interactions.
* Check interactions.
* Dark Mode.
* Immediate validation.
* Completion detection.
* Local-storage leaderboard management.

Avoid placing large amounts of JavaScript directly inside HTML when the functionality can be maintained in the project's JavaScript file.

---

## 18. CSS Guidelines

Keep application styling in the project's CSS files under `static/`.

CSS should:

* Use consistent spacing.
* Use readable typography.
* Provide responsive layouts.
* Support both light and dark themes.
* Clearly distinguish Sudoku 3 × 3 boxes.
* Provide visible states for selected, fixed, hinted, and incorrect cells.
* Keep controls usable on mobile devices.

Avoid hard-coded dimensions that make the Sudoku board unusable on smaller screens.

---

## 19. Testing Requirements

Changes to Sudoku logic should be tested before submission.

The project already includes tests for important Sudoku behavior, including:

* Complete board solution counting.
* Boards with one empty cell.
* Ambiguous boards.
* Invalid boards.
* Puzzle generation.
* Puzzle clue count.
* Puzzle uniqueness.

The project specifically verifies that generated puzzles have the requested clue count and exactly one solution. 

When modifying existing functionality, do not remove existing tests just to make the test suite pass.

Add tests when introducing important new backend behavior.

---

## 20. Dependency Rules

Use only the libraries specified by the project unless a new dependency is genuinely required.

The current project dependencies include:

```text
Flask
pytest
pytest-flask
```

These dependencies are defined in `requirements.txt`. 

If a new dependency is required:

1. Add it to `requirements.txt`.
2. Make sure it is actually used by the project.
3. Ensure the application can be installed from a clean environment.
4. Update the README if installation instructions change.

Do not rely on packages that are installed only on the developer's computer.

---

## 21. File and Path Rules

The application must not depend on developer-specific absolute paths.

Avoid code such as:

```python
os.chdir(r"C:\Users\Admin\github-copilot-python\starter")
```

Project files should use relative paths or paths derived from the project directory.

The application must be capable of running after the project is downloaded or cloned onto another computer.

---

## 22. Copilot Instructions

When generating or modifying code, Copilot should:

* Understand the existing project structure before creating new files.
* Reuse existing functions where appropriate.
* Avoid unnecessary rewrites.
* Preserve working functionality.
* Follow the existing naming conventions.
* Keep Flask routes separate from Sudoku business logic.
* Keep frontend behavior in the appropriate JavaScript files.
* Keep styling in CSS files.
* Avoid introducing unnecessary dependencies.
* Add or update tests when backend behavior changes.
* Prefer simple, readable solutions.
* Explain significant changes when requested.
* Never remove a required feature without a clear reason.
* Never replace the unique-solution algorithm with an approach that does not guarantee uniqueness.

---

## 23. Copilot Prompt Examples

### Example 1 — Add a feature

> Add the requested Sudoku feature while preserving the existing Flask architecture. Keep Sudoku logic in `sudoku_logic.py`, frontend behavior in the JavaScript file, and styling in the CSS file. Do not introduce unnecessary dependencies.

### Example 2 — Modify puzzle difficulty

> Update the Sudoku difficulty handling while preserving the existing Easy, Medium, and Hard clue counts. Ensure every generated puzzle still has exactly one solution.

### Example 3 — Fix validation

> Improve Sudoku move validation without changing the existing puzzle-generation algorithm. Invalid moves should be detected immediately and clearly highlighted in the UI.

### Example 4 — Fix responsive styling

> Update the Sudoku CSS so that the board and controls work on desktop and mobile screens while preserving the existing light and dark themes.

### Example 5 — Add tests

> Add tests for the new functionality without removing existing tests. Verify both successful behavior and invalid input cases.

---

## 24. General Rule for Copilot

Before making changes, inspect the existing implementation and understand how the pieces interact.

Prioritize:

1. Correct functionality
2. Preservation of existing features
3. Unique Sudoku solutions
4. Clean and maintainable code
5. Responsive and accessible UI
6. Minimal dependencies
7. Testability

Any generated code should fit naturally into the existing Sudoku Flask application rather than replacing the project architecture unnecessarily.
