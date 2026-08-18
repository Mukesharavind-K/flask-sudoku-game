// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const BOX_SIZE = 3;
let puzzle = [];
let solution = [];
let currentDifficulty = 'medium';
let hintsUsed = 0;
let timerIntervalId = null;
let elapsedSeconds = 0;
let isTimerRunning = false;
let scores = [];
let puzzleCompleted = false;
let currentTheme = 'light';

/**
 * Get the current board state from the DOM (all user entries + prefilled values)
 * @returns {Array} 9x9 board array where 0 = empty
 */
function getCurrentBoard() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  return board;
}

/**
 * Check if a value exists in the row (excluding the current cell)
 * @returns {boolean} true if duplicate exists
 */
function hasRowConflict(row, col, value, board) {
  for (let j = 0; j < SIZE; j++) {
    if (j !== col && board[row][j] === value) {
      return true;
    }
  }
  return false;
}

/**
 * Check if a value exists in the column (excluding the current cell)
 * @returns {boolean} true if duplicate exists
 */
function hasColumnConflict(row, col, value, board) {
  for (let i = 0; i < SIZE; i++) {
    if (i !== row && board[i][col] === value) {
      return true;
    }
  }
  return false;
}

/**
 * Check if a value exists in the 3x3 box (excluding the current cell)
 * @returns {boolean} true if duplicate exists
 */
function hasBoxConflict(row, col, value, board) {
  const boxRow = Math.floor(row / BOX_SIZE) * BOX_SIZE;
  const boxCol = Math.floor(col / BOX_SIZE) * BOX_SIZE;
  for (let i = boxRow; i < boxRow + BOX_SIZE; i++) {
    for (let j = boxCol; j < boxCol + BOX_SIZE; j++) {
      if ((i !== row || j !== col) && board[i][j] === value) {
        return true;
      }
    }
  }
  return false;
}

/**
 * Check if an entry is valid (no conflicts with Sudoku rules)
 * @returns {boolean} true if value is valid at position
 */
function isValidEntry(row, col, value, board) {
  if (value === 0 || value === '' || !value) {
    return true;  // Empty cells are always "valid"
  }
  return !hasRowConflict(row, col, value, board) && 
         !hasColumnConflict(row, col, value, board) && 
         !hasBoxConflict(row, col, value, board);
}

/**
 * Find all cells that conflict with the entered value
 * Returns array of [row, col] pairs including the entered cell if invalid
 * @returns {Array} array of conflicting cell positions
 */
function getConflictingCells(row, col, value, board) {
  if (value === 0 || value === '' || !value) {
    return [];  // No conflicts for empty cells
  }
  
  const conflicts = [];
  
  // Check row for conflicts
  for (let j = 0; j < SIZE; j++) {
    if (j !== col && board[row][j] === value) {
      conflicts.push([row, j]);
    }
  }
  
  // Check column for conflicts
  for (let i = 0; i < SIZE; i++) {
    if (i !== row && board[i][col] === value) {
      conflicts.push([i, col]);
    }
  }
  
  // Check 3x3 box for conflicts
  const boxRow = Math.floor(row / BOX_SIZE) * BOX_SIZE;
  const boxCol = Math.floor(col / BOX_SIZE) * BOX_SIZE;
  for (let i = boxRow; i < boxRow + BOX_SIZE; i++) {
    for (let j = boxCol; j < boxCol + BOX_SIZE; j++) {
      if ((i !== row || j !== col) && board[i][j] === value) {
        conflicts.push([i, j]);
      }
    }
  }
  
  // Add the entered cell itself if it has conflicts
  if (!isValidEntry(row, col, value, board)) {
    conflicts.push([row, col]);
  }
  
  return conflicts;
}

/**
 * Update the visual validation state of a cell and all affected cells
 */
function updateCellValidation(row, col) {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = getCurrentBoard();
  
  // Get the cell input
  const idx = row * SIZE + col;
  const inp = inputs[idx];
  const value = inp.value ? parseInt(inp.value, 10) : 0;
  
  // Get all cells that conflict with this value
  const conflictingCells = getConflictingCells(row, col, value, board);
  const conflictSet = new Set(conflictingCells.map(c => c[0] * SIZE + c[1]));
  
  // Update styling for all cells in the affected row, column, and box
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const cellIdx = i * SIZE + j;
      const cellInp = inputs[cellIdx];
      
      // Skip prefilled cells
      if (cellInp.disabled) continue;
      
      const cellValue = cellInp.value ? parseInt(cellInp.value, 10) : 0;
      
      // Clear previous validation classes
      cellInp.classList.remove('invalid', 'conflict');
      
      // Only validate if cell has a value
      if (cellValue !== 0) {
        // Check if this cell is in the conflict set for the current cell
        if (conflictSet.has(cellIdx)) {
          cellInp.classList.add('conflict');
        } else {
          // Check if this cell itself has conflicts with any other cell
          const cellBoard = getCurrentBoard();
          if (!isValidEntry(i, j, cellValue, cellBoard)) {
            cellInp.classList.add('conflict');
          }
        }
      }
    }
  }
}

/**
 * Clear all validation/conflict styling from the board
 */
function clearAllValidation() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < inputs.length; i++) {
    inputs[i].classList.remove('invalid', 'conflict');
  }
}

/**
 * Format seconds as MM:SS
 * @param {number} seconds - Total seconds elapsed
 * @returns {string} Formatted time string (e.g., "01:23")
 */
function formatTimer(seconds) {
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

/**
 * Update the timer display with current elapsed time
 */
function updateTimerDisplay() {
  document.getElementById('timer').innerText = formatTimer(elapsedSeconds);
}

/**
 * Start the timer (clears any existing interval to prevent duplicates)
 */
function startTimer() {
  // Clear any existing interval
  if (timerIntervalId) {
    clearInterval(timerIntervalId);
  }
  
  // Reset elapsed time and update display
  elapsedSeconds = 0;
  isTimerRunning = true;
  updateTimerDisplay();
  
  // Create new interval that increments every second
  timerIntervalId = setInterval(() => {
    elapsedSeconds++;
    updateTimerDisplay();
  }, 1000);
}

/**
 * Stop the timer and prevent further updates
 */
function stopTimer() {
  if (timerIntervalId) {
    clearInterval(timerIntervalId);
    timerIntervalId = null;
    isTimerRunning = false;
  }
}

/**
 * Load theme preference from localStorage
 */
function loadTheme() {
  try {
    const savedTheme = localStorage.getItem('sudoku_theme');
    currentTheme = savedTheme || 'light';
  } catch (e) {
    console.error('Error loading theme:', e);
    currentTheme = 'light';
  }
  applyTheme();
}

/**
 * Save theme preference to localStorage
 */
function saveTheme() {
  try {
    localStorage.setItem('sudoku_theme', currentTheme);
  } catch (e) {
    console.error('Error saving theme:', e);
  }
}

/**
 * Apply the current theme to the page
 */
function applyTheme() {
  const body = document.body;
  if (currentTheme === 'dark') {
    body.classList.add('dark-mode');
  } else {
    body.classList.remove('dark-mode');
  }
  updateThemeToggleButton();
}

/**
 * Toggle between light and dark themes
 */
function toggleTheme() {
  currentTheme = currentTheme === 'light' ? 'dark' : 'light';
  saveTheme();
  applyTheme();
}

/**
 * Update the theme toggle button text based on current theme
 */
function updateThemeToggleButton() {
  const btn = document.getElementById('theme-toggle');

  if (currentTheme === 'dark') {
    btn.textContent = '☀️';
    btn.title = 'Switch to light mode';
  } else {
    btn.textContent = '🌙';
    btn.title = 'Switch to dark mode';
  }
}

/**
 * Load scores from localStorage
 */
function loadScores() {
  try {
    const scoresJson = localStorage.getItem('sudoku_scores');
    if (!scoresJson) {
      scores = [];
      return;
    }
    
    const parsedScores = JSON.parse(scoresJson);
    if (!Array.isArray(parsedScores)) {
      scores = [];
      return;
    }
    
    // Filter out invalid scores
    scores = parsedScores.filter(score => isValidScore(score));
  } catch (e) {
    console.error('Error loading scores from localStorage:', e);
    scores = [];
  }
}

/**
 * Validate if a score object has all required fields and valid types
 */
function isValidScore(score) {
  return (
    typeof score === 'object' &&
    score !== null &&
    typeof score.playerName === 'string' &&
    typeof score.time === 'number' &&
    ['easy', 'medium', 'hard'].includes(score.difficulty) &&
    typeof score.hintsUsed === 'number' &&
    score.playerName.length > 0 &&
    score.time >= 0 &&
    score.hintsUsed >= 0
  );
}

/**
 * Prompt user for player name with validation and sanitization
 */
function promptForPlayerName() {
  let name = prompt('Enter your name for the scoreboard:');
  if (name === null) return null;  // User clicked Cancel
  
  name = name.trim();
  if (!name) name = 'Anonymous';
  if (name.length > 50) name = name.substring(0, 50);
  
  return name;
}

/**
 * Save a completed puzzle score to localStorage
 */
function saveScore(playerName, time, difficulty, hintsUsed) {
  // Create score object with only required fields
  const score = {
    playerName: playerName,
    time: time,
    difficulty: difficulty,
    hintsUsed: hintsUsed
  };
  
  // Add to scores array
  scores.push(score);
  
  // Sort by time (fastest first)
  scores.sort((a, b) => a.time - b.time);
  
  // Keep only top 10
  scores = scores.slice(0, 10);
  
  // Save to localStorage
  try {
    localStorage.setItem('sudoku_scores', JSON.stringify(scores));
  } catch (e) {
    console.error('Error saving scores to localStorage:', e);
  }
}

/**
 * Render the scoreboard table with top 10 scores
 */
function renderScoreboard() {
  const tbody = document.getElementById('scoreboard-body');
  tbody.innerHTML = '';  // Clear existing rows
  
  if (scores.length === 0) {
    const row = tbody.insertRow();
    const cell = row.insertCell(0);
    cell.colSpan = 5;
    cell.textContent = 'No scores yet. Complete a puzzle!';
    return;
  }
  
  scores.forEach((score, index) => {
    const row = tbody.insertRow();
    
    // Rank
    const rankCell = row.insertCell(0);
    rankCell.textContent = (index + 1).toString();
    
    // Player Name (safe rendering using textContent)
    const nameCell = row.insertCell(1);
    nameCell.textContent = score.playerName;
    
    // Time
    const timeCell = row.insertCell(2);
    timeCell.textContent = formatTimer(score.time);
    
    // Difficulty
    const diffCell = row.insertCell(3);
    diffCell.textContent = score.difficulty.charAt(0).toUpperCase() + score.difficulty.slice(1);
    
    // Hints
    const hintsCell = row.insertCell(4);
    hintsCell.textContent = score.hintsUsed.toString();
  });
}

/**
 * Handle puzzle completion: ask for name and save score
 */
function handlePuzzleSolved() {
  // Prevent duplicate saves for same puzzle
  if (puzzleCompleted) return;
  
  const playerName = promptForPlayerName();
  if (playerName !== null) {
    saveScore(playerName, elapsedSeconds, currentDifficulty, hintsUsed);
    renderScoreboard();
    puzzleCompleted = true;  // Only mark as completed after successful save
  }
  // If user pressed Cancel, puzzleCompleted remains false so they can try again
}

/**
 * Use a hint: find an empty editable cell and fill it with the correct value
 */
function useHint() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  
  // Check if there's a solution available
  if (!solution || solution.length === 0) {
    document.getElementById('message').innerText = 'No solution available';
    return;
  }
  
  // Find first empty editable cell (not prefilled, not already hinted)
  let hintUsed = false;
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const inp = inputs[idx];
      
      // Skip if cell is disabled (prefilled or already hinted)
      if (inp.disabled) continue;
      
      // Skip if cell already has user-entered value
      if (inp.value) continue;
      
      // Fill with correct value from solution
      inp.value = solution[i][j];
      inp.disabled = true;
      inp.className = 'sudoku-cell hinted';
      hintsUsed++;
      
      // Update hints counter display
      document.getElementById('hints-counter').innerText = 'Hints: ' + hintsUsed;
      
      // Clear validation styling when hint is used
      clearAllValidation();
      
      hintUsed = true;
      break;
    }
    if (hintUsed) break;
  }
  
  if (!hintUsed) {
    const msg = document.getElementById('message');
    msg.style.color = '#f57f17';
    msg.innerText = 'No empty cells remaining';
  }
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        // Sanitize input: only allow digits 1-9, delete/empty is ok
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        
        // Validate and update conflict highlighting
        const row = parseInt(e.target.dataset.row);
        const col = parseInt(e.target.dataset.col);
        updateCellValidation(row, col);
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz, sol) {
  puzzle = puz;
  solution = sol || [];
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
  // Clear any previous validation/conflict styling
  clearAllValidation();
}

async function newGame() {
  const res = await fetch('/new?difficulty=' + currentDifficulty);
  const data = await res.json();
  hintsUsed = 0;
  puzzleCompleted = false;
  document.getElementById('hints-counter').innerText = 'Hints: 0';
  renderPuzzle(data.puzzle, data.solution);
  document.getElementById('message').innerText = '';
  startTimer();
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  // Clear previous validation/conflict styling before showing check results
  clearAllValidation();
  
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (incorrect.size === 0) {
    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! You solved it!';
    stopTimer();
    handlePuzzleSolved();
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  // Load saved theme and apply it
  loadTheme();

  // Load and render scoreboard from localStorage
  loadScores();
  renderScoreboard();

  // Wire main buttons
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint').addEventListener('click', useHint);
  document.getElementById('check-solution').addEventListener('click', checkSolution);

  // Wire Dark/Light Mode toggle
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

 // Wire difficulty selector
document.getElementById('difficulty-select').addEventListener('change', (event) => {
  currentDifficulty = event.target.value;
  newGame();
}); 
});