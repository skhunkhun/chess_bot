Sunveer Khunkhun
March 5 2023

# HOW TO RUN CODE

    -To run the code type in the command line 'python3 main.py' and everything should run at once.
    - You will get a prompt to choose the number of players ('1' for the AI or '2' for 2 human players).
    - If '1' is selected, then there will be a prompt to choose which colour ('W' for white or 'B' for black).


# EVALUATION FUNCTION

    - The evaluation function gives each piece a score 'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9 and evaluates the risk of taking each piece on any given board.

    - It also checks if pieces has been developed, to determine whether or not it is a winning position by developing their pieces

    - If there is a potential check, the score is updated +10, and the AI will prioritize getting the check

    - If there is a checkmate on the board, the score is updated +1000, and the AI will prioritize the checkmate

# FUNCTIONS IMPLEMENTED

    In 'main.py', I have the initial board state, the main game while loop, a while loop to determine the number of player, and a while loop to determine which side the user wants.

    In 'a2GameFunctions.py' I have a functions for creating and maintaining the game state
        - The main functions include:
            - Determining valid moves
            - Getting all the moves for a current board state
            - Checks, checkmates, and stalemates

    In 'a2AiFunctions.py', I have multiple functions that determine the next move the AI plays based on Min-Max A-B pruning

        - The main functions include:
            - Setting up the AI
            - Min-max-a-b algorithm
            - Evaluating the board
            - Making the best move
