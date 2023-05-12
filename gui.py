import tkinter as tk
from PIL import ImageTk, Image
from chess import ChessGame
import random

PhotoImage = ImageTk.PhotoImage
SPRITE_SIZE = 100
SQUARE_COUNT = 8
SQUARE_SIZE = 100  # pixels


class Chess:
    def __init__(self):
        super().__init__()
        self.chess = ChessGame()
        self.window = tk.Tk()
        self.window.attributes("-topmost", True)
        self.canvas = tk.Canvas(height=SQUARE_COUNT * SQUARE_SIZE, width=SQUARE_COUNT * SQUARE_SIZE)
        self.canvas.bind("<Button-1>", self.interact)
        self.canvas.pack()
        self.first_click = None
        bB, bN, bK, bQ, bP, bR, wB, wR, wK, wQ, wP, wN = load_images()
        self.sprite_dict = {1: wP, 2: wR, 3: wN, 4: wB, 5: wQ, 6: wK, -1: bP, -2: bR, -3: bN, -4: bB, -5: bQ, -6: bK}

    def run(self):
        self.draw_board()
        self.window.mainloop()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(SQUARE_COUNT):
            for col in range(SQUARE_COUNT):
                x1 = col * SQUARE_SIZE
                y1 = row * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                if (row, col) == self.first_click:
                    color = 'red'
                elif (row + col) % 2 == 0:
                    color = 'white'
                else:
                    color = 'green'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                piece = self.chess.board[row][col]
                if piece != 0:
                    self.canvas.create_image(x1 + SQUARE_SIZE / 2, y1 + SQUARE_SIZE / 2, image=self.sprite_dict[piece])
        self.window.update()

    def interact(self, event):
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE

        if self.first_click is None:
            self.first_click = (row, col)

        else:
            piece, move_from, move_to = (self.chess.board[self.first_click[0], self.first_click[1]], self.first_click, (row, col))
            self.first_click = None

            # Check the player is moving the correct colour.
            if self.chess.to_move == 'White' and piece < 0:
                print("Please select a white piece to move.")
            elif self.chess.to_move == 'Black' and piece > 0:
                print("Please select a black piece to move.")
            # Update the board
            else:
                self.chess.update(piece, move_from, move_to)
                random_move = random.choice(self.chess.return_legal_moves())
                piece = self.chess.board[random_move[0], random_move[1]]
                move_from = (random_move[0], random_move[1])
                move_to = (random_move[2], random_move[3])
                self.chess.update(piece, move_from, move_to)
        self.draw_board()
        self.window.update()


def load_images():
    bB = PhotoImage(
        Image.open("C:/Users/Brody/Documents/GitHub/Chess-RL/maestro/bB.bmp").resize((SPRITE_SIZE, SPRITE_SIZE)))
    bN = PhotoImage(
        Image.open("C:/Users/Brody/Documents/GitHub/Chess-RL/maestro/bN.bmp").resize((SPRITE_SIZE, SPRITE_SIZE)))
    bK = PhotoImage(
        Image.open("C:/Users/Brody/Documents/GitHub/Chess-RL/maestro/bK.bmp").resize((SPRITE_SIZE, SPRITE_SIZE)))
    bQ = PhotoImage(
        Image.open("C:/Users/Brody/Documents/GitHub/Chess-RL/maestro/bQ.bmp").resize((SPRITE_SIZE, SPRITE_SIZE)))
    bP = PhotoImage(
        Image.open("C:/Users/Brody/Documents/GitHub/Chess-RL/maestro/bP.bmp").resize((SPRITE_SIZE, SPRITE_SIZE)))
    bR = PhotoImage(
        Image.open("C:/Users/Brody/Documents/GitHub/Chess-RL/maestro/bR.bmp").resize((SPRITE_SIZE, SPRITE_SIZE)))
    wB = PhotoImage(
        Image.open("C:/Users/Brody/Documents/GitHub/Chess-RL/maestro/wB.bmp").resize((SPRITE_SIZE, SPRITE_SIZE)))
    wR = PhotoImage(
        Image.open("C:/Users/Brody/Documents/GitHub/Chess-RL/maestro/wR.bmp").resize((SPRITE_SIZE, SPRITE_SIZE)))
    wK = PhotoImage(
        Image.open("C:/Users/Brody/Documents/GitHub/Chess-RL/maestro/wK.bmp").resize((SPRITE_SIZE, SPRITE_SIZE)))
    wQ = PhotoImage(
        Image.open("C:/Users/Brody/Documents/GitHub/Chess-RL/maestro/wQ.bmp").resize((SPRITE_SIZE, SPRITE_SIZE)))
    wP = PhotoImage(
        Image.open("C:/Users/Brody/Documents/GitHub/Chess-RL/maestro/wP.bmp").resize((SPRITE_SIZE, SPRITE_SIZE)))
    wN = PhotoImage(
        Image.open("C:/Users/Brody/Documents/GitHub/Chess-RL/maestro/wN.bmp").resize((SPRITE_SIZE, SPRITE_SIZE)))
    return bB, bN, bK, bQ, bP, bR, wB, wR, wK, wQ, wP, wN
