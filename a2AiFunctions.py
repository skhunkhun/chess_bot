from a2GameFunctions import *
# Function to make a move
def make_move(board, move):

    row_from, col_from, row_to, col_to = move
    piece = board[row_from][col_from]

    if (row_to == 0 and piece == 'bP') or (row_to == 7 and piece == 'wP'):
        board[row_to][col_to] = f"{piece[0]}{'Q'}"
        board[row_from][col_from] = None
    else:
        board[row_from][col_from] = None
        board[row_to][col_to] = piece

# Function to evaluate the current board and make a move
def evaluate_board(board, player):
    # Define piece values
    piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
    score = 0

    if in_check(board, player):
        if player == 'w':
            score -= 10  # Add a score if opponent's king is in check
        else:
            score += 10

    # Evaluate each piece on the board
    for row_idx, row in enumerate(board):
        for piece in row:
            if piece is not None:
                # Evaluate the piece
                piece_score = piece_values[piece[1]]
                if piece[0] == player:
                    score -= piece_score
                else:
                    score += piece_score

    # Evaluate if each piece has developed
    for row_idx, row in enumerate(board):
        for piece in row:
            if piece is not None and piece[0] == player:
                if (player == 'w' and row_idx in (0, 1)):
                    score -= 1
                if (player == 'b' and row_idx in (6, 7)):
                    score += 1
                if (player == 'w' and row_idx in (2, 3, 4, 5)):
                    score -= 1
                elif (player == 'b' and row_idx in (1, 2, 3, 4)):
                    score += 1

    return score

# function that implements a Min-max tree with A-B pruning
def min_max_a_b(board, depth, alpha, beta, maximizing_player):
    player = 'w'
    if maximizing_player:
        player = 'w'
    else:
        player = 'b'

    score = 0
    
    # check if current board contains a checkmate
    if is_checkmate(board, player):
        if player == 'b':
            score += 1000 
        else:
            score -= 1000
        return score + evaluate_board(board, player)
    
    # check if current board contains a stalemate
    if is_stalemate(board, player):
        return score + evaluate_board(board, player)

    if depth == 0:
        return score + evaluate_board(board, player)
    
    # potential moves for white player
    if maximizing_player:
        max_eval = -float('inf')
        for move in get_all_moves(board, player):
            board_copy = copy.deepcopy(board)
            make_move(board_copy, move)
            eval = min_max_a_b(board_copy, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        # potential moves for black player
        min_eval = float('inf')
        for move in get_all_moves(board, player):
            board_copy = copy.deepcopy(board)
            make_move(board_copy, move)
            eval = min_max_a_b(board_copy, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# function to setup and play the chess bot
def play_chess_bot(board, player):
    
    maximizing_player = True
    if player[0] == 'w':
        maximizing_player = False
    else:
        maximizing_player = True

    # get the best move for the AI 
    best_move = None
    best_eval = -float('inf')
    for move in get_all_moves(board, player):
        board_copy = copy.deepcopy(board)
        make_move(board_copy, move)
        eval = min_max_a_b(board_copy, 2, -float('inf'), float('inf'), maximizing_player)
        if eval > best_eval:
            best_eval = eval
            best_move = move

    make_move(board, best_move)
    print(f"{player} player moved {board[best_move[2]][best_move[3]]} from {chr(97+best_move[1])}{best_move[0]+1} to {chr(97+best_move[3])}{1+best_move[2]}")