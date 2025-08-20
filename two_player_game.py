import math

# A function to print the Tic-Tac-Toe board
def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
    print("\n")

# A function to check if the game has ended (win, lose, or draw)
def check_game_over(board):
    # Check rows for a win
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != ' ':
            return row[0]
    
    # Check columns for a win
    for col in range(len(board)):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
            
    # Check diagonals for a win
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
        
    # Check for a draw
    if all(' ' not in row for row in board):
        return "Draw"
    
    # Game is not over
    return None

# The Minimax algorithm
def minimax(board, depth, is_maximizing):
    score = check_game_over(board)
    
    # Return a value based on the game state
    if score == 'X':
        return 1
    if score == 'O':
        return -1
    if score == "Draw":
        return 0

    # If the maximizing player (AI) is to play
    if is_maximizing:
        best_score = -math.inf
        
        # Iterate through all empty cells
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == ' ':
                    board[i][j] = 'X' # Make the move
                    
                    # Recursively call minimax and get the score
                    score = minimax(board, depth + 1, False)
                    best_score = max(score, best_score)
                    
                    # Undo the move (backtracking)
                    board[i][j] = ' '
        
        return best_score
        
    # If the minimizing player (Human) is to play
    else:
        best_score = math.inf
        
        # Iterate through all empty cells
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == ' ':
                    board[i][j] = 'O' # Make the move
                    
                    # Recursively call minimax and get the score
                    score = minimax(board, depth + 1, True)
                    best_score = min(score, best_score)
                    
                    # Undo the move (backtracking)
                    board[i][j] = ' '
        
        return best_score

# Main game loop
def play_game():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    
    print("Welcome to Tic-Tac-Toe!")
    print("You are 'O' and the AI is 'X'.")
    print("The board is a grid from 1 to 9:")
    print("1 | 2 | 3")
    print("--+---+--")
    print("4 | 5 | 6")
    print("--+---+--")
    print("7 | 8 | 9\n")
    
    current_player = 'O' # Human goes first
    
    while True:
        print_board(board)
        
        if current_player == 'O':
            # Human player's turn
            try:
                move = int(input("Enter your move (1-9): "))
                if not 1 <= move <= 9:
                    print("Invalid input. Please enter a number between 1 and 9.")
                    continue
                
                row, col = (move - 1) // 3, (move - 1) % 3
                
                if board[row][col] != ' ':
                    print("That position is already taken. Try again.")
                    continue
                
                board[row][col] = 'O'
            
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
        
        else:
            # AI's turn (Minimax)
            print("AI's turn. Calculating the best move...")
            best_score = -math.inf
            best_move = None
            
            # The AI iterates through all possible moves to find the best one
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'X'
                        
                        # Get the score for this potential move using minimax
                        score = minimax(board, 0, False)
                        
                        print(f"  - For move ({i+1},{j+1}), the minimax score is: {score}")
                        
                        board[i][j] = ' ' # Undo the move
                        
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
            
            # Make the best move found by the AI
            board[best_move[0]][best_move[1]] = 'X'
            print(f"AI chooses move at ({best_move[0]+1},{best_move[1]+1}).")
            
        # Check if the game is over after the move
        game_result = check_game_over(board)
        if game_result:
            print_board(board)
            if game_result == 'Draw':
                print("It's a draw!")
            else:
                print(f"Player '{game_result}' wins!")
            break
            
        # Switch players
        current_player = 'X' if current_player == 'O' else 'O'

# Run the game
if __name__ == "__main__":
    play_game()