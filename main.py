from a2AiFunctions import *

board = [
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
]

# Get the number of players
num_players = 0
while True:
    try:
        num_players = int(input("Choose the number of players ('1' or '2'): "))
        print(num_players)
        if num_players == 1 or num_players == 2:
            break
        else:
            print("Invalid option. Choose either '1' or '2'")
            continue
    except Exception:
        print("Invalid option. Choose either '1' or '2'")

# Get the player colour
if num_players == 1:
    side = 'white'
    while True:
        side = input("Choose a side ('W' or 'B'): ")
        if side == 'W':
            side = 'black'
            break
        elif side == 'B':
            side = 'white'
            break
        else:
            print("Invalid option. Choose either 'W' or 'B'")

player = 'white'
print_board(board)

# loop that runs the game
while True:

    # Check for stalemate
    copy_board = copy.deepcopy(board)
    if is_stalemate(copy_board, player):
        print(f"Stalemate! It is a draw.")
        break
    
    # Check for checkmate
    copy_board = copy.deepcopy(board)
    if is_checkmate(copy_board, player):
        winner = "Black" if player == "white" else "White"
        print(f"Checkmate! {winner} player has won the game.")
        break
    
    # Determine if player wants to play the bot
    if num_players == 1 and side == player:
        play_chess_bot(board, player)
        print_board(board)
        if player == 'white':
            player = 'black'
        else:
            player = 'white'
        continue
    
    # Enter player moves
    print(f"{player.capitalize()} player's turn.")
    move = input("Enter move (e.g. 'e2 e4'): ")
    if move == 'Q':
        break
    move = move.split(" ")
    if len(move) != 2 or len(move[0]) != 2 or len(move[1]) != 2:
        print("Invalid move. Try again.")
        continue

    try:
        col_from = ord(move[0][0]) - 97
        row_from = int(move[0][1]) - 1
        col_to = ord(move[1][0]) - 97
        row_to = int(move[1][1]) - 1
        piece = board[row_from][col_from]
    except Exception:
        print("Invalid move. Try again.")
        continue
    
    # check if player wants to castle their king
    if (board[row_from][col_from] == 'wK' and board[row_to][col_to] == 'wR') or (board[row_from][col_from] == 'bK' and board[row_to][col_to] == 'bR'):
        new_board = castle(board, row_from, col_from)
        if new_board == None:
            print_board(board)
        else:
            print_board(new_board)
            if player == 'white':
                player = 'black'
            else:
                player = 'white'
        continue
    else:
        # check if a valid move is played
        if not valid_move(board, piece, col_from, row_from, col_to, row_to, player):
            print("Invalid move.")
            continue

    copy_board = copy.deepcopy(board)
    copy_board[row_from][col_from] = None
    copy_board[row_to][col_to] = piece

    if in_check(copy_board, player):
        print("Invalid move: King is in check.")
        continue

    # check if pawn can be promoted
    promoted_piece = promote_pawn(board, piece, col_to, row_to) 

    if promoted_piece != "":
        board[row_from][col_from] = None
        board[row_to][col_to] = promoted_piece
    
    else:
        board[row_from][col_from] = None
        board[row_to][col_to] = piece

    # print the board
    print_board(board)

    # switch the turns
    if player == 'white':
        player = 'black'
    else:
        player = 'white'