from collections import deque

def solve_water_jug_dfs(jug1_capacity, jug2_capacity, target_amount, target_jug_number):
    """
    Solves the water jug problem using Depth-First Search (DFS).
    
    Args:
        jug1_capacity: The maximum capacity of the first jug.
        jug2_capacity: The maximum capacity of the second jug.
        target_amount: The target amount of water to be measured.
        target_jug_number: The jug (1 or 2) that should contain the target amount.
        
    Returns:
        A list of states representing the solution path, or None if no solution exists.
    """
    
    initial_state = (0, 0)
    stack = [(initial_state, [initial_state])]
    visited = {initial_state}
    step_count = 0

    while stack:
        current_state, path = stack.pop()
        jug1, jug2 = current_state
        step_count += 1
        
        # Print the current state being processed
        print(f"\nProcessing Step {step_count}: Jug 1 = {jug1}, Jug 2 = {jug2}")
        
        # Check if the current state is the goal based on the target jug
        if (target_jug_number == 1 and jug1 == target_amount) or \
           (target_jug_number == 2 and jug2 == target_amount):
            print("Solution found!")
            return path
        
        # Define all possible moves
        moves = [
            (jug1_capacity, jug2),  # Fill jug 1
            (jug1, jug2_capacity),  # Fill jug 2
            (0, jug2),              # Empty jug 1
            (jug1, 0),              # Empty jug 2
            # Pour jug 1 to jug 2
            (max(0, jug1 - (jug2_capacity - jug2)), min(jug2_capacity, jug2 + jug1)),
            # Pour jug 2 to jug 1
            (min(jug1_capacity, jug1 + jug2), max(0, jug2 - (jug1_capacity - jug1))),
        ]

        for next_state in moves:
            if next_state not in visited:
                visited.add(next_state)
                new_path = path + [next_state]
                stack.append((next_state, new_path))
                
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
    """Prompts the user for jug capacities, target amount, and target jug."""
    try:
        jug1_capacity = int(input("Enter the capacity of Jug 1: "))
        jug2_capacity = int(input("Enter the capacity of Jug 2: "))
        target_amount = int(input("Enter the target amount: "))
        target_jug_number = int(input("Enter the jug number to store the target amount (1 or 2): "))
        
        if target_amount > max(jug1_capacity, jug2_capacity):
            print("The target amount cannot be greater than the largest jug's capacity.")
            return None, None, None, None
            
        if target_jug_number not in [1, 2]:
            print("Invalid target jug number. Please enter 1 or 2.")
            return None, None, None, None

        return jug1_capacity, jug2_capacity, target_amount, target_jug_number
    except ValueError:
        print("Invalid input. Please enter whole numbers only.")
        return None, None, None, None

# --- Main Execution ---
if __name__ == "__main__":
    print("Welcome to the dynamic water jug problem solver using DFS!")
    jug1_cap, jug2_cap, target, target_jug = get_dynamic_input()

    if jug1_cap is not None:
        print(f"\nSolving the water jug problem with jugs of capacity {jug1_cap} and {jug2_cap}, and a target of {target} gallons in Jug {target_jug}.")
        solution_path = solve_water_jug_dfs(jug1_cap, jug2_cap, target, target_jug)
        print_solution(solution_path)
