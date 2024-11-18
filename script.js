let grid = [];
let level = 1;
let moves = 0;
const moveCounter = document.getElementById('move-counter');
const gridContainer = document.getElementById('grid-container');
const restartButton = document.getElementById('restart-button');
const solveButton = document.getElementById('solve-button');
const levelDisplay = document.getElementById('level-display'); // Reference to the level display
const startPage = document.getElementById('start-page');
const gamePage = document.getElementById('game');
const startButton = document.getElementById('start-button');

// Start game button event
startButton.addEventListener('click', () => {
    startPage.style.display = 'none';
    gamePage.style.display = 'block';
    initializeGrid();
});

// Initialize grid based on level
function initializeGrid() {
    const size = level + 1; // level 1 -> 2x2, level 2 -> 3x3, etc.
    grid = Array.from({ length: size }, () => Array(size).fill(0)); // 0 for grey, 1 for green
    moves = 0;
    updateGridUI();
    updateLevelDisplay(); // Update level display
}

// Update the grid UI
function updateGridUI() {
    gridContainer.innerHTML = '';
    const size = level + 1; // Determine the size of the grid
    gridContainer.style.gridTemplateColumns = `repeat(${size}, 50px)`; // Set the number of columns

    grid.forEach((row, rowIndex) => {
        row.forEach((cell, colIndex) => {
            const cellDiv = document.createElement('div');
            cellDiv.className = 'cell' + (cell === 1 ? ' green' : '');
            cellDiv.addEventListener('click', () => cellClick(rowIndex, colIndex));
            gridContainer.appendChild(cellDiv);
        });
    });
    moveCounter.textContent = `Moves: ${moves}`;
}

// Update level display
function updateLevelDisplay() {
    levelDisplay.textContent = `Level: ${level}`; // Update the level display text
}

// Handle cell click
function cellClick(row, col) {
    const size = level + 1;

    // Function to toggle the state of a cell
    const toggleCell = (r, c) => {
        if (r >= 0 && r < size && c >= 0 && c < size) {
            grid[r][c] = grid[r][c] === 0 ? 1 : 0; // Toggle state
        }
    };

    // Toggle clicked cell and its neighbors
    toggleCell(row, col); // Toggle itself
    toggleCell(row - 1, col); // Up
    toggleCell(row + 1, col); // Down
    toggleCell(row, col - 1); // Left
    toggleCell(row, col + 1); // Right

    moves++;
    updateGridUI();

    // Check if the level is solved after updating the UI
    if (isLevelSolved()) {
        // Show the final state before moving to the next level
        setTimeout(() => {
            alert(`Level Solved in ${moves} moves!`);
            level++;
            initializeGrid();
        }, 100); // Short delay to allow the final state to render
    }
}

// Check if the level is solved
function isLevelSolved() {
    return grid.flat().every(cell => cell === 1); // Check if all cells are green
}

// Restart level
restartButton.addEventListener('click', () => {
    initializeGrid();
});

// Solve level
solveButton.addEventListener('click', () => {
    const levelInput = prompt("Enter Level (1-10):");
    const levelNum = parseInt(levelInput, 10);
    if (levelNum >= 1 && levelNum <= 10) {
        alert("Solver feature is not implemented yet. You are currently at Level: " + level);
        // Do not change the level, just notify the user.
    } else {
        alert("Please enter a valid level number between 1 and 10.");
    }
});

// Start the game
initializeGrid();