import heapq

# Heuristic costs, to be filled by user
heuristic_costs = {}

class Node:
    def __init__(self, name, is_and=False):
        self.name = name
        self.is_and = is_and
        self.neighbors = []  # List of neighbor node names
        self.cost = 0

def ao_star(graph, start_node_name, goal_node_name):
    """
    Solves the problem using the AO* algorithm.
    """
    
    # Stores the optimal path to each node
    optimal_path = {}
    
    # Priority queue: (f_cost, node_name)
    frontier = [(heuristic_costs.get(start_node_name, 0), start_node_name)]
    
    # Stores the g_cost (cost from start)
    g_cost = {start_node_name: 0}
    
    while frontier:
        f_cost, current_node_name = heapq.heappop(frontier)
        
        if current_node_name == goal_node_name:
            return optimal_path, g_cost[current_node_name]
            
        current_node = graph[current_node_name]
        
        # If it's an AND node, we need to solve all subproblems
        if current_node.is_and:
            total_g_cost_for_and = 0
            
            # Recalculate f_cost for the AND node based on its neighbors
            new_f_cost = 0
            for neighbor_name in current_node.neighbors:
                # The cost of an AND node is the sum of costs of all its subproblems
                # We add 1 for the cost to traverse the edge to each subproblem
                g_cost[neighbor_name] = g_cost[current_node_name] + 1
                new_f_cost += g_cost[neighbor_name] + heuristic_costs.get(neighbor_name, 0)
                
            # If the new path is better, update and push to frontier
            if new_f_cost < f_cost:
                 heapq.heappush(frontier, (new_f_cost, current_node_name))

        # If it's an OR node, we choose the best path
        else:
            for neighbor_name in current_node.neighbors:
                new_g_cost = g_cost[current_node_name] + 1
                
                if neighbor_name not in g_cost or new_g_cost < g_cost[neighbor_name]:
                    g_cost[neighbor_name] = new_g_cost
                    h_cost = heuristic_costs.get(neighbor_name, 0)
                    f_cost = new_g_cost + h_cost
                    heapq.heappush(frontier, (f_cost, neighbor_name))
                    optimal_path[neighbor_name] = current_node_name
                    
    return None, None

def get_dynamic_input():
    """Prompts the user to build the graph and heuristic table."""
    graph = {}
    
    # 1. Get nodes
    node_names_input = input("Enter node names separated by spaces (e.g., A B C D): ")
    node_names = node_names_input.split()
    for name in node_names:
        is_and_input = input(f"Is node {name} an AND node? (yes/no): ")
        is_and = is_and_input.lower() == 'yes'
        graph[name] = Node(name, is_and)
    
    # 2. Get connections
    print("\nEnter connections. Format: 'start_node end_node'")
    print("Type 'done' when finished.")
    while True:
        edge_input = input("> ")
        if edge_input.lower() == 'done':
            break
        try:
            start, end = edge_input.split()
            if start in graph and end in graph:
                graph[start].neighbors.append(end)
            else:
                print("Error: Invalid node name.")
        except (ValueError, IndexError):
            print("Error: Invalid input format. Please use 'start_node end_node'.")

    # 3. Get heuristic costs
    global heuristic_costs
    print("\nEnter heuristic costs (estimated distance) to the goal node.")
    print("Format: 'node_name cost'")
    goal_name = input("First, enter the name of the goal node: ")
    for name in node_names:
        try:
            h_cost_input = input(f"Enter heuristic cost for {name} to {goal_name}: ")
            heuristic_costs[name] = int(h_cost_input)
        except ValueError:
            print("Error: Invalid cost. Using 0.")
            heuristic_costs[name] = 0
    
    # 4. Get start and goal nodes
    start_name = input("Enter the starting node name: ")
    
    return graph, start_name, goal_name

def reconstruct_path(optimal_path, start, goal):
    """Reconstructs the path from the optimal_path dictionary."""
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = optimal_path[current]
    path.append(start)
    path.reverse()
    return path

# --- Main Execution ---
if __name__ == "__main__":
    print("AO* Search with Dynamic AND-OR Graph")
    graph, start_node_name, goal_node_name = get_dynamic_input()

    if start_node_name in graph and goal_node_name in graph:
        optimal_path, total_cost = ao_star(graph, start_node_name, goal_node_name)
        if optimal_path:
            path = reconstruct_path(optimal_path, start_node_name, goal_node_name)
            print(f"\nOptimal path found: {' -> '.join(path)}")
            print(f"Total cost: {total_cost}")
        else:
            print("\nNo solution found.")
    else:
        print("Invalid start or goal node name.")
