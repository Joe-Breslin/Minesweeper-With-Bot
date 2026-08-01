# Game_State.py

import board_generator
import random
import tkinter as tk
from collections import deque
from typing import List, Optional, Tuple

class GameState:

    def __init__(self, user_width, user_height, bomb_pct):
        self.user_width = user_width
        self.user_height = user_height
        self.bomb_pct = bomb_pct
        self.board = board_generator.BoardGenerator.generate_hidden_board(user_width, user_height, bomb_pct)
        self.visible: List[List[Optional[object]]] = [[None for _ in range(user_width)] for _ in range(user_height)]
        self.game_over = False
        self.won = False
        self.first_click = True

    def ensure_safe_start(self, row, col):
        safe_cells = {(row, col)}
        safe_cells.update(self.neighbors(row,col))
        self.board = board_generator.BoardGenerator.generate_hidden_board(
            self.user_width, self.user_height, self.bomb_pct, safe_cells
        )

    def in_bounds(self, row, col): 
        return 0 <= row < self.user_height and 0 <= col < self.user_width
    
    def neighbors(self, row, col):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if self.in_bounds(nr, nc):
                    yield nr, nc

    def toggle_flag(self, row, col):
        if self.game_over or self.won:
            return
        
        current = self.visible[row][col]
        if current is None:
            self.visible[row][col] = "!"
        elif current == "!":
            self.visible[row][col] = None

    def reveal(self, row, col):
        if self.game_over or self.won:
            return 

        current = self.visible[row][col]
        if current is not None and current != "!":
            return
        if current == "!":
            return

        if self.first_click:
            self.ensure_safe_start(row, col)
            self.first_click = False
        
        if self.board[row][col] == -1:
            self.visible[row][col] = "M"
            self.game_over = True
            self.reveal_all_mines()
            return
        self.flood_reveal(row, col)
        self.check_win()

    def flood_reveal(self, row, col):
        q = deque([(row,col)])

        while q:
            r, c = q.popleft()
            if self.visible[r][c] is not None:
                continue
            if self.board[r][c] == -1:
                continue
            self.visible[r][c] = int(self.board[r][c])

            if self.board[r][c] == 0:
                for nr, nc in self.neighbors(r, c):
                    if self.visible[nr][nc] is None:
                        q.append((nr, nc))

    def reveal_all_mines(self):
        for r in range(self.user_height):
            for c in range(self.user_width):
                if self.board[r][c] == -1 and self.visible[r][c] != "!":
                    self.visible[r][c] = -1

    def check_win(self):
        for r in range(self.user_height):
            for c in range(self.user_width):
                if self.board[r][c] != -1 and self.visible[r][c] is None:
                    return
        self.won = True

    def reset(self):
        self.board = board_generator.BoardGenerator.generate_hidden_board(self.user_width, self.user_height, self.bomb_pct)
        self.visible = [[None for _ in range(self.user_width)] for _ in range(self.user_height)]
        self.game_over = False
        self.won = False
        self.first_click = True

    def visible_mine_count(self):
        return sum(1 for r in range(self.user_height) for c in range(self.user_width) if self.visible[r][c] == "!")

    def chord(self, row, col):
        if self.game_over or self.won:
            return
        value = self.visible[row][col]
        if not isinstance(value, int) or value <= 0:
            return

        flagged = sum(1 for nr, nc in self.neighbors(row, col) if self.visible[nr][nc] == "!")
        if flagged != value:
            return

        for nr, nc in self.neighbors(row, col):
            if self.visible[nr][nc] is None:
                self.reveal(nr, nc)