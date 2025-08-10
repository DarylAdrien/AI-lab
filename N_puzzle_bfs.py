def bfs_n_puzzle(initial_state, goal_state):
    if not is_solvable(initial_state):
        return None, "This puzzle is unsolvable."
    
    queue = deque([(initial_state, [])]) # (state, path)
    visited = {initial_state}
    step_count = 0

    while queue:
        current_state, path = queue.popleft()
        step_count += 1
        
        print(f"\nProcessing Step {step_count}:")
        for row in current_state:
            print(row)
        
        if current_state == goal_state:
            return path + [current_state], "Solution found!"

        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [current_state]
                queue.append((neighbor, new_path))
                
    return None, "Solution not found (shouldn't happen for solvable puzzles)."

def get_inversions(puzzle):
    inversions = 0
    flat_puzzle = [item for sublist in puzzle for item in sublist if item != 0]
    for i in range(len(flat_puzzle)):
        for j in range(i + 1, len(flat_puzzle)):
            if flat_puzzle[i] > flat_puzzle[j]:
                inversions += 1
    return inversions

def find_blank_position(puzzle):
    for r in range(len(puzzle)):
        for c in range(len(puzzle[0])):
            if puzzle[r][c] == 0:
                return r, c
    return -1, -1

def is_solvable(puzzle):
    n = len(puzzle)
    inversions = get_inversions(puzzle)
    blank_row, _ = find_blank_position(puzzle)

    if n % 2 == 1:
        # For odd-sized grids (e.g., 3x3), solvable if inversions are even
        return inversions % 2 == 0
    else:
        # For even-sized grids (e.g., 4x4)
        # Solvable if inversions + blank_row_from_bottom is even
        blank_row_from_bottom = n - blank_row
        return (inversions + blank_row_from_bottom) % 2 == 0

def get_neighbors(state):
    neighbors = []
    blank_r, blank_c = find_blank_position(state)
    n = len(state)
    
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
    
    for dr, dc in moves:
        new_r, new_c = blank_r + dr, blank_c + dc
        
        if 0 <= new_r < n and 0 <= new_c < n:
            new_state = [list(row) for row in state]
            new_state[blank_r][blank_c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[blank_r][blank_c]
            neighbors.append(tuple(tuple(row) for row in new_state))
            
    return neighbors

def get_dynamic_input():
    try:
        n = int(input("Enter the size of the puzzle (e.g., 3 for a 3x3 puzzle): "))
        print(f"Enter the puzzle tiles row by row, separated by spaces. Use 0 for the blank space.")
        print(f"For a {n}x{n} puzzle, enter {n*n} numbers.")
        
        puzzle = []
        for i in range(n):
            row_input = input(f"Enter row {i+1}: ").split()
            if len(row_input) != n:
                print(f"Error: Row must contain exactly {n} numbers.")
                return None, None
            row = [int(num) for num in row_input]
            puzzle.append(row)

        initial_state = tuple(tuple(row) for row in puzzle)

        # Create the goal state dynamically
        goal_list = list(range(1, n*n))
        goal_list.append(0)
        goal_state = tuple(tuple(goal_list[i*n : (i+1)*n]) for i in range(n))

        return initial_state, goal_state
    
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return None, None
    
# --- Main Execution ---

if __name__ == "__main__":
    initial_state, goal_state = get_dynamic_input()

    if initial_state and goal_state:
        print("\nInitial State:")
        for row in initial_state:
            print(row)
        
        print("\nGoal State:")
        for row in goal_state:
            print(row)

        print("\nStarting search...")
        solution_path, message = bfs_n_puzzle(initial_state, goal_state)

        if solution_path:
            print(message)
            print("Number of steps:", len(solution_path) - 1)
            for i, state in enumerate(solution_path):
                print(f"\nStep {i}:")
                for row in state:
                    print(row)
        else:
            print(message)
