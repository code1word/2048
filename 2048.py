import tkinter as tk
import random
import constants as c

options = [2, 4]


def generic_stack(matrix):
    temp_matrix = [[0] * 4 for _ in range(4)]
    for i in range(4):
        fill_position = 0
        for j in range(4):
            if matrix[i][j] != 0:
                temp_matrix[i][fill_position] = matrix[i][j]
                fill_position += 1
    return temp_matrix


def generic_combine(matrix):
    for i in range(4):
        for j in range(3):
            if matrix[i][j] != 0 and matrix[i][j] == matrix[i][j + 1]:
                matrix[i][j] *= 2
                matrix[i][j + 1] = 0
    return matrix


def generic_reverse(matrix):
    temp_matrix = []
    for i in range(4):
        temp_matrix.append([])
        for j in range(4):
            temp_matrix[i].append(matrix[i][3 - j])
    return temp_matrix


def generic_transpose(matrix):
    temp_matrix = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            temp_matrix[i][j] = matrix[j][i]
    return temp_matrix


class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048')
        self.master.iconbitmap("dy.ico")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.main_grid = tk.Frame(
            self, bg=c.GRID_COLOR, bd=3, width=400, height=400)
        self.main_grid.grid(pady=(110, 20), padx=(20, 20), row=0, column=0)
        self.make_GUI()
        self.start_game()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)
        self.master.bind("<space>", self.reset)

        self.mainloop()

    def make_GUI(self):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=c.EMPTY_CELL_COLOR,
                    width=100,
                    height=100)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        self.score_frame = tk.Frame(self)
        self.score_frame.place(relx=0.5, y=50, anchor="center")
        tk.Label(
            self.score_frame,
            text="Score",
            font=c.SCORE_LABEL_FONT).grid(
            row=0)
        self.score_label = tk.Label(
            self.score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)

    def start_game(self):

        self.allow = True
        self.appear = True

        self.matrix = [[0] * 4 for _ in range(4)]

        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2")
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2")

        self.score = 0

    def stack(self):
        temp_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    temp_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = temp_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    def reverse(self):
        temp_matrix = []
        for i in range(4):
            temp_matrix.append([])
            for j in range(4):
                temp_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = temp_matrix

    def transpose(self):
        temp_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                temp_matrix[i][j] = self.matrix[j][i]
        self.matrix = temp_matrix

    def add_new_tile(self):
        if any(0 in row for row in self.matrix):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            while(self.matrix[row][col] != 0):
                row = random.randint(0, 3)
                col = random.randint(0, 3)
            self.matrix[row][col] = random.choices(options, [9, 1], k=1)[0]

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(
                        bg=c.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(
                        bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLORS[cell_value],
                        fg=c.CELL_NUMBER_COLORS[cell_value],
                        font=c.CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value))
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def left(self, event):
        if self.left_move_exists() and self.allow:
            self.stack()
            self.combine()
            self.stack()
            self.add_new_tile()
            self.update_GUI()
            self.game_over()

    def right(self, event):
        if self.right_move_exists() and self.allow:
            self.reverse()
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
            self.add_new_tile()
            self.update_GUI()
            self.game_over()

    def up(self, event):
        if self.up_move_exists() and self.allow:
            self.transpose()
            self.stack()
            self.combine()
            self.stack()
            self.transpose()
            self.add_new_tile()
            self.update_GUI()
            self.game_over()

    def down(self, event):
        if self.down_move_exists() and self.allow:
            self.transpose()
            self.reverse()
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
            self.transpose()
            self.add_new_tile()
            self.update_GUI()
            self.game_over()

    def right_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1] and self.matrix[i][j] != 0:
                    return True
        temp_matrix = self.matrix
        temp_matrix = generic_reverse(temp_matrix)
        temp_matrix = generic_stack(temp_matrix)
        temp_matrix = generic_combine(temp_matrix)
        temp_matrix = generic_stack(temp_matrix)
        temp_matrix = generic_reverse(temp_matrix)
        if temp_matrix == self.matrix:
            return False
        return True

    def left_move_exists(self):
        for i in range(4):
            for j in range(1, 4):
                if self.matrix[i][j] == self.matrix[i][j - 1] and self.matrix[i][j] != 0:
                    return True
        temp_matrix = self.matrix
        temp_matrix = generic_stack(temp_matrix)
        temp_matrix = generic_combine(temp_matrix)
        temp_matrix = generic_stack(temp_matrix)
        if temp_matrix == self.matrix:
            return False
        return True

    def down_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j] and self.matrix[i][j] != 0:
                    return True
        temp_matrix = self.matrix
        temp_matrix = generic_transpose(temp_matrix)
        temp_matrix = generic_reverse(temp_matrix)
        temp_matrix = generic_stack(temp_matrix)
        temp_matrix = generic_combine(temp_matrix)
        temp_matrix = generic_stack(temp_matrix)
        temp_matrix = generic_reverse(temp_matrix)
        temp_matrix = generic_transpose(temp_matrix)
        if temp_matrix == self.matrix:
            return False
        return True

    def up_move_exists(self):
        for i in range(1, 4):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i - 1][j] and self.matrix[i][j] != 0:
                    return True
        temp_matrix = self.matrix
        temp_matrix = generic_transpose(temp_matrix)
        temp_matrix = generic_stack(temp_matrix)
        temp_matrix = generic_combine(temp_matrix)
        temp_matrix = generic_stack(temp_matrix)
        temp_matrix = generic_transpose(temp_matrix)
        if temp_matrix == self.matrix:
            return False
        return True

    def game_over(self):
        if any(2048 in row for row in self.matrix) and self.appear:
            self.allow = False
            self.appear = False
            self.game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            self.game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                self.game_over_frame,
                text="You win!",
                bg=c.WINNER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT).pack()
            tk.Button(
                self.game_over_frame,
                text="Continue Playing?",
                command=self.clear_wins,
                fg="#000000"
            ).pack()

        elif not any(0 in row for row in self.matrix) and not self.left_move_exists() and not self.right_move_exists() and not self.up_move_exists() and not self.down_move_exists():
            self.game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            self.game_over_frame.place(relx=0.5, rely=0.5, anchor="center")

            if self.appear:
                tk.Label(
                    self.game_over_frame,
                    text="Game over!",
                    bg=c.LOSER_BG,
                    fg=c.GAME_OVER_FONT_COLOR,
                    font=c.GAME_OVER_FONT).pack()
                reset_label_frame = tk.Frame(self.main_grid, borderwidth=1)
                reset_label_frame.place(relx=0.5, rely=0.65, anchor="center")
                tk.Label(
                    reset_label_frame,
                    text="Press Spacebar to Restart",
                    font=("Helvetica", 15, "bold"),
                    bg="#ffffff"
                ).pack()
            else:
                tk.Label(
                    self.game_over_frame,
                    text="Well done!",
                    bg=c.WINNER_BG,
                    fg=c.GAME_OVER_FONT_COLOR,
                    font=c.GAME_OVER_FONT).pack()
                reset_label_frame = tk.Frame(self.main_grid, borderwidth=1)
                reset_label_frame.place(relx=0.5, rely=0.65, anchor="center")
                tk.Label(
                    reset_label_frame,
                    text="Press Spacebar to Restart",
                    font=("Helvetica", 15, "bold"),
                    bg="#ffffff"
                ).pack()

    def reset(self, event):
        for widgets in self.main_grid.winfo_children():
            widgets.destroy()
        for widgets in self.score_frame.winfo_children():
            widgets.destroy()
        self.make_GUI()
        self.start_game()

    def clear_wins(self):
        self.game_over_frame.destroy()
        self.allow = True

def main():
    Game()

if __name__ == "__main__":
    main()