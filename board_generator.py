# Board_Generator.py

import numpy as np
import random
 
class BoardGenerator:
    
    @staticmethod
    def generate_hidden_board(user_width, user_height, safe_cells=None):
        if safe_cells is None:
            safe_cells = set()

        # First create board with zeros
        board = np.zeros((user_height, user_width), dtype=int)
        bombs_needed = int(user_width * user_height * 0.15)

        for _ in range(bombs_needed):
            row = random.randint(0,user_height - 1)
            col = random.randint(0,user_width -1)

            while board[row][col] == -1 or (row, col) in safe_cells:
                row = random.randint(0, user_height -1) 
                col = random.randint(0,user_width -1)

            board[row][col] = -1
        for row in range(user_height):
            for col in range(user_width):
                if board[row][col] == -1:
                    continue
                bomb_count = 0
                for i in [-1,0,1]:
                    for j in [-1,0,1]:
                        if i == 0 and j == 0:
                            continue
                        r = row + i
                        c = col + j
                        if 0 <= r < user_height and 0 <= c < user_width and board[r][c] == -1:
                            bomb_count += 1
                board[row][col] = bomb_count
        return board