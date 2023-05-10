from chess import ChessBoard
from gui import ChessGUI

def main():
    # Create a new chess board object.
    chess = ChessBoard()
    chessGUI = ChessGUI(chess)

    # Loop until the game is over.
    while True:
        # Get the move from the user
        move = input("Enter your move (e.g. 'e2 e4'): ")

        # Parse the input
        if validate_input(move):
            piece, move_from, move_to = parse_input(chess, move)
        else:
            continue

        # Check the player is moving the correct colour.
        if chess.white_to_move and piece < 0:
            print("Please select a white piece to move.")
            continue
        elif not chess.white_to_move and piece > 0:
            print("Please select a black piece to move.")
            continue

        # Update the board
        chess.update(piece, move_from, move_to)
        chessGUI.draw_board()
        chessGUI.window.update()

def validate_input(move):
    '''
    Validate the input string. Returns True or False.
    '''
    if not isinstance(move, str):
        print('Move must be a string')
        return False
    move_parts = move.split()
    if len(move_parts) != 2:
        print('Move must consist of two parts separated by a space')
        return False
    move_from, move_to = move_parts
    if len(move_from) != 2 or len(move_to) != 2:
        print('Both parts of the move must have length 2')
        return False
    if move_from[0] not in 'abcdefgh' or move_to[0] not in 'abcdefgh':
        print('The first character of both parts of the move must be a letter from a to h')
        return False
    if move_from[1] not in '12345678' or move_to[1] not in '12345678':
        print('The second character of both parts of the move must be a digit from 1 to 8')
        return False

    return True


def parse_input(chess, move):
    """
    Takes in a move and passes it to the chess environment.
    """
    # Parse input
    move_from, move_to = move.split()
    move_from = (int(move_from[1]) - 1, ord(move_from[0]) - ord('a'))
    move_to = (int(move_to[1]) - 1, ord(move_to[0]) - ord('a'))
    piece = chess.board[move_from[0]][move_from[1]]
    return piece, move_from, move_to


if __name__ == "__main__":
    main()