# A simplified implementation of Blocks World using Means-Ends Analysis

def is_clear(block, state):
    for b, s in state.items():
        if s == block:
            return False
    return True

def get_on_top_of(block, state):
    for b, s in state.items():
        if s == block:
            return b
    return None

def is_goal_state(current, goal):
    return current == goal

def move_block(block_to_move, destination, state):
    state[block_to_move] = destination
    return state

def solve_blocks_world(current_state, goal_state):
    print("Initial State:", current_state)
    print("Goal State:", goal_state)
    
    solution_steps = []
    
    while not is_goal_state(current_state, goal_state):
        made_a_move = False
        
        # Check for blocks not in their final position
        for block, destination in goal_state.items():
            if current_state[block] != destination:
                
                # Check if the block is clear to move
                if is_clear(block, current_state):
                    
                    # Check if the destination is clear
                    if is_clear(destination, current_state) or destination == 'table':
                        
                        # Apply the move operator
                        current_state = move_block(block, destination, current_state)
                        solution_steps.append(f"Move {block} to {destination}")
                        made_a_move = True
                        break # Start over after a move is made
                    else:
                        # Sub-goal: clear the destination
                        block_on_top = get_on_top_of(destination, current_state)
                        if block_on_top:
                            current_state = move_block(block_on_top, 'table', current_state)
                            solution_steps.append(f"Sub-goal: Move {block_on_top} to table to clear {destination}")
                            made_a_move = True
                            break
                else:
                    # Sub-goal: clear the block to be moved
                    block_on_top = get_on_top_of(block, current_state)
                    if block_on_top:
                        current_state = move_block(block_on_top, 'table', current_state)
                        solution_steps.append(f"Sub-goal: Move {block_on_top} to table to clear {block}")
                        made_a_move = True
                        break

        if not made_a_move and not is_goal_state(current_state, goal_state):
            print("Could not find a valid move to make. Goal might be unreachable.")
            break
            
    return solution_steps, current_state

# Sample Input and Output
# Initial state: A on B, B on Table, C on Table
# Goal state: C on A, A on B, B on Table
initial_state = {'A': 'B', 'B': 'table', 'C': 'table'}
goal_state = {'C': 'A', 'A': 'B', 'B': 'table'}

solution, final_state = solve_blocks_world(initial_state, goal_state)
print("\nSolution Steps:")
for step in solution:
    print(f"- {step}")

print("\nFinal State:", final_state)