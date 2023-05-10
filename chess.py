import numpy as np


class ChessBoard:
    """
    An environment for Chess.
    """

    def __init__(self):
        '''
        Initializes following params:
        board: 8x8 board with piece positions
        white_in_check: boolean
        black_in_check: boolean
        white_to move: boolean
        white_castled: boolean
        black_castled: boolean
            '''
        self.board = np.zeros((8, 8), dtype=int)
        self.pieces = {
                                    0: '',
                                    1: '♙',
                                    2: '♖',
                                    3: '♘',
                                    4: '♗',
                                    5: '♕',
                                    6: '♔',
                                    -1: '♟',
                                    -2: '♜',
                                    -3: '♞',
                                    -4: '♝',
                                    -5: '♛',
                                    -6: '♚'
                                }
        self.squares = {}
        for row in range(8):
            for col in range(8):
                self.squares[(row, col)] = chr(col + ord('a')) + str(row + 1)
        # Pawns
        for i in range(8):
            self.board[1][i] = 1
            self.board[6][i] = -1

        # Rooks
        self.board[0][0] = 2
        self.board[0][7] = 2
        self.board[7][0] = -2
        self.board[7][7] = -2

        # Knights
        self.board[0][1] = 3
        self.board[0][6] = 3
        self.board[7][1] = -3
        self.board[7][6] = -3

        # Bishops
        self.board[0][2] = 4
        self.board[0][5] = 4
        self.board[7][2] = -4
        self.board[7][5] = -4

        # Queens
        self.board[0][3] = 5
        self.board[7][3] = -5

        # Kings
        self.board[0][4] = 6
        self.board[7][4] = -6

        # Track game parameters
        self.white_to_move = True
        self.white_in_check = False
        self.black_in_check = False
        self.white_can_castle = True
        self.black_can_castle = True
        self.win = 0

        # Print the board
        print(np.flip(self.board, axis=0))

    def in_check(self, board, color):
        '''
        This is a function to check for check.
        It takes in a board and a color, and it returns True or False.
        '''

        # Get king position.
        if color == 0:
            king_pos = np.where(board == 6)
        else:
            king_pos = np.where(board == -6)
        king_pos = (king_pos[0][0], king_pos[1][0])

        # Check if any opposite color piece can move to the king position.
        for i in range(8):
            for j in range(8):
                if color == 0:
                    # Check black pieces
                    if board[i][j] < 0:
                        if self.can_move(board[i][j], (i, j), king_pos):
                            print(board[i][j], 'on', (i, j), 'can capture the king on: ', king_pos)
                            return True
                else:
                    # Check white pieces
                    if board[i][j] > 0:
                        if self.can_move(board[i][j], (i, j), king_pos):
                            return True
        return False

    def can_move(self, piece, move_from, move_to):
        """
        Returns True or False.
        Checks if a move from a square to a square by a piece is possible.
        I.e. that it doesn't move through any other pieces, or that it doesn't land on a piece of the same color.
        This does not mean that the move is necessarily legal.
        """
        start_row, start_col = move_from
        end_row, end_col = move_to

        if move_from == move_to:
            return False

        # Pawn
        if abs(piece) == 1:
            if piece == 1:  # White pawn
                if start_row == 1:  # Pawn is on its starting position
                    # Check if it can move one or two squares forward
                    if (end_row == start_row + 1 and end_col == start_col and self.board[end_row][end_col] == 0) or \
                            (end_row == start_row + 2 and end_col == start_col and self.board[end_row][end_col] == 0 and
                             self.board[end_row - 1][end_col] == 0):
                        return True
                else:  # Pawn is not on its starting position
                    # Check if it can move one square forward
                    if end_row == start_row + 1 and end_col == start_col and self.board[end_row][end_col] == 0:
                        return True
                # Check if it can capture diagonally
                if end_row == start_row + 1 and abs(end_col - start_col) == 1 and self.board[end_row][end_col] < 0:
                    return True
            else:  # Black pawn
                if start_row == 6:  # Pawn is on its starting position
                    # Check if it can move one or two squares forward
                    if (end_row == start_row - 1 and end_col == start_col and self.board[end_row][end_col] == 0) or \
                            (end_row == start_row - 2 and end_col == start_col and self.board[end_row][end_col] == 0 and
                             self.board[end_row + 1][end_col] == 0):
                        return True
                else:  # Pawn is not on its starting position
                    # Check if it can move one square forward
                    if end_row == start_row - 1 and end_col == start_col and self.board[end_row][end_col] == 0:
                        return True
                # Check if it can capture diagonally
                if end_row == start_row - 1 and abs(end_col - start_col) == 1 and self.board[end_row][end_col] > 0:
                    return True

        # Rook
        elif abs(piece) == 2:
            # Check if the move is horizontal or vertical
            if start_row == end_row or start_col == end_col:
                # Check if there are no pieces blocking the path
                if start_row == end_row:  # Horizontal move
                    for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                        if self.board[start_row][col] != 0:
                            return False
                else:  # Vertical move
                    for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                        if self.board[row][start_col] != 0:
                            return False
                # Check if the destination square is empty or occupied by an opponent's piece
                if self.board[end_row][end_col] == 0 or (piece > 0 and self.board[end_row][end_col] < 0) or (
                        piece < 0 and self.board[end_row][end_col] > 0):
                    return True

        # Knight
        elif abs(piece) == 3:
            # Check if the move is an L-shape
            if (abs(end_row - start_row) == 2 and abs(end_col - start_col) == 1) or \
                    (abs(end_row - start_row) == 1 and abs(end_col - start_col) == 2):
                # Check if the destination square is empty or occupied by an opponent's piece
                if self.board[end_row][end_col] == 0 or (piece > 0 and self.board[end_row][end_col] < 0) or (
                        piece < 0 and self.board[end_row][end_col] > 0):
                    return True

        # Bishop
        elif abs(piece) == 4:
            # Check if the move is diagonal
            if abs(end_row - start_row) == abs(end_col - start_col):
                # Check if there are no pieces blocking the path
                row_offset = 1 if end_row > start_row else -1
                col_offset = 1 if end_col > start_col else -1
                for offset in range(1, abs(end_row - start_row)):
                    if self.board[start_row + row_offset * offset][start_col + col_offset * offset] != 0:
                        return False
                # Check if the destination square is empty or occupied by an opponent's piece
                if self.board[end_row][end_col] == 0 or (piece > 0 and self.board[end_row][end_col] < 0) or (
                        piece < 0 and self.board[end_row][end_col] > 0):
                    return True

        # Queen
        elif abs(piece) == 5:
            # Check if the move is horizontal, vertical, or diagonal
            if start_row == end_row or start_col == end_col or abs(end_row - start_row) == abs(end_col - start_col):
                # Check if there are no pieces blocking the path
                if start_row == end_row:  # Horizontal move
                    for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                        if self.board[start_row][col] != 0:
                            return False
                elif start_col == end_col:  # Vertical move
                    for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                        if self.board[row][start_col] != 0:
                            return False
                else:  # Diagonal move
                    row_offset = 1 if end_row > start_row else -1
                    col_offset = 1 if end_col > start_col else -1
                    for offset in range(1, abs(end_row - start_row)):
                        if self.board[start_row + row_offset * offset][start_col + col_offset * offset] != 0:
                            return False
                # Check if the destination square is empty or occupied by an opponent's piece
                if self.board[end_row][end_col] == 0 or (piece > 0 and self.board[end_row][end_col] < 0) or (
                        piece < 0 and self.board[end_row][end_col] > 0):
                    return True

        # King
        elif abs(piece) == 6:
            # Castling
            if piece == 6 and self.white_can_castle:
                if move_to == (0, 6) and self.board[0, 5] == 0:
                    return True
                if move_to == (0, 2) and self.board[0, 3] == 0 and self.board[0, 4] == 0:
                    return True
            if piece == -6 and self.black_can_castle:
                if move_to == (7, 6) and self.board[7, 5] == 0:
                    return True
                if move_to == (7, 2) and self.board[7, 3] == 0 and self.board[7, 4] == 0:
                    return True

            # Normal move
            if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
                if self.board[move_to] * piece <= 0:
                    return True

            return False

        # Invalid Piece
        else:
            return False

    def legal_move(self, piece, move_from, move_to):
        """
        Returns True or False.
        Checks if a move from a square to a square by a piece is legal.
        I.e. making the move does not put the king into check.
        """
        temp_board = np.copy(self.board)
        temp_board[move_to[0]][move_to[1]] = piece
        temp_board[move_from[0]][move_from[1]] = 0
        if self.white_to_move:
            if self.in_check(temp_board, 0):
                return False
        else:
            if self.in_check(temp_board, 1):
                return False
        return True

    def print_legal_moves(self, board, color):
        for i in range(8):
            for j in range(8):
                if color == 0:
                    # Check white pieces
                    if board[i][j] > 0:
                        for x in range(8):
                            for y in range(8):
                                if self.can_move(board[i][j], (i, j), (x, y)):
                                    piece_name = self.pieces[board[i][j]]
                                    square_name = self.squares[(x, y)]
                                    print(piece_name, 'to', square_name)
                else:
                    # Check black pieces
                    if board[i][j] < 0:
                        for x in range(8):
                            for y in range(8):
                                if self.can_move(board[i][j], (i, j), (x, y)) and self.legal_move(board[i][j], (i, j), (x, y)):
                                    piece_name = self.pieces[board[i][j]]
                                    square_name = self.squares[(x, y)]
                                    print(piece_name, 'to', square_name)

    def update(self, piece, move_from, move_to):
        # If the move is possible and legal.
        if self.can_move(piece, move_from, move_to) and self.legal_move(piece, move_from, move_to):
            # Check if castling.
            if piece == 6 and move_to == (0, 6):
                self.board[0, 7] = 0
                self.board[0, 5] = 2

            if piece == 6 and move_to == (0, 3):
                self.board[0, 0] = 0
                self.board[0, 4] = 2

            if piece == -6 and move_to == (7, 6):
                self.board[7, 7] = 0
                self.board[7, 5] = 2

            if piece == 6 and move_to == (7, 3):
                self.board[7, 0] = 0
                self.board[7, 4] = 2

            self.board[move_to[0]][move_to[1]] = piece
            self.board[move_from[0]][move_from[1]] = 0

            # Update castling booleans.
            if abs(piece) == 2 or abs(piece) == 6:
                # update the white_castle or black_castle boolean
                if piece > 0:
                    self.white_can_castle = False
                else:
                    self.black_can_castle = False

            # Switch the turn.
            self.white_to_move = not self.white_to_move
            print(np.flip(self.board, axis=0))

        else:
            print("Not legal.")
