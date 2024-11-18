import tkinter as tk
from tkinter import messagebox
import heapq
from collections import deque

# Game State Variables
level = 1
moves = 0
grid = []

# BFS Solver for Levels 1, 2, and 3
def bfs_solver(initial_grid):
    size = len(initial_grid)
    initial_state = (tuple(tuple(row) for row in initial_grid), [])  # Immutable state
    queue = deque([initial_state])
    visited = set()
    visited.add(initial_state[0])

    # Toggle function
    def toggle(grid, row, col):
        new_grid = [list(r) for r in grid]  # Convert to mutable list
        for r, c in [(row, col), (row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if 0 <= r < size and 0 <= c < size:
                new_grid[r][c] = 1 - new_grid[r][c]
        return tuple(tuple(r) for r in new_grid)  # Convert back to immutable tuple

    # BFS loop
    while queue:
        current_grid, moves = queue.popleft()

        # Check if solved
        if all(cell == 1 for row in current_grid for cell in row):
            return moves

        # Generate neighbors
        for row in range(size):
            for col in range(size):
                new_grid = toggle(current_grid, row, col)
                new_state = (new_grid, moves + [(row, col)])
                if new_state[0] not in visited:
                    visited.add(new_state[0])
                    queue.append(new_state)

    return None  # Shouldn't reach here if the grid is solvable


# A* Solver for Level 4 (Optimized)
def a_star_solver(initial_grid):
    size = len(initial_grid)
    initial_state = (tuple(tuple(row) for row in initial_grid), 0, [])  # Immutable state
    goal_state = tuple([tuple([1] * size)] * size)
    
    # Priority Queue using heapq for better performance
    pq = []
    heapq.heappush(pq, (0, initial_state))  # (heuristic, state)
    visited = set()
    visited.add(initial_state[0])

    # Toggle function
    def toggle(grid, row, col):
        new_grid = [list(r) for r in grid]  # Convert to mutable list
        for r, c in [(row, col), (row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if 0 <= r < size and 0 <= c < size:
                new_grid[r][c] = 1 - new_grid[r][c]
        return tuple(tuple(r) for r in new_grid)  # Convert back to immutable tuple

    # Heuristic function (optimizing heuristic)
    def heuristic(grid):
        # Count the number of cells that are in the wrong state
        return sum(1 for row in grid for cell in row if cell == 0)

    while pq:
        _, (current_grid, current_cost, moves) = heapq.heappop(pq)

        # Check if solved
        if current_grid == goal_state:
            return moves

        # Generate neighbors
        for row in range(size):
            for col in range(size):
                new_grid = toggle(current_grid, row, col)
                new_cost = current_cost + 1
                new_moves = moves + [(row, col)]
                
                # Skip revisiting already visited grids
                if new_grid not in visited:
                    visited.add(new_grid)
                    heapq.heappush(pq, (new_cost + heuristic(new_grid), (new_grid, new_cost, new_moves)))

    return None  # Shouldn't reach here if the grid is solvable


# Solve Level Function
def solve_level():
    global grid, moves

    if level <= 3:
        solution_moves = bfs_solver(grid)
    elif level == 4:
        solution_moves = a_star_solver(grid)

    if solution_moves is None:
        messagebox.showinfo("No Solution", "This grid cannot be solved!")
        return

    moves = 0  # Reset moves counter

    # Perform each move with a delay
    for index, (row, col) in enumerate(solution_moves):
        root.after(
            500 * index, 
            lambda r=row, c=col, final=(index == len(solution_moves) - 1): auto_click(r, c, final)
        )


# Automated click function
def auto_click(row, col, final=False):
    global moves

    toggle_cell(row, col)
    moves += 1
    update_grid_ui()

    if final:
        # Show success message and move to the next level
        messagebox.showinfo("Level Solved!", f"Solved automatically in {moves} moves!")
        next_level()  # Move to the next level only once


# Initialize the game
def initialize_grid():
    global grid, moves
    size = level + 1  # Grid size increases with level
    grid = [[0 for _ in range(size)] for _ in range(size)]  # 0 = Grey, 1 = Green
    moves = 0
    update_grid_ui()
    update_level_display()


# Toggle the state of a cell and its neighbors
def toggle_cell(row, col):
    size = len(grid)
    for r, c in [(row, col), (row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
        if 0 <= r < size and 0 <= c < size:
            grid[r][c] = 1 - grid[r][c]  # Toggle state


# Check if the level is solved
def is_level_solved():
    return all(cell == 1 for row in grid for cell in row)


# Handle cell click
def cell_click(row, col):
    global moves
    toggle_cell(row, col)
    moves += 1
    update_grid_ui()
    if is_level_solved():
        messagebox.showinfo("Level Solved!", f"You solved level {level} in {moves} moves!")
        next_level()


# Move to the next level
def next_level():
    global level
    level += 1
    if level > 4:
        messagebox.showinfo("Congratulations!", "You have completed all levels!")
        root.quit()
    else:
        initialize_grid()


# Restart the current level
def restart_level():
    initialize_grid()


# Update the UI grid
def update_grid_ui():
    for widget in grid_frame.winfo_children():
        widget.destroy()

    size = len(grid)
    for row in range(size):
        for col in range(size):
            color = "lightgrey" if grid[row][col] == 0 else "green"
            cell = tk.Button(grid_frame, bg=color, width=4, height=2,
                             command=lambda r=row, c=col: cell_click(r, c))
            cell.grid(row=row, column=col, padx=2, pady=2)

    move_label.config(text=f"Moves: {moves}")


# Update the level display
def update_level_display():
    level_label.config(text=f"Level: {level}")


# Create the main window
root = tk.Tk()
root.title("Discoloration Game")
root.configure(bg="black")

# Home Page Frame
home_frame = tk.Frame(root, bg="black")
home_frame.pack(fill="both", expand=True)

# Title
title_label = tk.Label(home_frame, text="Discoloration Game", font=("Montserrat", 24, "bold"), fg="white", bg="black")
title_label.pack(pady=20)

# Rulebook with Instructions
instructions_label = tk.Label(home_frame, text="Welcome to the Discoloration Game!\n", font=("Montserrat", 14), fg="white", bg="black")
instructions_label.pack(pady=5)
instructions_label = tk.Label(home_frame, text="Instructions", font=("Montserrat", 14, "underline"), fg="white", bg="black")
instructions_label.pack(pady=5)
instructions_text = tk.Label(home_frame, text="1. Click on a cell to toggle its state (green or grey).\n"
                                               "2. Clicking a cell will also toggle its neighboring cells.\n"
                                               "3. The goal is to turn all cells green.\n"
                                               "4. Use the 'Restart Level' button to reset the current level.\n"
                                               "5. Use the 'Solve Level' button to get the answer.\n\n"
                                               "Good luck!", font=("Montserrat", 12), fg="white", bg="black")
instructions_text.pack(pady=5)

# Developer Info
dev_label = tk.Label(home_frame, text="Developed by Devansh Goel and Aditya Saigal", font=("Montserrat", 10),
                     fg="white", bg="black")
dev_label.pack(side=tk.BOTTOM, pady=10)

# Start Game Button
start_button = tk.Button(home_frame, text="Start Game", font=("Montserrat", 16), command=lambda: start_game(), bg="green", fg="white")
start_button.pack(pady=20)

# Game Page Frame
game_frame = tk.Frame(root, bg="black")

# Title
title_label = tk.Label(game_frame, text="Discoloration Game", font=("Montserrat", 24, "bold"), fg="white", bg="black")
title_label.pack(pady=20)

# Level display
level_label = tk.Label(game_frame, text=f"Level: {level}", font=("Montserrat", 16), fg="white", bg="black")
level_label.pack(pady=10)

# Move counter
move_label = tk.Label(game_frame, text=f"Moves: {moves}", font=("Montserrat", 14), fg="white", bg="black")
move_label.pack()

# Grid container
grid_frame = tk.Frame(game_frame, bg="black")
grid_frame.pack(pady=10)

# Control buttons for game actions
control_frame = tk.Frame(game_frame, bg="black")
control_frame.pack()

restart_button = tk.Button(control_frame, text="Restart Level", font=("Montserrat", 12), command=restart_level, bg="red", fg="white")
restart_button.pack(side=tk.LEFT, padx=10)

solve_button = tk.Button(control_frame, text="Solve Level", font=("Montserrat", 12), command=solve_level, bg="blue", fg="white")
solve_button.pack(side=tk.LEFT, padx=10)

# Developer Info at the bottom of the game page
dev_label_game = tk.Label(game_frame, text="Developed by Devansh Goel and Aditya Saigal", font=("Montserrat", 10),
                          fg="white", bg="black")
dev_label_game.pack(side=tk.BOTTOM, pady=10)

# Function to start the game (switch from homepage to game)
def start_game():
    home_frame.pack_forget()  # Hide the home frame
    game_frame.pack(fill="both", expand=True)  # Show the game frame
    initialize_grid()  # Initialize the first level grid

# Start the application
root.mainloop()
