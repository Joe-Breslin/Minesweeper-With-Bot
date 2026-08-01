# GUI.py

import tkinter as tk
import random
from collections import deque
from typing import List, Optional, Tuple
import Game_State
import time
import Solver

class MinesweeperGUI:

    def __init__(self, root: tk.Tk, user_width, user_height, cell_size: int = 40):
        self.root = root
        self.state = Game_State.GameState(user_width, user_height)
        self.solver = Solver.MinesweeperSolver(self.state)
        self.cell_size = cell_size

        self.canvas_width = user_width * cell_size
        self.canvas_height = user_height * cell_size
        
        self.root.title("Minesweeper Prototype")

        top_frame =tk.Frame(root)
        top_frame.pack(fill="x")

        self.status_label = tk.Label(top_frame, text="Click to Begin")
        self.status_label.pack(side="left", padx=8, pady=6)

        self.mine_label = tk.Label(top_frame, text= f"Mines flagged: 0")
        self.mine_label.pack(side="left", padx=8)

        self.restart_button = tk.Button(top_frame, text="Restart", command=self.restart)
        self.restart_button.pack(side="right", padx=8)

        self.solver_step_button = tk.Button(top_frame, text="Solver Step", command=self.solver_step)
        self.solver_step_button.pack(side="right", padx=8)

        self.auto_solve_button = tk.Button(top_frame, text="Auto Solve", command=self.auto_solve)
        self.auto_solve_button.pack(side="right", padx=8)
        self.auto_solving = False

        self.timer_label = tk.Label(top_frame, text="Time:0")
        self.timer_label.pack(side="right", padx=8)

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Button-2>", self.on_chord_click)
        self.canvas.bind("<Double-Button-1>", self.on_chord_click)

        self.start_time: Optional[float] = None
        self.timer_running = False

        self.draw_board()
        self.update_timer()

    def restart(self):
        self.state.reset()
        self.auto_solving = False
        self.start_time = None
        self.timer_running = False
        self.status_label.config(text="Click to begin")
        self.mine_label.config(text="Mines flagged: 0")
        self.draw_board()
    
    def on_left_click(self, event):
        row, col = self.pixel_to_cell(event.x, event.y)
        if row is None:
            return
        
        if self.start_time is None and not self.state.game_over and not self.state.won:
            self.start_time = time.time()
            self.timer_running = True 
            self.status_label.config(text="Game in progress")

        self.state.reveal(row, col)
        self.mine_label.config(text=f"Mines flagged: {self.state.visible_mine_count()}")

        if self.state.game_over:
            self.status_label.config(text= "Game Over")
            self.timer_running = False
        elif self.state.won:
            self.status_label.config(text="You Won!")
            self.timer_running = False
        
        self.draw_board()

    def on_right_click(self, event):
        row, col = self.pixel_to_cell(event.x, event.y)
        if row is None:
            return
        
        self.state.toggle_flag(row,col)
        self.mine_label.config(text=f"Mines flagged: {self.state.visible_mine_count()}")
        self.draw_board()

    def on_chord_click(self, event):
        row, col = self.pixel_to_cell(event.x, event.y)
        if row is None:
            return

        self.state.chord(row, col)
        self.mine_label.config(text=f"Mines flagged: {self.state.visible_mine_count()}")

        if self.state.game_over:
            self.status_label.config(text="Game Over")
            self.timer_running = False
        elif self.state.won:
            self.status_label.config(text="You Won!")
            self.timer_running = False
            
        self.draw_board()

    def pixel_to_cell(self, x, y):
        row = y // self.cell_size
        col = x // self.cell_size
        if not self.state.in_bounds(row,col):
            return None, None
        return row, col
    
    def draw_board(self):
        self.canvas.delete("all")

        for r in range(self.state.user_height):
            for c in range(self.state.user_width):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                value = self.state.visible[r][c]
                fill = "#d9d9d9"
                text = ""
                text_color = "black"

                if value is None:
                    fill = "#a6a6a6"
                elif value == "!":
                    fill = "#a6a6a6"
                    text = "!!"
                    text_color = "red"
                elif value == "M":
                    fill = "#ff6666"
                    text = "X"
                    text_color = "black"
                elif value == -1:
                    fill = "#ffcccc"
                    text = "X"
                    text_color = "black"
                else:
                    fill = "#eaeaea"
                    if value != 0:
                        text = str(value)

                self.canvas.create_rectangle(x1,y1,x2,y2, fill=fill, outline="black")
                if text:
                    self.canvas.create_text(
                       x1 + self.cell_size // 2, 
                       y1 + self.cell_size // 2,
                       text=text,
                       fill=text_color,
                       font=("Arial", 14, "bold")
                    )
    def update_timer(self):
        if self.timer_running and self.start_time is not None:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}")
        else:
            if self.start_time is None:
                self.timer_label.config(text="Time: 0")
        self.root.after(250, self.update_timer)

    def solver_step(self):
        if self.start_time is None and not self.state.game_over and not self.state.won:
            self.start_time = time.time()
            self.timer_running = True
            self.status_label.config(text="Game in Progress")

        print(self.solver.deduce())
        moved = self.solver.step()
        self.mine_label.config(text=f"Mines flagged: {self.state.visible_mine_count()}")

        if self.state.game_over:
            self.status_label.config(text="Game Over")
            self.timer_running = False
        elif self.state.won:
            self.status_label.config(text="You Won!")
            self.timer_running = False
        elif not moved:
            self.status_label.config(text="Solver Stuck - no logical move available")

        self.draw_board()

    def auto_solve(self):
        if self.auto_solving:
            self.auto_solving = False
            self.auto_solve_button.config(text="Auto Solve")
            return

        self.auto_solving = True
        self.auto_solve_button.config(text="Stop Solving")
        self._auto_solve_step()

    def _auto_solve_step(self):
        if not self.auto_solving:
            return
        if self.state.game_over or self.state.won:
            self.auto_solving = False
            self.auto_solve_button.config(text="Auto Solve")

        self.solver_step()

        if not self.auto_solving:
            return
        if self.state.game_over or self.state.won:
            self.auto_solving = False
            self.auto_solve_button.config(text="Auto Solve")
            return

        self.root.after(300, self._auto_solve_step)

