from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    # Map difficulty to clue counts
    difficulty_map = {
        'easy': 40,
        'medium': 35,
        'hard': 30
    }
    
    # Get difficulty parameter (case-insensitive), default to 'medium'
    difficulty = request.args.get('difficulty', 'medium').lower()
    
    # Get clue count from difficulty, or use explicit clues parameter if provided
    if 'clues' in request.args:
        # Explicit clues parameter takes precedence (backward compatibility)
        clues = int(request.args.get('clues'))
    else:
        # Use difficulty mapping, default to medium if invalid
        clues = difficulty_map.get(difficulty, 35)
    
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle, 'solution': solution})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})

if __name__ == '__main__':
    app.run(debug=True)