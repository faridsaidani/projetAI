import tkinter as tk
from tkinter import messagebox
import random
import time


class TicTacToe:
    def __init__(self):
        self.board = [[' ']*3 for _ in range(3)]
        self.current_player = None
        self.difficulty = None
        self.human_score = 0
        self.ai_score = 0
        self.tie_score = 0

        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.window.geometry("400x400")

        self.buttons = []
        self._create_board()

        self.score_label = tk.Label(self.window, text="Human: 0 | AI: 0 | Tie: 0")
        self.score_label.pack(pady=10)

        self.reset_button = tk.Button(self.window, text="New Game", font=("Helvetica", 12), command=self._reset_game)
        self.reset_button.pack(pady=10)

    def _create_board(self):
        board_frame = tk.Frame(self.window)
        board_frame.pack()

        for row in range(3):
            row_buttons = []
            for col in range(3):
                button = tk.Button(
                    board_frame,
                    text=' ',
                    font=("Helvetica", 32),
                    width=4,
                    height=2,
                    command=lambda r=row, c=col: self._make_move(r, c)
                )
                button.grid(row=row, column=col, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def _make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = 'X'
            self.buttons[row][col].configure(text='X', state=tk.DISABLED, bg='lightblue')
            self.current_player = 'O'

            if self._check_winner('X'):
                self._show_message("You win!")
                self.human_score += 1
                self._update_score_label()
                self._reset_board()
                return

            if self._board_full():
                self._show_message("It's a tie!")
                self.tie_score += 1
                self._update_score_label()
                self._reset_board()
                return
            if self.difficulty != 'easy':
                self.window.after(500, self._make_computer_move)

    def _make_computer_move(self):
        if self.difficulty == 'medium':
            self._make_random_move()
        elif self.difficulty == 'hard':
            _, best_move = self._minimax(self.board, 'O')
            self.board[best_move[0]][best_move[1]] = 'O'
            self.buttons[best_move[0]][best_move[1]].configure(text='O', state=tk.DISABLED, bg='lightpink')
            self.current_player = 'X'

            if self._check_winner('O'):
                self._update_score_label()
                self._show_message_with_delay("You lose!")
                self.ai_score += 1
                self._reset_board()
                return

            if self._board_full():
                self._update_score_label()
                self._show_message_with_delay("It's a tie!")
                self.tie_score += 1
                self._reset_board()
                return

    def _make_random_move(self):
        empty_cells = [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ' ']
        if empty_cells:
            # Check if AI has a winning move
            for row, col in empty_cells:
                self.board[row][col] = 'O'
                if self._check_winner('O'):
                    self.board[row][col] = 'O'
                    self.buttons[row][col].configure(text='O', state=tk.DISABLED, bg='lightpink')
                    self.current_player = 'X'
                    if self._check_winner('O'):
                        self._update_score_label()
                        self._show_message_with_delay("You lose!")
                        self.ai_score += 1
                    elif self._board_full():
                        self._update_score_label()
                        self._show_message_with_delay("It's a tie!")
                        self.tie_score += 1
                    self._reset_board()
                    return

                self.board[row][col] = ' '  # Undo the move

            # Check if human has a winning move and block it
            for row, col in empty_cells:
                self.board[row][col] = 'X'
                if self._check_winner('X'):
                    self.board[row][col] = 'O'
                    self.buttons[row][col].configure(text='O', state=tk.DISABLED, bg='lightpink')
                    self.current_player = 'X'
                    return

                self.board[row][col] = ' '  # Undo the move

            # If no winning moves, make a random move
            row, col = random.choice(empty_cells)
            self.board[row][col] = 'O'
            self.buttons[row][col].configure(text='O', state=tk.DISABLED, bg='lightpink')
            self.current_player = 'X'

    def _minimax(self, state, player):
        if self._check_winner('X'):
            return -1, None
        elif self._check_winner('O'):
            return 1, None
        elif self._board_full():
            return 0, None

        best_score = float('-inf') if player == 'O' else float('inf')
        best_move = None

        for row in range(3):
            for col in range(3):
                if state[row][col] == ' ':
                    state[row][col] = player
                    score, _ = self._minimax(state, 'X' if player == 'O' else 'O')
                    state[row][col] = ' '

                    if player == 'O' and score > best_score:
                        best_score = score
                        best_move = (row, col)
                    elif player == 'X' and score < best_score:
                        best_score = score
                        best_move = (row, col)

        return best_score, best_move

    def _check_winner(self, player):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == player:
                return True

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == player:
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True

        return False

    def _board_full(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def _reset_board(self):
        self.board = [[' ']*3 for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].configure(text=' ', state=tk.NORMAL, bg='white')

    def _reset_game(self):
        self._reset_board()
        self.current_player = None
        self.window.destroy()
        self.__init__()
        self.run()

    def _update_score_label(self):
        score_text = f"Human: {self.human_score} | AI: {self.ai_score} | Tie: {self.tie_score}"
        self.score_label.config(text=score_text)

    def _show_message(self, message):
        messagebox.showinfo("Game Over", message)

    def _show_message_with_delay(self, message):
        self.window.after(1000, lambda: self._show_message(message))

    def _choose_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.window.withdraw()  # Hide the difficulty selection window
        self._create_side_window()

    def _create_side_window(self):
        side_window = tk.Toplevel(self.window)
        side_window.title("Choose Side")

        side_label = tk.Label(side_window, text="Choose Your Side:")
        side_label.pack()

        x_button = tk.Button(side_window, text="X", font=("Helvetica", 20),
                             command=lambda: self._choose_side('X'))
        x_button.pack(pady=10)

        o_button = tk.Button(side_window, text="O", font=("Helvetica", 20),
                             command=lambda: self._choose_side('O'))
        o_button.pack(pady=10)

    def _choose_side(self, side):
        self.current_player = side
        self.window.deiconify()  # Show the main game window
        self.window.focus_force()
        self.window.title(f"Tic-Tac-Toe - Difficulty: {self.difficulty} - Side: {self.current_player}")

        if self.current_player == 'O':
            self._make_computer_move()

    def run(self):
        difficulty_window = tk.Toplevel(self.window)
        difficulty_window.title("Choose Difficulty")

        difficulty_label = tk.Label(difficulty_window, text="Choose Difficulty:", font=("Helvetica", 16))
        difficulty_label.pack(pady=10)

        easy_button = tk.Button(difficulty_window, text="Easy", font=("Helvetica", 16),
                                command=lambda: self._choose_difficulty('easy'))
        easy_button.pack(pady=10)

        medium_button = tk.Button(difficulty_window, text="Medium", font=("Helvetica", 16),
                                  command=lambda: self._choose_difficulty('medium'))
        medium_button.pack(pady=10)

        hard_button = tk.Button(difficulty_window, text="Hard", font=("Helvetica", 16),
                                command=lambda: self._choose_difficulty('hard'))
        hard_button.pack(pady=10)

        self.window.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()
