def solve_water_jug_dfs(jug1_capacity, jug2_capacity, target_amount):
    """
    Solves the water jug problem using Depth-First Search (DFS).
    
    Args:
        jug1_capacity: The maximum capacity of the first jug.
        jug2_capacity: The maximum capacity of the second jug.
        target_amount: The target amount of water to be measured.
        
    Returns:
        A list of states representing the solution path, or None if no solution exists.
    """
    
    # State is represented as a tuple: (jug1_current, jug2_current)
    initial_state = (0, 0)
    
    # Stack for DFS. It stores tuples of (current_state, path_to_state)
    stack = [(initial_state, [initial_state])]
    
    # Set to keep track of visited states to avoid cycles and redundant computations
    visited = {initial_state}
    
    # Main DFS loop
    while stack:
        current_state, path = stack.pop()
        jug1, jug2 = current_state

        # Check if the current state is the goal
        if jug1 == target_amount or jug2 == target_amount:
            print("Solution found!")
            return path
        
        # Define all possible moves
        moves = [
            # Fill jug 1 completely
            (jug1_capacity, jug2),
            # Fill jug 2 completely
            (jug1, jug2_capacity),
            # Empty jug 1
            (0, jug2),
            # Empty jug 2
            (jug1, 0),
            # Pour jug 1 to jug 2
            (max(0, jug1 - (jug2_capacity - jug2)), min(jug2_capacity, jug2 + jug1)),
            # Pour jug 2 to jug 1
            (min(jug1_capacity, jug1 + jug2), max(0, jug2 - (jug1_capacity - jug1))),
        ]

        # Explore new states from the current state
        for next_state in moves:
            if next_state not in visited:
                visited.add(next_state)
                new_path = path + [next_state]
                stack.append((next_state, new_path))
                
    # If the stack becomes empty and the goal wasn't reached
    print("No solution found.")
    return None

def print_solution(solution):
    """Prints the solution path in a readable format."""
    if solution:
        for i, (jug1, jug2) in enumerate(solution):
            print(f"Step {i}: Jug 1: {jug1} liters, Jug 2: {jug2} liters")
    else:
        print("No solution path to display.")

def get_dynamic_input():
    """Prompts the user for jug capacities and target amount."""
    try:
        jug1_capacity = int(input("Enter the capacity of Jug 1: "))
        jug2_capacity = int(input("Enter the capacity of Jug 2: "))
        target_amount = int(input("Enter the target amount: "))
        
        if target_amount > max(jug1_capacity, jug2_capacity):
            print("The target amount cannot be greater than the largest jug's capacity.")
            return None, None, None
            
        return jug1_capacity, jug2_capacity, target_amount
    except ValueError:
        print("Invalid input. Please enter whole numbers only.")
        return None, None, None

# --- Main Execution ---
if __name__ == "__main__":
    print("Welcome to the dynamic water jug problem solver using DFS!")
    jug1_cap, jug2_cap, target = get_dynamic_input()

    if jug1_cap is not None:
        print(f"\nSolving the water jug problem with jugs of capacity {jug1_cap} and {jug2_cap}, and a target of {target} gallons.")
        solution_path = solve_water_jug_dfs(jug1_cap, jug2_cap, target)
        print_solution(solution_path)
