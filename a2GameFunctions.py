import copy
import random

# Function to print the current board state
def print_board(board):

    for row_num in range (0, 8):
        print(row_num + 1, end="  ")
        for col_num in range(0, 8):
            square = board[row_num][col_num]
            # use '-' to represent empty squares
            print(f"{square or '- '} ", end="")
        print()


    # print the column letters
    print("   A  B  C  D  E  F  G  H")

# Function to determine if a valid chess move has been played
def valid_move(board, piece, col_from, row_from, col_to, row_to, player):

    if not piece:
        # print("No piece at specified location. Try again.")
        return False
    
    if piece[0] != player[0]:
        # print("Invalid move: Cannot move opposing players piece")
        return False
    
    if 'P' in piece:
        if not valid_pawn_move(board, piece, col_from, row_from, col_to, row_to):
            # print("Invalid Pawn move.")
            return False
    
    if 'B' in piece:
        if not valid_bishop_move(board, piece, col_from, row_from, col_to, row_to):
            # print("Invalid move: Bishops can only move diagonally")
            return False
   
    if 'R' in piece:
        if not valid_rook_move(board, piece, col_from, row_from, col_to, row_to):
            # print("Invalid move: Rooks can only move vertically and horizontally")
            return False

    if 'Q' in piece:
        if not valid_queen_move(board, piece, col_from, row_from, col_to, row_to):
            # print("Invalid move: Queen can only move diagonally or vertically/horizontally")
            return False
        
    if 'N' in piece:
        if not valid_knight_move(board, piece, col_from, row_from, col_to, row_to):
            # print("Invalid move: Knights can only move in an 'L' shape")
            return False
        
    if 'K' in piece:
        if not valid_king_move(board, piece, col_from, row_from, col_to, row_to):
            # print("Invalid move: Kings 1 spot in any direction")
            return False

    return True

# Function to determine if a valid pawn move has been played
def valid_pawn_move(board, piece, col_from, row_from, col_to, row_to):

    if piece == 'wP':
        if row_to <= row_from:
            return False
        elif abs(col_to - col_from) == 1 and row_to == row_from + 1 and board[row_to][col_to] and board[row_to][col_to][0] != piece[0]:
            return True
        elif board[row_to][col_to] is None:
            if row_from == 1:
                if col_from == col_to and (row_to == row_from + 2 or row_to == row_from + 1):
                    return True
                else:
                    return False
            elif col_from == col_to and row_to == row_from + 1:
                return True
        
    if piece == 'bP':
        if row_to >= row_from:
            return False
        elif abs(col_to - col_from) == 1 and row_to == row_from - 1 and board[row_to][col_to] and board[row_to][col_to][0] != piece[0]:
            return True
        elif board[row_to][col_to] is None:
            if row_from == 6:
                if col_from == col_to and (row_to == row_from - 2 or row_to == row_from - 1):
                    return True
                else:
                    return False
            elif col_from == col_to and row_to == row_from - 1:
                return True
    return False

# Function to determine if a valid bishop move has been played
def valid_bishop_move(board, piece, col_from, row_from, col_to, row_to):

    # Get the current diagonals that the bishop can move to
    if abs(row_to - row_from) != abs(col_to - col_from):
        return False
    row_dir = 1 if row_to > row_from else -1
    col_dir = 1 if col_to > col_from else -1
    curr_row, curr_col = row_from + row_dir, col_from + col_dir
    while curr_row != row_to and curr_col != col_to:
        if board[curr_row][curr_col]:
            return False
        curr_row += row_dir
        curr_col += col_dir
    if board[row_to][col_to]:
        return board[row_to][col_to].startswith('b' if piece.startswith('w') else 'w')
    return True

# Function to determine if a valid rook move has been played
def valid_rook_move(board, piece, col_from, row_from, col_to, row_to):
        
    if row_from != row_to and col_from != col_to:
        return False
    if row_from == row_to:
        col_dir = 1 if col_to > col_from else -1
        curr_col = col_from + col_dir
        while curr_col != col_to:
            if board[row_from][curr_col]:
                return False
            curr_col += col_dir
        if board[row_to][col_to]:
            return board[row_to][col_to].startswith('b' if piece.startswith('w') else 'w')
    else:
        row_dir = 1 if row_to > row_from else -1
        curr_row = row_from + row_dir
        while curr_row != row_to:
            if board[curr_row][col_from]:
                return False
            curr_row += row_dir
        if board[row_to][col_to]:
            return board[row_to][col_to].startswith('b' if piece.startswith('w') else 'w')
    return True

# Function to determine if a valid Knight move has been played
def valid_knight_move(board, piece, col_from, row_from, col_to, row_to):

    row_diff = abs(row_to - row_from)
    col_diff = abs(col_to - col_from)

    if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
        if not board[row_to][col_to] or board[row_to][col_to][0] != piece[0]:
            # target square is empty or has an opposing piece
            return True

    return False

# Function to determine if a valid queen move has been played
def valid_queen_move(board, piece, col_from, row_from, col_to, row_to):

    # use the valid rook move and valid bishop move functions to determine the queen movements
    if (row_from == row_to and valid_rook_move(board, piece, col_from, row_from, col_to, row_to)) or (col_from == col_to and valid_rook_move(board, piece, col_from, row_from, col_to, row_to)):
        return True
    
    if  abs(row_to - row_from) == abs(col_to - col_from) and valid_bishop_move(board, piece, col_from, row_from, col_to, row_to):
        return True

    return False

# Function to determine if a valid king move has been made
def valid_king_move(board, piece, col_from, row_from, col_to, row_to):

    # check all moves within one space of the king
    if abs(row_to - row_from) > 1 or abs(col_to - col_from) > 1:
        return False
    
    # check if same colour piece is in the square
    if board[row_to][col_to] and board[row_to][col_to].startswith(piece[0]):
        return False
    
    return True

# Function to determine whether or not a player wants to castle
def castle(board, row, col):
    # Check if king is in starting position
    if board[row][col] != 'wK' and board[row][col] != 'bK':
        print("Invalid move: piece is not a king")
        return None

    # Determine which side the player wants to castle on
    if col == 4:
        # King-side castle
        if board[row][7] == 'wR' or board[row][7] == 'bR':
            if board[row][5] == None and board[row][6] == None:
                print(board[row][col])
                board[row][6] = 'wK' if board[row][col] == 'wK' else 'bK'
                board[row][5] = 'wR' if board[row][col] == 'wK' else 'bR'
                board[row][4] = None
                board[row][7] = None
                return board
            else:
                print("Invalid move: pieces in the way of castle")
                return None
        else:
            print("Invalid move: no rook to castle with")
            return None

    elif col == 0:
        # Queen-side castle
        if board[row][0] == 'wR' or board[row][0] == 'bR':
            if board[row][1] == None and board[row][2] == None and board[row][3] == None:
                board[row][2] = 'wK' if board[row][col] == 'wK' else 'bK'
                board[row][3] = 'wR' if board[row][col] == 'wK' else 'bR'
                board[row][4] = None
                board[row][0] = None
                return board
            else:
                print("Invalid move: pieces in the way of castle")
                return None
        else:
            print("Invalid move: no rook to castle with")
            return None

    else:
        print("Invalid move: king is not in starting position")
        return None

# Function to determine if a player wants to promote a pawn
def promote_pawn(board, piece, col_to, row_to):

    if (row_to == 0 and piece == 'bP') or (row_to == 7 and piece == 'wP'):
        while True:
            new_piece = input("Enter piece to promote pawn to (Q, R, B, N): ")
            if new_piece not in ('Q', 'R', 'B', 'N'):
                print("Invalid piece. Try again.")
                continue
            board[row_to][col_to] = f"{piece[0]}{new_piece}"
            return board[row_to][col_to]
    return ""

# Function to determine if the player is in check
def in_check(board, player):

    # Find the position of the king of the given player
    king_pos = None
    for row in range(8):
        for col in range(8):
            if board[row][col] == f"{player[0]}K":
                king_pos = (row, col)
                break
        if king_pos:
            break

    # Check if any opponent pieces can attack the king
    opponent = "w" if player[0] == "b" else "b"
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.startswith(opponent):
                if valid_move(board, piece, col, row, king_pos[1], king_pos[0], opponent):
                    return True

    return False

# Function to get all of the valid king moves and return them
def get_king_moves(board, king_pos):
    row, col = king_pos
    
    possible_moves = []
    
    # Loop over all eight possible king moves in all directions
    for row_diff in [-1, 0, 1]:
        for col_diff in [-1, 0, 1]:
            if row_diff == 0 and col_diff == 0:
                continue
            
            # Calculate the new position
            row_to = row + row_diff
            col_to = col + col_diff
            
            # Check if the new position is within the board bounds
            if row_to < 0 or row_to > 7 or col_to < 0 or col_to > 7:
                continue
                
            # Check if the new position is not occupied by a friendly piece
            if board[row_to][col_to] and board[row_to][col_to].startswith(board[row][col][0]):
                continue
                
            possible_moves.append((row, col, row_to, col_to))
    
    return possible_moves

# Function to retrieve all of the valid moves within a given board state
def get_piece_moves(board, row ,col, player):
    piece = board[row][col]
    moves = []

    if piece == 'wP':
        if row > 0 and board[row+1][col] is None:
            moves.append((row, col, row+1, col))
            
            # Move two squares forward on first move
            if row == 1 and board[row+2][col] is None:
                moves.append((row, col, row+2, col))
                
        # Capture diagonally to the left
        if row > 0 and col > 0 and board[row+1][col-1] is not None and board[row+1][col-1][0] == 'b':
            moves.append((row, col, row+1, col-1))
        
        # Capture diagonally to the right
        if row > 0 and col < 7 and board[row+1][col+1] is not None and board[row+1][col+1][0] == 'b':
            moves.append((row, col, row+1, col+1))
    
    if piece == 'bP':
        if row < 7 and board[row-1][col] is None:
            moves.append((row, col, row-1, col))
            
            # Move two squares forward on first move
            if row == 6 and board[row-2][col] is None:
                moves.append((row, col, row-2, col))
                
        if row < 7 and col > 0 and board[row-1][col-1] is not None and board[row-1][col-1][0] == 'w':
            moves.append((row, col, row-1, col-1))
        
        if row < 7 and col < 7 and board[row-1][col+1] is not None and board[row-1][col+1][0] == 'w':
            moves.append((row, col, row-1, col+1))

    # Get rook moves
    if 'R' in piece:
        # All rook moves
        rook_moves = [(0,1), (0,-1), (1,0), (-1,0)]

        for direction in rook_moves:
            for i in range(1, 8):
                row_to = row + i*direction[0]
                col_to = col + i*direction[1]
                if row_to < 0 or row_to > 7 or col_to < 0 or col_to > 7:
                    break
                if board[row_to][col_to] is None:
                    moves.append((row, col, row_to, col_to))
                elif board[row_to][col_to][0] != piece[0]:
                    moves.append((row, col, row_to, col_to))
                    break
                else:
                    break
    # Get knight moves
    if 'N' in piece:
        # All knight moves
        knight_moves = [(2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]

        for move in knight_moves:
            row_diff, col_diff = move
            row_to = row + row_diff
            col_to = col + col_diff
            # print(row_to, col_to)
            if (row_to < 8 and row_to >=0) and (col_to < 8 and col_to >= 0) and (board[row_to][col_to] is None or board[row_to][col_to][0] != piece[0]):
                moves.append((row, col, row_to, col_to))

    # Get bishop moves
    if 'B' in piece:
        for i in range(1, 8):
            # Diagonal moves
            for x, y in [(i, i), (-i, i), (i, -i), (-i, -i)]:
                row_to, col_to = row + x, col + y
                if (row_to < 8 and row_to >=0) and (col_to < 8 and col_to >= 0):
                    if board[row_to][col_to] is None:
                        moves.append((row, col, row_to, col_to))
                    elif board[row_to][col_to][0] != piece[0]:
                        moves.append((row, col, row_to, col_to))
                        break
                    else:
                        break
    
    # Get queen moves
    if 'Q' in piece:
        rook_moves = [(0,1), (0,-1), (1,0), (-1,0)]
        for direction in rook_moves:
            for i in range(1, 8):
                row_to = row + i*direction[0]
                col_to = col + i*direction[1]
                if row_to < 0 or row_to > 7 or col_to < 0 or col_to > 7:
                    break
                if board[row_to][col_to] is None:
                    moves.append((row, col, row_to, col_to))
                elif board[row_to][col_to][0] != piece[0]:
                    moves.append((row, col, row_to, col_to))
                    break
                else:
                    break

        for i in range(1, 8):
            # Diagonal moves
            for x, y in [(i, i), (-i, i), (i, -i), (-i, -i)]:
                row_to, col_to = row + x, col + y
                if (row_to < 8 and row_to >=0) and (col_to < 8 and col_to >= 0):
                    if board[row_to][col_to] is None:
                        moves.append((row, col, row_to, col_to))
                    elif board[row_to][col_to][0] != piece[0]:
                        moves.append((row, col, row_to, col_to))
                        break
                    else:
                        break
    
    # Get king moves
    if 'K' in piece:
        king_pos = (row, col)
        for row, col, row_to, col_to in get_king_moves(board, king_pos):
            copy_board = copy.deepcopy(board)
            copy_board[row_to][col_to] = copy_board[row][col] 
            copy_board[row][col] = None
        
            if not in_check(copy_board, player):
                moves.append((row, col, row_to, col_to))

    return moves

# Function to get all moves within a current board
def get_all_moves(board, player):
    all_moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None and piece.startswith(player[0]):
                moves = get_piece_moves(board, row, col, player)
                for row, col, row_to, col_to in moves:
                    if valid_move(board, piece, col, row, col_to, row_to, player): # check if move is valid
                        copy_board = copy.deepcopy(board)
                        copy_board[row_to][col_to] = copy_board[row][col] 
                        copy_board[row][col] = None
                        if not in_check(copy_board, player): # check if player is in check
                            all_moves.extend([(row, col, row_to, col_to)])
    return all_moves

# Function to determine if there is a checkmate
def is_checkmate(board, player):

    # Get all current board moves and if the king in not in check for any move, then there is no checkmate
    all_moves = get_all_moves(board, player)
    for row, col, row_to, col_to in all_moves:
        copy_board = copy.deepcopy(board)
        copy_board[row_to][col_to] = copy_board[row][col] 
        copy_board[row][col] = None
        if not in_check(copy_board, player):
            return False
   
    return True

# Function to determine if there is a stalemate
def is_stalemate(board, player):

    # First, check if the player's king is in check
    if in_check(board, player):
        return False
    
    # get all possible moves for the player
    all_moves = get_all_moves(board, player)
    if len(all_moves) == 0:
        return True
    
    return False