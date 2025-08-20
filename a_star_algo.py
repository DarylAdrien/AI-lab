# import heapq

# # Class to represent a graph node
# class Node:
#     def __init__(self, name):
#         self.name = name
#         self.neighbors = {}  # Format: {neighbor_node: cost}

#     def add_neighbor(self, neighbor, cost):
#         self.neighbors[neighbor] = cost

# # Heuristic function: provided by the user
# heuristic_costs = {}

# def a_star_shortest_path(graph, start_node_name, goal_node_name):
#     """
#     Finds the shortest path on a graph using the A* algorithm.
#     """
#     # Initialize the priority queue with (f_cost, node_name)
#     start_node = graph[start_node_name]
#     start_h = heuristic_costs.get(start_node.name, 0)
#     frontier = [(start_h, start_node.name)]

#     came_from = {}
#     g_cost = {start_node.name: 0}
    
#     print("\n--- A* Algorithm Trace ---")
#     step_count = 0

#     while frontier:
#         step_count += 1
        
#         # Pop the node with the lowest f_cost
#         f_cost, current_node_name = heapq.heappop(frontier)
        
#         print(f"\nStep {step_count}: Popping node '{current_node_name}' with f_cost = {f_cost}")
#         print(f"  Current g_cost is {g_cost[current_node_name]}")
        
#         if current_node_name == goal_node_name:
#             print("Goal node reached!")
#             return came_from, g_cost[current_node_name]

#         current_node = graph[current_node_name]
#         print(f"  Exploring neighbors of '{current_node_name}':")
        
#         for neighbor_node, cost in current_node.neighbors.items():
#             new_g_cost = g_cost[current_node_name] + cost
            
#             print(f"    - Neighbor: '{neighbor_node.name}' (Edge cost: {cost})")
            
#             if neighbor_node.name not in g_cost or new_g_cost < g_cost[neighbor_node.name]:
#                 g_cost[neighbor_node.name] = new_g_cost
#                 h_cost = heuristic_costs.get(neighbor_node.name, 0)
#                 f_cost = new_g_cost + h_cost
#                 heapq.heappush(frontier, (f_cost, neighbor_node.name))
#                 came_from[neighbor_node.name] = current_node.name
                
#                 print(f"      Path to '{neighbor_node.name}' is improved/new. Updating costs:")
#                 print(f"      g_cost = {new_g_cost}, h_cost = {h_cost}, f_cost = {f_cost}")
#                 print(f"      Pushing to frontier: ({f_cost}, '{neighbor_node.name}')")
#             else:
#                 print(f"      Path to '{neighbor_node.name}' is not an improvement. Skipping.")

#     print("\nNo path found.")
#     return None, None

# def get_dynamic_input():
#     """Prompts the user to build the graph and heuristic table."""
#     graph = {}
    
#     # 1. Get nodes
#     node_names_input = input("Enter node names separated by spaces (e.g., A B C D): ")
#     node_names = node_names_input.split()
#     for name in node_names:
#         graph[name] = Node(name)
    
#     # 2. Get edges and costs
#     print("\nEnter connections (edges) and costs. Format: 'start end cost'")
#     print("Type 'done' when finished.")
#     while True:
#         edge_input = input("> ")
#         if edge_input.lower() == 'done':
#             break
#         try:
#             start, end, cost = edge_input.split()
#             cost = int(cost)
#             if start in graph and end in graph:
#                 graph[start].add_neighbor(graph[end], cost)
#                 graph[end].add_neighbor(graph[start], cost)  # Assuming bidirectional
#             else:
#                 print("Error: Invalid node name.")
#         except (ValueError, IndexError):
#             print("Error: Invalid input format. Please use 'start end cost'.")

#     # 3. Get heuristic costs for each node to the goal
#     global heuristic_costs
#     print("\nEnter heuristic costs (estimated distance) to the goal node.")
#     print("Format: 'node_name cost'")
#     goal_name = input("First, enter the name of the goal node: ")
#     for name in node_names:
#         if name != goal_name:
#             try:
#                 h_cost_input = input(f"Enter heuristic cost for {name} to {goal_name}: ")
#                 heuristic_costs[name] = int(h_cost_input)
#             except ValueError:
#                 print("Error: Invalid cost. Using 0.")
#                 heuristic_costs[name] = 0
    
#     # 4. Get start and goal nodes
#     start_name = input("Enter the starting node name: ")
    
#     return graph, start_name, goal_name

# def reconstruct_path(came_from, start, goal):
#     """Reconstructs the path from the came_from dictionary."""
#     path = []
#     current = goal
#     while current != start:
#         path.append(current)
#         current = came_from[current]
#     path.append(start)
#     path.reverse()
#     return path

# # --- Main Execution ---
# if __name__ == "__main__":
#     print("A* Pathfinding with Dynamic Tree-like Graph")
#     graph, start_node_name, goal_node_name = get_dynamic_input()

#     if start_node_name in graph and goal_node_name in graph:
#         path_info, total_cost = a_star_shortest_path(graph, start_node_name, goal_node_name)
#         if path_info:
#             path = reconstruct_path(path_info, start_node_name, goal_node_name)
#             print(f"\nPath found: {' -> '.join(path)}")
#             print(f"Total cost: {total_cost}")
#         else:
#             print("\nNo path found.")
#     else:
#         print("Invalid start or goal node name.")


import heapq

# Class to represent a graph node
class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}  # Format: {neighbor_node: cost}

    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost

# Heuristic function: provided by the user
heuristic_costs = {}

def a_star_shortest_path(graph, start_node_name, goal_node_name):
    """
    Finds the shortest path on a graph using the A* algorithm with open and closed sets.
    """
    # Initialize the priority queue with (f_cost, node_name)
    start_node = graph[start_node_name]
    start_h = heuristic_costs.get(start_node.name, 0)
    frontier = [(start_h, start_node.name)]

    # --- New Sets Added ---
    open_set = {start_node.name}
    closed_set = set()

    came_from = {}
    g_cost = {start_node.name: 0}
    
    print("\n--- A* Algorithm Trace ---")
    step_count = 0

    while frontier:
        step_count += 1
        
        # Pop the node with the lowest f_cost
        f_cost, current_node_name = heapq.heappop(frontier)
        
        # --- Move node from open_set to closed_set ---
        open_set.remove(current_node_name)
        closed_set.add(current_node_name)

        print(f"\nStep {step_count}: Popping node '{current_node_name}' with f_cost = {f_cost}")
        print(f"  Current g_cost is {g_cost[current_node_name]}")
        
        if current_node_name == goal_node_name:
            print("Goal node reached!")
            return came_from, g_cost[current_node_name]

        current_node = graph[current_node_name]
        print(f"  Exploring neighbors of '{current_node_name}':")
        
        for neighbor_node, cost in current_node.neighbors.items():
            neighbor_name = neighbor_node.name

            # --- Check if neighbor is in the closed_set ---
            if neighbor_name in closed_set:
                print(f"    - Neighbor: '{neighbor_name}' is in the closed set. Skipping.")
                continue

            new_g_cost = g_cost[current_node_name] + cost
            
            print(f"    - Neighbor: '{neighbor_name}' (Edge cost: {cost})")
            
            # Check if this is a better path than any previous one
            if neighbor_name not in g_cost or new_g_cost < g_cost[neighbor_name]:
                g_cost[neighbor_name] = new_g_cost
                h_cost = heuristic_costs.get(neighbor_name, 0)
                f_cost = new_g_cost + h_cost
                
                # --- Only push to frontier if it's not already in the open set with a better or equal cost ---
                if neighbor_name not in open_set:
                    heapq.heappush(frontier, (f_cost, neighbor_name))
                    open_set.add(neighbor_name)
                    came_from[neighbor_name] = current_node_name
                    
                    print(f"      Path to '{neighbor_name}' is improved/new. Updating costs:")
                    print(f"      g_cost = {new_g_cost}, h_cost = {h_cost}, f_cost = {f_cost}")
                    print(f"      Pushing to frontier: ({f_cost}, '{neighbor_name}')")
                else:
                    # This case means the node is already in the frontier but we found a better path.
                    # The original implementation of heapq doesn't support easy priority updates.
                    # The standard way to handle this is to just push the new, better path. The old
                    # path will be processed later but will be discarded because its g_cost
                    # will be higher than the g_cost we just updated.
                    print(f"      Found a better path to '{neighbor_name}' already in frontier. Updating costs...")
                    g_cost[neighbor_name] = new_g_cost
                    came_from[neighbor_name] = current_node_name
                    heapq.heappush(frontier, (f_cost, neighbor_name))
            else:
                print(f"      Path to '{neighbor_name}' is not an improvement. Skipping.")

    print("\nNo path found.")
    return None, None

def get_dynamic_input():
    """Prompts the user to build the graph and heuristic table."""
    graph = {}
    
    # 1. Get nodes
    node_names_input = input("Enter node names separated by spaces (e.g., A B C D): ")
    node_names = node_names_input.split()
    for name in node_names:
        graph[name] = Node(name)
    
    # 2. Get edges and costs
    print("\nEnter connections (edges) and costs. Format: 'start end cost'")
    print("Type 'done' when finished.")
    while True:
        edge_input = input("> ")
        if edge_input.lower() == 'done':
            break
        try:
            start, end, cost = edge_input.split()
            cost = int(cost)
            if start in graph and end in graph:
                graph[start].add_neighbor(graph[end], cost)
                graph[end].add_neighbor(graph[start], cost)  # Assuming bidirectional
            else:
                print("Error: Invalid node name.")
        except (ValueError, IndexError):
            print("Error: Invalid input format. Please use 'start end cost'.")

    # 3. Get heuristic costs for each node to the goal
    global heuristic_costs
    print("\nEnter heuristic costs (estimated distance) to the goal node.")
    print("Format: 'node_name cost'")
    goal_name = input("First, enter the name of the goal node: ")
    for name in node_names:
        if name != goal_name:
            try:
                h_cost_input = input(f"Enter heuristic cost for {name} to {goal_name}: ")
                heuristic_costs[name] = int(h_cost_input)
            except ValueError:
                print("Error: Invalid cost. Using 0.")
                heuristic_costs[name] = 0
    heuristic_costs[goal_name] = 0  # Heuristic cost for the goal is always 0
    
    # 4. Get start and goal nodes
    start_name = input("Enter the starting node name: ")
    
    return graph, start_name, goal_name

def reconstruct_path(came_from, start, goal):
    """Reconstructs the path from the came_from dictionary."""
    path = []
    current = goal
    while current != start:
        if current in came_from:
            path.append(current)
            current = came_from[current]
        else:
            return None # Path not found
    path.append(start)
    path.reverse()
    return path

# --- Main Execution ---
if __name__ == "__main__":
    print("A* Pathfinding with Dynamic Tree-like Graph")
    graph, start_node_name, goal_node_name = get_dynamic_input()

    if start_node_name in graph and goal_node_name in graph:
        path_info, total_cost = a_star_shortest_path(graph, start_node_name, goal_node_name)
        if path_info:
            path = reconstruct_path(path_info, start_node_name, goal_node_name)
            if path:
                print(f"\nPath found: {' -> '.join(path)}")
                print(f"Total cost: {total_cost}")
            else:
                print("\nNo path found (reconstruction failed).")
        else:
            print("\nNo path found.")
    else:
        print("Invalid start or goal node name.")