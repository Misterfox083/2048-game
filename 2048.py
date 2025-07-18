import tkinter as tk
import random

GRID_LEN = 4
GRID_PADDING = 10

class Game(tk.Frame):
    def __init__(self):
        super().__init__(bg="#bbada0", bd=3, width=400, height=400)
        self.grid()
        self.master.title('2048')

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()

        self.master.bind("<Key>", self.key_down)
        self.mainloop()

    def init_grid(self):
        background = tk.Frame(self, bg="#bbada0", width=400, height=400)
        background.grid()

        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = tk.Frame(
                    background,
                    bg="#cdc1b4",
                    width=100,
                    height=100)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = tk.Label(master=cell, text="", bg="#cdc1b4",
                             justify=tk.CENTER, font=("Verdana", 24, "bold"), width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = [[0] * GRID_LEN for _ in range(GRID_LEN)]
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_LEN)
                       for j in range(GRID_LEN) if self.matrix[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.matrix[i][j] = 2 if random.random() < 0.9 else 4

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                value = self.matrix[i][j]
                if value == 0:
                    self.grid_cells[i][j].configure(text="", bg="#cdc1b4")
                else:
                    self.grid_cells[i][j].configure(
                        text=str(value), bg="#eee4da" if value == 2 else "#f2b179")

    def key_down(self, event):
        key = event.keysym
        if key == "Up":
            self.matrix, moved = self.move_up()
        elif key == "Down":
            self.matrix, moved = self.move_down()
        elif key == "Left":
            self.matrix, moved = self.move_left()
        elif key == "Right":
            self.matrix, moved = self.move_right()
        else:
            return

        if moved:
            self.add_new_tile()
            self.update_grid_cells()
            if self.game_over():
                self.grid_cells[1][1].configure(text="Game Over", bg="red")

    def compress(self, mat):
        new_mat = [[0] * GRID_LEN for _ in range(GRID_LEN)]
        moved = False
        for i in range(GRID_LEN):
            pos = 0
            for j in range(GRID_LEN):
                if mat[i][j] != 0:
                    new_mat[i][pos] = mat[i][j]
                    if j != pos:
                        moved = True
                    pos += 1
        return new_mat, moved

    def merge(self, mat):
        moved = False
        for i in range(GRID_LEN):
            for j in range(GRID_LEN - 1):
                if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                    mat[i][j] *= 2
                    mat[i][j + 1] = 0
                    moved = True
        return mat, moved

    def reverse(self, mat):
        return [row[::-1] for row in mat]

    def transpose(self, mat):
        return [list(row) for row in zip(*mat)]

    def move_left(self):
        mat, moved1 = self.compress(self.matrix)
        mat, moved2 = self.merge(mat)
        mat, _ = self.compress(mat)
        return mat, moved1 or moved2

    def move_right(self):
        mat = self.reverse(self.matrix)
        mat, moved1 = self.compress(mat)
        mat, moved2 = self.merge(mat)
        mat, _ = self.compress(mat)
        mat = self.reverse(mat)
        return mat, moved1 or moved2

    def move_up(self):
        mat = self.transpose(self.matrix)
        mat, moved1 = self.compress(mat)
        mat, moved2 = self.merge(mat)
        mat, _ = self.compress(mat)
        mat = self.transpose(mat)
        return mat, moved1 or moved2

    def move_down(self):
        mat = self.transpose(self.matrix)
        mat = self.reverse(mat)
        mat, moved1 = self.compress(mat)
        mat, moved2 = self.merge(mat)
        mat, _ = self.compress(mat)
        mat = self.reverse(mat)
        mat = self.transpose(mat)
        return mat, moved1 or moved2

    def game_over(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                if self.matrix[i][j] == 0:
                    return False
                if j < GRID_LEN - 1 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    return False
                if i < GRID_LEN - 1 and self.matrix[i][j] == self.matrix[i + 1][j]:
                    return False
        return True


def main():
    Game()


if __name__ == '__main__':
    main()
