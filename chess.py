import numpy as np


class ChessGame:
    """
    An environment for Chess.
    """

    def __init__(self):
        '''
        Initializes following params:
        board: 8x8 board with piece positions
        white_to move: boolean to tell which player it is to move
        white_can_castle: boolean to tell can white castle?
        black_can_castle: boolean to tell can black castle?
        '''
        self.board = np.zeros((8, 8), dtype=int)

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
        self.board[0][4] = 5
        self.board[7][4] = -5

        # Kings
        self.board[0][3] = 6
        self.board[7][3] = -6

        # Track game parameters
        self.to_move = 'White'
        self.white_can_short_castle = True
        self.white_can_long_castle = True
        self.black_can_short_castle = True
        self.black_can_long_castle = True
        self.winner = None

    def in_check(self, color):
        '''
        This is a function to check for check.
        It takes in a board and a color, and it returns True or False.
        '''
        # Get king position.
        if color == 'White':
            king_pos = np.where(self.board == 6)
            enemy_piece = np.where(self.board < 0)
        elif color == 'Black':
            king_pos = np.where(self.board == -6)
            enemy_piece = np.where(self.board > 0)
        king_pos = (king_pos[0][0], king_pos[1][0])

        # Check if any opposite color piece can move to the king position.
        for i, j in zip(enemy_piece[0], enemy_piece[1]):
            if self.can_move(self.board[i][j], (i, j), king_pos):
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
                # Check if it can capture diagonally (inc. en passant)
                if end_row == start_row + 1 and abs(end_col - start_col) == 1:
                    if self.board[end_row][end_col] < 0 or self.board[start_row][end_col] == -1:
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
                if end_row == start_row - 1 and abs(end_col - start_col) == 1:
                    if self.board[end_row][end_col] > 0 or self.board[start_row][end_col] == 1:
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
            if piece == 6:
                if move_to == (0, 1) and self.board[0, 2] == 0 and self.board[
                    0, 1] == 0 and self.white_can_short_castle:
                    return True
                if move_to == (0, 5) and self.board[0, 4] == 0 and self.board[0, 5] == 0 and self.board[
                    0, 6] == 0 and self.white_can_long_castle:
                    return True
            if piece == -6:
                if move_to == (7, 1) and self.board[7, 2] == 0 and self.board[
                    7, 1] == 0 and self.black_can_short_castle:
                    return True
                if move_to == (7, 5) and self.board[7, 4] == 0 and self.board[7, 5] == 0 and self.board[
                    7, 6] == 0 and self.black_can_long_castle:
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
        returns True if a move from a square to a square by a piece is legal.
        """
        temp = self.board[move_to[0]][move_to[1]]
        self.board[move_to[0]][move_to[1]] = piece
        self.board[move_from[0]][move_from[1]] = 0
        if self.in_check(self.to_move):
            self.board[move_to[0]][move_to[1]] = temp
            self.board[move_from[0]][move_from[1]] = piece
            return False
        else:
            self.board[move_to[0]][move_to[1]] = temp
            self.board[move_from[0]][move_from[1]] = piece
            return True

    def no_legal_moves(self):
        '''
        returns true if there exists no legal moves for the colour to play.
        '''
        if self.to_move == 'White':
            pieces = np.where(self.board > 0)
        elif self.to_move == 'Black':
            pieces = np.where(self.board < 0)

        for i, j in zip(pieces[0], pieces[1]):
            for x in range(0, 7):
                for y in range(0, 7):
                    if self.can_move(self.board[i][j], (i, j), (x, y)) and self.legal_move(self.board[i][j], (i, j),
                                                                                           (x, y)):
                        return False
        return True

    def update(self, piece, move_from, move_to):
        # If the move is possible and legal.
        if self.can_move(piece, move_from, move_to):
            if self.legal_move(piece, move_from, move_to):
                # Check if castling.
                if piece == 6 and move_to == (0, 5):
                    self.board[0, 7] = 0
                    self.board[0, 4] = 2

                if piece == 6 and move_to == (0, 1):
                    self.board[0, 0] = 0
                    self.board[0, 2] = 2

                if piece == -6 and move_to == (7, 5):
                    self.board[7, 7] = 0
                    self.board[7, 4] = -2

                if piece == -6 and move_to == (7, 1):
                    self.board[7, 0] = 0
                    self.board[7, 2] = -2

                # Promotion
                if piece == 1 and move_to[0] == 7:
                    piece = 5
                if piece == -1 and move_to[0] == 0:
                    piece = -5

                # En Passant
                if piece == 1 and move_to[0] == 5:
                    self.board[move_from[0]][move_to[1]] = 0
                if piece == -1 and move_to[0] == 2:
                    self.board[move_from[0]][move_to[1]] = 0

                self.board[move_to[0]][move_to[1]] = piece
                self.board[move_from[0]][move_from[1]] = 0

                # Castling Rights
                if piece == 6:
                    self.white_can_short_castle = False
                    self.white_can_long_castle = False
                    # print("White lost both short and long castle")
                if piece == -6:
                    self.black_can_short_castle = False
                    self.black_can_long_castle = False
                    # print("Black lost both short and long castle")
                if piece == 2 and move_from[1] == 0 or move_to == (0, 0):
                    self.white_can_short_castle = False
                    # print("White lost short castle")
                if piece == 2 and move_from[1] == 7 or move_to == (0, 7):
                    self.white_can_long_castle = False
                    # print("White lost long castle")
                if piece == -2 and move_from[1] == 0 or move_to == (7, 0):
                    self.black_can_short_castle = False
                    # print("Black lost short castle")
                if piece == -2 and move_from[1] == 7 or move_to == (7, 7):
                    self.black_can_long_castle = False
                    # print("Black lost long castle")

                # Check for end conditions otherwise switch the turn to the other player
                if self.to_move == 'White':
                    self.to_move = 'Black'
                elif self.to_move == 'Black':
                    self.to_move = 'White'

                if self.no_legal_moves():
                    if self.in_check(self.to_move):
                        print("Checkmate.")
                        self.winner = self.to_move
                    else:
                        print("Stalemate.")
