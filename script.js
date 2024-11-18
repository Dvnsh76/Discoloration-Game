let currentLevel = 1;
let maxLevel = 5;  // 2x2 to 7x7 grid
let gridSize = 2;  // Starts with level 1 (2x2)
let grid = [];
let moveCount = 0;

const gridContainer = document.getElementById('grid');
const moveCountDisplay = document.getElementById('move-count');
const levelDisplay = document.getElementById('current-level');
const restartButton = document.getElementById('restart');

// Initialize the game with the current level
function initGame() {
    gridContainer.innerHTML = '';  // Clear previous grid
    moveCount = 0;
    moveCountDisplay.textContent = moveCount;
    levelDisplay.textContent = currentLevel;

    // Set grid size based on the current level
    gridSize = currentLevel + 1;  // Level 1 -> 2x2, Level 2 -> 3x3, etc.
    gridContainer.style.gridTemplateColumns = `repeat(${gridSize}, 1fr)`;
    gridContainer.style.gridTemplateRows = `repeat(${gridSize}, 1fr)`;

    // Create a new grid
    grid = [];
    for (let i = 0; i < gridSize; i++) {
        grid[i] = [];
        for (let j = 0; j < gridSize; j++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.row = i;
            cell.dataset.col = j;
            cell.addEventListener('click', () => handleClick(i, j));
            grid[i][j] = 0;  // Initial state is grey (0)
            gridContainer.appendChild(cell);
        }
    }
}

// Handle the click on a cell
function handleClick(row, col) {
    toggleCell(row, col);
    toggleCell(row - 1, col);  // Above
    toggleCell(row + 1, col);  // Below
    toggleCell(row, col - 1);  // Left
    toggleCell(row, col + 1);  // Right

    moveCount++;
    moveCountDisplay.textContent = moveCount;

    // Check if all cells are green
    checkWin();
}

// Toggle cell state (grey to green, green to grey)
function toggleCell(row, col) {
    if (row >= 0 && row < gridSize && col >= 0 && col < gridSize) {
        const cell = document.querySelector(`.cell[data-row='${row}'][data-col='${col}']`);
        grid[row][col] = 1 - grid[row][col];  // Flip between 0 and 1
        cell.classList.toggle('green');
    }
}

// Check if the player has won (all cells green)
function checkWin() {
    const allGreen = grid.every(row => row.every(cell => cell === 1));
    if (allGreen) {
        setTimeout(() => {
            alert(`Level ${currentLevel} completed in ${moveCount} moves!`);
            nextLevel();
        }, 100);
    }
}

// Move to the next level
function nextLevel() {
    if (currentLevel < maxLevel) {
        currentLevel++;
        initGame();
    } else {
        alert("Congratulations! You've completed all levels!");
    }
}

// Restart the current level
restartButton.addEventListener('click', initGame);

// Initialize the game for the first time
initGame();


document.getElementById('solve-game').addEventListener('click', () => {
    const currentGrid = getCurrentGridState();  // Function to get the current grid state
    const solution = bfsSolver(currentGrid);

    if (solution.length > 0) {
        alert(`Solution found! Applying solution...`);
        solution.forEach(move => {
            handleClick(move.row, move.col);  // Simulate each click
        });
    } else {
        alert("No solution found!");
    }
});

// Function to get the current grid state (convert the DOM to the grid array)
function getCurrentGridState() {
    const grid = [];
    const cells = document.querySelectorAll('.cell');
    let gridSize = Math.sqrt(cells.length);  // Calculate grid size dynamically
    for (let i = 0; i < gridSize; i++) {
        grid[i] = [];
        for (let j = 0; j < gridSize; j++) {
            const cell = cells[i * gridSize + j];
            grid[i][j] = cell.classList.contains('green') ? 1 : 0;
        }
    }
    return grid;
}
