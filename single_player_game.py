import random

def get_conflicts(board):
    """
    Calculates the number of pairs of attacking queens (conflicts).
    """
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Check for same row
            if board[i] == board[j]:
                conflicts += 1
            # Check for diagonals
            elif abs(i - j) == abs(board[i] - board[j]):
                conflicts += 1
    return conflicts

def find_min_conflict_move(board):
    """
    Finds a move that results in the minimum number of conflicts.
    """
    n = len(board)
    min_conflicts = get_conflicts(board)
    best_moves = []
    
    print(f"\nEvaluating possible moves to reduce conflicts from {min_conflicts}...")
    
    # Iterate through each column
    for col in range(n):
        original_row = board[col]
        
        # Try moving the queen in this column to every other row
        for row in range(n):
            if row != original_row:
                board[col] = row
                current_conflicts = get_conflicts(board)
                
                print(f"  - Testing move: move queen in col {col} to row {row}. New conflicts: {current_conflicts}")
                
                if current_conflicts < min_conflicts:
                    min_conflicts = current_conflicts
                    best_moves = [(col, row)]
                elif current_conflicts == min_conflicts:
                    best_moves.append((col, row))
        
        # Restore the original position for the next iteration
        board[col] = original_row

    print(f"Minimum conflicts found for this step is: {min_conflicts}")
    return best_moves

def solve_n_queens(n):
    """
    Solves the N-Queens problem using a simple hill-climbing heuristic.
    """
    # Initialize a random board state
    board = [random.randint(0, n - 1) for _ in range(n)]
    
    print(f"Starting with a randomly generated board: {board}")
    
    steps = 0
    while True:
        print("\n" + "="*50)
        print(f"STEP {steps}:")
        print("Current board configuration:", board)
        
        # Calculate heuristic value (conflicts)
        conflicts = get_conflicts(board)
        print(f"Current conflicts (heuristic value): {conflicts}")
        
        if conflicts == 0:
            print("\nSolution found! The number of conflicts is zero.")
            return board
        
        # Find best moves based on min-conflict heuristic
        best_moves = find_min_conflict_move(board)
        
        if not best_moves:
            # Stagnation or local minimum, restart
            print("\nStagnated or reached a local minimum. No move can reduce conflicts.")
            print("Restarting the search from a new random board.")
            board = [random.randint(0, n - 1) for _ in range(n)]
            steps = 0
            continue
            
        # Choose a random best move to avoid infinite loops on plateaus
        col_to_move, new_row = random.choice(best_moves)
        print(f"\nChoosing a move: moving queen in column {col_to_move} to row {new_row}.")
        board[col_to_move] = new_row
        
        steps += 1
        
        if steps > n * n * 2:  # Safety break to prevent infinite loop
            print("\nReached maximum steps. No solution found within the step limit.")
            return None

def print_board(board):
    """
    Prints a visual representation of the board.
    """
    if board is None:
        return
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)

def main():
    """
    Main function to run the N-Queens game.
    """
    try:
        N = int(input("Enter the number of queens (N): "))
        if N <= 0:
            print("Please enter a positive integer.")
            return
        
        print("\n" + "="*50)
        print("SOLVING N-QUEENS USING MIN-CONFLICTS HEURISTIC")
        print("="*50)
        solution = solve_n_queens(N)
        
        print("\n" + "="*50)
        print("FINAL SOLUTION")
        print("="*50)
        print_board(solution)
        
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()