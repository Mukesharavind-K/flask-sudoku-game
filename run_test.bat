@echo off
cd /d "c:\Users\Admin\github-copilot-python\starter"
echo Running pytest...
python -m pytest tests/test_sudoku_logic.py::TestCountSolutions::test_count_solutions_complete_board_has_one_solution -v > pytest_output.log 2>&1
echo Test run completed
echo Output written to pytest_output.log
type pytest_output.log
