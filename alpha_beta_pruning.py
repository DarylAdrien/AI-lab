import math
import sys

# Set a high recursion limit for deep trees
sys.setrecursionlimit(2000)

def minimax(node, depth, maximizing_player, verbose=True):
    """
    Standard Minimax algorithm to find the best move.
    """
    if 'value' in node:
        return node['value'], 1

    if maximizing_player:
        best_value = -math.inf
        nodes_visited = 1
        
        for child_key in node.get('children', {}):
            child_node = node['children'][child_key]
            value, visited = minimax(child_node, depth + 1, False, verbose)
            best_value = max(best_value, value)
            nodes_visited += visited
            
            if verbose:
                print(f"  {'|  ' * depth}Minimax(MAX): Exploring child '{child_key}'. Current best value: {best_value}")

        return best_value, nodes_visited
    else: # Minimizing player
        best_value = math.inf
        nodes_visited = 1
        
        for child_key in node.get('children', {}):
            child_node = node['children'][child_key]
            value, visited = minimax(child_node, depth + 1, True, verbose)
            best_value = min(best_value, value)
            nodes_visited += visited
            
            if verbose:
                print(f"  {'|  ' * depth}Minimax(MIN): Exploring child '{child_key}'. Current best value: {best_value}")
                
        return best_value, nodes_visited

def alphabeta(node, depth, alpha, beta, maximizing_player, verbose=True):
    """
    Alpha-Beta Pruning algorithm to find the best move.
    """
    if 'value' in node:
        return node['value'], 1

    if maximizing_player:
        best_value = -math.inf
        nodes_visited = 1
        
        for child_key in node.get('children', {}):
            child_node = node['children'][child_key]
            value, visited = alphabeta(child_node, depth + 1, alpha, beta, False, verbose)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            nodes_visited += visited

            if verbose:
                print(f"  {'|  ' * depth}Alpha-Beta(MAX): Exploring child '{child_key}'. Alpha: {alpha}, Beta: {beta}")

            if beta <= alpha:
                if verbose:
                    print(f"  {'|  ' * depth}--- PRUNING BRANCH '{child_key}' (beta <= alpha) ---")
                return best_value, nodes_visited
                
        return best_value, nodes_visited
    else: # Minimizing player
        best_value = math.inf
        nodes_visited = 1
        
        for child_key in node.get('children', {}):
            child_node = node['children'][child_key]
            value, visited = alphabeta(child_node, depth + 1, alpha, beta, True, verbose)
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            nodes_visited += visited

            if verbose:
                print(f"  {'|  ' * depth}Alpha-Beta(MIN): Exploring child '{child_key}'. Alpha: {alpha}, Beta: {beta}")
                
            if beta <= alpha:
                if verbose:
                    print(f"  {'|  ' * depth}--- PRUNING BRANCH '{child_key}' (beta <= alpha) ---")
                return best_value, nodes_visited
                
        return best_value, nodes_visited

def get_user_tree():
    """
    Prompts the user to create a game tree.
    """
    print("\n--- Enter Your Game Tree ---")
    print("Example: A simple tree with 2 children, each having 2 children.")
    print("Root has children A and B. A has children C(value=3) and D(value=5). B has children E(value=2) and F(value=9).")
    
    tree_nodes = {}
    
    def build_node(node_name):
        children_str = input(f"Enter children for node '{node_name}' (e.g., C, D) or 'leaf' if it has a value: ").strip().upper()
        
        if children_str == 'LEAF':
            try:
                value = int(input(f"Enter the value for leaf node '{node_name}': "))
                return {'value': value}
            except ValueError:
                print("Invalid input. Please enter an integer value.")
                return build_node(node_name)
        else:
            children_list = children_str.split(',')
            node = {'children': {}}
            for child in children_list:
                child = child.strip()
                node['children'][child] = build_node(child)
            return node

    root_name = input("Enter the name of the root node (e.g., Root): ").strip().upper()
    return {root_name: build_node(root_name)}

def visualize_tree(node, prefix="", is_last=True):
    """
    Visualizes the tree structure.
    """
    node_name = list(node.keys())[0]
    node_content = node[node_name]
    
    if 'value' in node_content:
        print(prefix + ("└── " if is_last else "├── ") + f"{node_name}: Value = {node_content['value']}")
    else:
        print(prefix + ("└── " if is_last else "├── ") + f"{node_name}")
        
        children = list(node_content.get('children', {}).keys())
        for i, child_key in enumerate(children):
            is_last_child = (i == len(children) - 1)
            visualize_tree({child_key: node_content['children'][child_key]}, prefix + ("    " if is_last else "│   "), is_last_child)

def main():
    """
    Main function to run the comparison.
    """
    print("Welcome to the Minimax vs. Alpha-Beta Pruning demonstration.")
    
    user_tree = get_user_tree()
    root_key = list(user_tree.keys())[0]
    
    print("\n" + "="*50)
    print("Your Custom Game Tree")
    print("="*50)
    visualize_tree(user_tree)
    
    print("\n" + "="*50)
    print("1. MINIMAX ALGORITHM (Full Search)")
    print("="*50)
    minimax_result, minimax_visited = minimax(user_tree[root_key], 0, True)
    
    print("\n" + "="*50)
    print("2. ALPHA-BETA PRUNING")
    print("="*50)
    alphabeta_result, alphabeta_visited = alphabeta(user_tree[root_key], 0, -math.inf, math.inf, True)
    
    print("\n" + "="*50)
    print("PERFORMANCE COMPARISON")
    print("="*50)
    print(f"Minimax: Best Value = {minimax_result}, Nodes Visited = {minimax_visited}")
    print(f"Alpha-Beta: Best Value = {alphabeta_result}, Nodes Visited = {alphabeta_visited}")

    if alphabeta_visited < minimax_visited:
        print("\nConclusion: Alpha-Beta Pruning explored fewer nodes and is thus more efficient.")
    elif alphabeta_visited == minimax_visited:
        print("\nConclusion: Alpha-Beta Pruning explored the same number of nodes. Pruning did not occur on this specific tree.")
    else:
        print("\nConclusion: Minimax was more efficient in this case.")

if __name__ == "__main__":
    main()