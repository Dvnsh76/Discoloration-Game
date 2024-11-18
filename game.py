import tkinter as tk
from tkinter import messagebox
from collections import deque
import copy
import time

# Game State Variables
level = 1
moves = 0
grid = []

# BFS Solver
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


# Solve Level Function
def solve_level():
    global grid, moves

    solution_moves = bfs_solver(grid)
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
            color = "green" if grid[row][col] == 1 else "grey"
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

# Level display
level_label = tk.Label(root, text=f"Level: {level}", font=("Arial", 16))
level_label.pack(pady=10)

# Move counter
move_label = tk.Label(root, text=f"Moves: {moves}", font=("Arial", 14))
move_label.pack()

# Grid container
grid_frame = tk.Frame(root)
grid_frame.pack(pady=10)

# Control buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

restart_button = tk.Button(button_frame, text="Restart Level", command=restart_level, bg="#007bff", fg="white", width=15)
restart_button.pack(side=tk.LEFT, padx=5)

solve_button = tk.Button(button_frame, text="Solve Level", command=solve_level, bg="#28a745", fg="white", width=15)
solve_button.pack(side=tk.LEFT, padx=5)

# Start the game
initialize_grid()
root.mainloop()
