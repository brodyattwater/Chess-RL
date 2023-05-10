import tkinter as tk

class ChessGUI:
    def __init__(self, chess):
        self.chess = chess
        self.window = tk.Tk()
        self.window.title('Chess')
        self.canvas = tk.Canvas(self.window, width=400, height=400)
        self.canvas.pack()
        self.draw_board()


    def draw_board(self):
        for row in range(8):
            for col in range(8):
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                if (row + col) % 2 == 0:
                    color = 'white'
                else:
                    color = 'brown'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                piece = self.chess.board[row][7-col]
                if piece != 0:
                    self.canvas.create_text(x1 + 25, y1 + 25, text=self.chess.pieces[piece], font=("Helvetica", 24))

    def run(self):
        self.window.mainloop()