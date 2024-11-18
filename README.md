# Discoloration Game

**Discoloration** is a web-based puzzle game where the goal is to turn all cells in a grid from grey to green by clicking on them. Clicking a cell toggles its state and the states of its neighboring cells. The game provides an engaging challenge across multiple levels, with the added feature of an AI solver to help find optimal solutions.

---

## **Game Rules**

Welcome to **Discoloration Game!** 

### Instructions:

1. **Click on a cell** to toggle its state between grey and green.
2. Clicking a cell will also **toggle the state of its neighboring cells** (adjacent horizontal and vertical cells).
3. The **goal is to turn all cells green** by clicking on them strategically.
4. Use the **"Restart Level"** button to reset the current level.
5. Use the **"Solve Level"** button to automatically solve the level using an AI solver.
6. Progress through increasing levels of difficulty, from a 2x2 grid to a 5x5 grid.

**Good luck!**

---

## **Developer Information**

This game is developed by:

- **Devansh Goel**  
- **Aditya Saigal**

---

## **Algorithms Used**

### **1. Breadth-First Search (BFS)**

For **levels 1, 2, and 3**, the **BFS** algorithm is used to find the solution. BFS is an uninformed search algorithm that explores all possible states level by level. It guarantees finding the shortest solution in an unweighted grid.

- **State Representation**: The grid is represented as a 2D array where each cell is either grey (0) or green (1).
- **Neighbor Generation**: Each click on a cell toggles its state and the state of its neighboring cells.
- **Goal**: The algorithm continues until all cells are green, and the sequence of moves is returned.

### **2. A* (A-Star) Algorithm**

For **level 4**, the game uses **A\* Search** to find an optimized solution. A\* is a pathfinding algorithm that uses heuristics to guide its search towards the goal, making it more efficient than BFS for larger grids.

- **Heuristic**: The heuristic used in A\* is the **Manhattan Distance**, which counts the number of grey cells that need to be turned green. This heuristic helps prioritize grids that are closer to the goal.
- **Priority Queue**: A\* uses a priority queue (min-heap) to expand the most promising states first, ensuring an optimized and faster solution.

---

## **Code Explanation:**

### **Game Flow**

1. **Level Initialization**:  
   The game starts with a 2x2 grid and progresses to larger grids as the player advances through the levels. For each level, the grid size increases by one, i.e., Level 1 has a 2x2 grid, Level 2 has a 3x3 grid, Level 3 has a 4x4 grid, and Level 4 has a 5x5 grid.

2. **User Interaction**:  
   The player interacts with the game by clicking on cells, toggling their state. Each click affects the selected cell and its immediate neighbors (up, down, left, right).

3. **Automatic Solution**:  
   The player can choose to solve the level automatically using the **BFS** or **A\*** algorithm. The game computes the optimal sequence of moves and displays it.

4. **Game State Management**:  
   The game uses a grid state represented as a 2D array. Each cell can either be grey (0) or green (1). The goal is to toggle the grid to an all-green state by applying valid moves.

5. **UI Components**:  
   The game UI includes:
   - A grid of buttons representing the cells.
   - Move counter and level display.
   - Buttons for restarting the level, solving the level, and starting the game.

6. **Algorithm Choice**:  
   - **Levels 1, 2, and 3** use **Breadth-First Search** to find the solution.
   - **Level 4** uses **A\*** for an optimized solution with a heuristic to minimize moves.

### **Key Code Components**

1. **Grid Initialization**:  
   The grid is initialized based on the current level's size. It starts with all cells set to grey.

2. **Cell Toggle**:  
   Each time a player clicks on a cell, its state and the state of its neighbors are toggled.

3. **Solvers (BFS and A\*)**:  
   The solvers implement the BFS and A\* algorithms to automatically solve the grid and return the sequence of moves required to achieve a solution.

4. **User Interface (UI)**:  
   The UI is created using the **Tkinter** library. It includes buttons for each cell, a move counter, level display, and action buttons like "Restart Level" and "Solve Level."

5. **Game Progression**:  
   The game progresses through increasing levels. The player starts at Level 1 and works their way through the grid sizes until Level 4. After completing all levels, the game ends.

---

## **Technologies Used**

- **Python**  
- **Tkinter** (for GUI)
- **Breadth-First Search (BFS)**
- **A\* Search Algorithm**
- **Heuristic: Manhattan Distance**

---

## **Installation**

To run the Discoloration Game locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/discoloration-game.git
   ```
   
   
2. Navigate into the project directory:
  ```bash
  cd discoloration-game
  ```

3. Run the Python script:
  ```bash
  python game_and_solver.py
  ```
