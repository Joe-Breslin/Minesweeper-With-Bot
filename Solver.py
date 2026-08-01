# Solver.py

import Game_State

class MinesweeperSolver:
    """Deterministic Solver v0.1.0"""

    def __init__(self, state):
        self.state = state

    def frontier_constraints(self):
        constraints = []
        s = self.state

        for r in range(s.user_height):
            for c in range(s.user_width):
                value = s.visible[r][c]
                if not isinstance(value, int) or value < 0:
                    continue

                unknown = set()
                flagged = 0
                for nr, nc in s.neighbors(r, c):
                    v = s.visible[nr][nc]
                    if v == "!":
                        flagged += 1
                    elif v is None:
                        unknown.add((nr, nc))

                if unknown:
                    constraints.append((unknown, value - flagged))
        return constraints

    def deduce(self):
        constraints = self.frontier_constraints()
        safe = set()
        mines = set()

        changed = True
        while changed:
            changed = False

            for cells, remaining in constraints:
                unresolved = cells - mines - safe
                remaining = remaining - len(cells & mines)
                if not unresolved:
                    continue

                if remaining <= 0:
                    for cell in unresolved:
                        if cell not in safe:
                            safe.add(cell)
                            changed = True
                elif remaining == len(unresolved):
                    for cell in unresolved:
                        if cell not in mines:
                            mines.add(cell)
                            changed = True
            for cells_a, rem_a in constraints:
                a = cells_a - mines - safe
                if not a:
                    continue
                rem_a = rem_a - len(cells_a & mines)
                for cells_b, rem_b in constraints:
                    b = cells_b - mines - safe
                    if not b or a == b:
                        continue
                    rem_b = rem_b - len(cells_b & mines)
                    if a < b:
                        diff = b - a
                        diff_mines = rem_b - rem_a 
                        if diff_mines == 0:
                            for cell in diff:
                                if cell not in safe:
                                    safe.add(cell)
                                    changed = True
                        elif diff_mines == len(diff):
                            for cell in diff:
                                if cell not in mines:
                                    mines.add(cell)
                                    changed = True
        return safe, mines

    def step(self):
        s = self.state
        if s.game_over or s.won:
            return False

        if all(s.visible[r][c] is None for r in range(s.user_height) for c in range(s.user_width)):
            s.reveal(s.user_height // 2, s.user_width // 2)
            return True

        safe, mines = self.deduce()

        moved = False
        for r, c in mines:
            if s.visible[r][c] is None:
                s.toggle_flag(r,c)
                moved = True 
        for r, c in safe:
            if s.visible[r][c] is None:
                s.reveal(r, c)
                moved = True

        return moved

    def solve_fully(self, max_steps = 1000):
        for _ in range(max_steps):
            if self.state.game_over or self.state.won:
                break
            if not self.step():
                break
        return self.state.won
        