# A comprehensive implementation of Blocks World using Means-Ends Analysis
# with detailed terminal output and user input

def is_clear(block, state):
    """Check if a block has nothing on top of it"""
    for b, s in state.items():
        if s == block:
            return False
    return True

def get_on_top_of(block, state):
    """Get the block that is on top of the given block"""
    for b, s in state.items():
        if s == block:
            return b
    return None

def is_goal_state(current, goal):
    """Check if current state matches goal state"""
    return current == goal

def move_block(block_to_move, destination, state):
    """Move a block to a new destination"""
    state[block_to_move] = destination
    return state

def print_state(state, title="State"):
    """Print the state in a readable format"""
    print(f"\n{title}:")
    print("-" * 40)
    for block, destination in sorted(state.items()):
        print(f"  {block} is on {destination}")
    print("-" * 40)

def get_user_input():
    """Get initial and goal states from user input"""
    print("=" * 60)
    print("BLOCKS WORLD SOLVER - MEANS-ENDS ANALYSIS")
    print("=" * 60)
    
    print("\nEnter the states using the format: Block:Destination")
    print("Use 'table' for blocks placed on the table")
    print("Enter one block-destination pair per line")
    print("Press Enter on empty line when done")
    print("\nExample:")
    print("A:table")
    print("B:A")
    print("C:B")
    
    # Get initial state
    print("\n" + "=" * 30)
    print("ENTER INITIAL STATE:")
    print("=" * 30)
    
    initial_state = {}
    while True:
        line = input("Block:Destination (or press Enter to finish): ").strip()
        if not line:
            break
        
        if ':' not in line:
            print("Invalid format! Use Block:Destination format")
            continue
            
        try:
            block, destination = line.split(':', 1)
            block = block.strip().upper()
            destination = destination.strip().lower()
            
            if destination != 'table':
                destination = destination.upper()
            
            initial_state[block] = destination
            print(f"Added: {block} on {destination}")
        except ValueError:
            print("Invalid format! Use Block:Destination format")
    
    if not initial_state:
        print("No initial state entered! Using default example...")
        initial_state = {'B':'table', 'G':'B', 'E':'G', 'C':'E', 'D':'C', 'A':'D'}
    
    # Get goal state
    print("\n" + "=" * 30)
    print("ENTER GOAL STATE:")
    print("=" * 30)
    
    goal_state = {}
    while True:
        line = input("Block:Destination (or press Enter to finish): ").strip()
        if not line:
            break
            
        if ':' not in line:
            print("Invalid format! Use Block:Destination format")
            continue
            
        try:
            block, destination = line.split(':', 1)
            block = block.strip().upper()
            destination = destination.strip().lower()
            
            if destination != 'table':
                destination = destination.upper()
            
            goal_state[block] = destination
            print(f"Added: {block} on {destination}")
        except ValueError:
            print("Invalid format! Use Block:Destination format")
    
    if not goal_state:
        print("No goal state entered! Using default example...")
        goal_state = {'D':'table', 'B':'D', 'G':'B', 'A':'G', 'E':'A', 'C':'E'}
    
    return initial_state, goal_state

def solve_blocks_world(current_state, goal_state):
    """Solve the blocks world problem with detailed output"""
    
    print("\n" + "=" * 60)
    print("STARTING BLOCKS WORLD ANALYSIS")
    print("=" * 60)
    
    print_state(current_state, "INITIAL STATE")
    print_state(goal_state, "GOAL STATE")
    
    solution_moves = []
    max_iterations = 50  # Prevent infinite loops
    iterations = 0
    
    while not is_goal_state(current_state, goal_state) and iterations < max_iterations:
        made_a_move = False
        iterations += 1
        
        print(f"\n{'='*20} ITERATION {iterations} {'='*20}")
        print_state(current_state, "CURRENT STATE")
        
        # Check for differences
        print("\nANALYZING DIFFERENCES FROM GOAL:")
        differences = []
        for block, destination in goal_state.items():
            if current_state[block] != destination:
                current_pos = current_state[block]
                differences.append((block, current_pos, destination))
                print(f"  ❌ {block} should be on {destination} but is on {current_pos}")
        
        if not differences:
            print("  ✅ All blocks are in correct positions!")
            break
        
        print(f"\nFound {len(differences)} block(s) not in goal position")
        print("\nANALYZING POSSIBLE MOVES:")
        print("-" * 40)
        
        # Try to move each misplaced block
        for block, current_pos, goal_pos in differences:
            print(f"\n🔍 ATTEMPTING TO MOVE {block} from {current_pos} to {goal_pos}")
            
            # Check if the block is clear to move
            is_block_clear = is_clear(block, current_state)
            print(f"   Is {block} clear to move? {'✅ YES' if is_block_clear else '❌ NO'}")
            
            if not is_block_clear:
                blocking_block = get_on_top_of(block, current_state)
                print(f"   {block} is blocked by {blocking_block}")
                print(f"   🎯 SUB-GOAL: Move {blocking_block} to table to clear {block}")
                print(f"   ⚡ EXECUTING: Move {blocking_block} to table")
                
                current_state = move_block(blocking_block, 'table', current_state)
                solution_moves.append(f"Move {blocking_block} to table (to clear {block})")
                
                print(f"   ✅ {blocking_block} moved to table")
                print_state(current_state, "STATE AFTER MOVE")
                made_a_move = True
                break
            
            # Block is clear, check if destination is clear
            is_dest_clear = is_clear(goal_pos, current_state) or goal_pos == 'table'
            print(f"   Is destination {goal_pos} clear? {'✅ YES' if is_dest_clear else '❌ NO'}")
            
            if is_dest_clear:
                # Can make the direct move
                print(f"   🎯 DIRECT GOAL: Move {block} to {goal_pos}")
                print(f"   ⚡ EXECUTING: Move {block} to {goal_pos}")
                
                current_state = move_block(block, goal_pos, current_state)
                solution_moves.append(f"Move {block} to {goal_pos}")
                
                print(f"   ✅ {block} successfully moved to {goal_pos}")
                print_state(current_state, "STATE AFTER MOVE")
                made_a_move = True
                break
            else:
                # Destination is blocked
                blocking_dest = get_on_top_of(goal_pos, current_state)
                print(f"   Destination {goal_pos} is blocked by {blocking_dest}")
                print(f"   🎯 SUB-GOAL: Move {blocking_dest} to table to clear {goal_pos}")
                print(f"   ⚡ EXECUTING: Move {blocking_dest} to table")
                
                current_state = move_block(blocking_dest, 'table', current_state)
                solution_moves.append(f"Move {blocking_dest} to table (to clear {goal_pos})")
                
                print(f"   ✅ {blocking_dest} moved to table")
                print_state(current_state, "STATE AFTER MOVE")
                made_a_move = True
                break

        if not made_a_move and not is_goal_state(current_state, goal_state):
            print("\n❌ NO VALID MOVES FOUND!")
            print("The goal might be unreachable or there's a logical error.")
            break
        
        print(f"\nEND OF ITERATION {iterations}")
        print("=" * 60)
    
    # Final results
    print(f"\n{'='*25} FINAL RESULTS {'='*25}")
    
    if is_goal_state(current_state, goal_state):
        print("🎉 SUCCESS! Goal state achieved!")
    else:
        print("❌ Could not reach goal state")
    
    print(f"Total iterations: {iterations}")
    print(f"Total moves made: {len(solution_moves)}")
    
    print_state(current_state, "FINAL STATE")
    
    print("\n📋 COMPLETE SOLUTION SEQUENCE:")
    print("-" * 50)
    if solution_moves:
        for i, move in enumerate(solution_moves, 1):
            print(f"{i:2d}. {move}")
    else:
        print("No moves were needed (already at goal state)")
    
    print("\n" + "=" * 60)
    
    return solution_moves, current_state

def main():
    """Main function to run the blocks world solver"""
    try:
        # Get input from user
        initial_state, goal_state = get_user_input()
        
        # Validate input
        if not initial_state or not goal_state:
            print("Error: Both initial and goal states must be provided!")
            return
        
        # Check if all blocks in goal state exist in initial state
        initial_blocks = set(initial_state.keys())
        goal_blocks = set(goal_state.keys())
        
        if initial_blocks != goal_blocks:
            missing_in_initial = goal_blocks - initial_blocks
            missing_in_goal = initial_blocks - goal_blocks
            
            if missing_in_initial:
                print(f"Error: Blocks in goal state but not in initial state: {missing_in_initial}")
            if missing_in_goal:
                print(f"Error: Blocks in initial state but not in goal state: {missing_in_goal}")
            return
        
        # Solve the puzzle
        solution_moves, final_state = solve_blocks_world(initial_state.copy(), goal_state)
        
        # Ask if user wants to solve another puzzle
        while True:
            choice = input("\nWould you like to solve another puzzle? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                print("\n" + "="*60)
                main()
                break
            elif choice in ['n', 'no']:
                print("\nThank you for using the Blocks World Solver!")
                break
            else:
                print("Please enter 'y' for yes or 'n' for no")
                
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your input and try again.")

if __name__ == "__main__":
    main()