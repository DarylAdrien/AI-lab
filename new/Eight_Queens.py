
def heuristic(board):
    
    h = 0
    n = len(board)
    for c1 in range(n):
        for c2 in range(c1 + 1, n):
            r1, r2 = board[c1], board[c2]
            if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                h += 1
    return h

def print_board(board, title=None):
   
    n = len(board)
    if title:
        print(title)
    for r in range(n):
        row_cells = []
        for c in range(n):
            row_cells.append('Q' if board[c] == r else '.')
        print(' '.join(row_cells))
    print(f"Board list: {board}")
    print(f"Heuristic (attacking pairs): {heuristic(board)}")
    print()


def get_best_neighbor(board):
   
    n = len(board)
    current_h = heuristic(board)
    best_board = board[:]
    best_h = current_h
    moved = (None, None, None)

    for col in range(n):
        original_row = board[col]
        for row in range(n):
            if row == original_row:
                continue
            new_board = board[:]
            new_board[col] = row
            h = heuristic(new_board)
            if h < best_h:
                best_board = new_board
                best_h = h
                moved = (col, original_row, row)
    return best_board, best_h, moved

def hill_climbing(board, max_steps=200):
    
    step = 0
    board = board[:] 
    print_board(board, title="Initial Board (Hill Climbing)")

    while step < max_steps:
        step += 1
        neighbor, neighbor_h, moved = get_best_neighbor(board)
        current_h = heuristic(board)

        print(f"Step {step}: Current h={current_h}")
        if moved[0] is not None:
            col, fr, to = moved
            print(f"  Move: column {col}, row {fr} → row {to}")
        else:
            print("  No improving move found.")
        print_board(neighbor, title=f"Board after step {step}")

        if neighbor_h >= current_h:  # stuck or solved
            if neighbor_h == 0:
                print("Hill climbing found a solution.\n")
            else:
                print(" Hill climbing stuck at local optimum.\n")
            return neighbor
        board = neighbor

    print("Hill climbing stopped due to step limit.\n")
    return board

def solve_backtracking(preferred):
   
    n = len(preferred)
    board = [-1] * n
    rows_used = set()
    diag1 = set()
    diag2 = set()
    steps = 0

    def place(col):
        nonlocal steps
        if col == n:
            return True

        # try preferred row first
        candidates = list(range(n))
        pref = preferred[col]
        if 0 <= pref < n:
            candidates.remove(pref)
            candidates = [pref] + candidates

        for r in candidates:
            steps += 1
            if r in rows_used or (r - col) in diag1 or (r + col) in diag2:
                continue  # conflict

            # place queen
            board[col] = r
            rows_used.add(r); diag1.add(r - col); diag2.add(r + col)

            if place(col + 1):
                return True

            # backtrack
            board[col] = -1
            rows_used.remove(r); diag1.remove(r - col); diag2.remove(r + col)

        return False

    place(0)
    return board, steps


if __name__ == "__main__":
    n = int(input("Enter the number of queens to be placed: "))
    print("Enter integers (space-separated)")
    # print("Example: 0 4 7 5 2 6 1 3\n")

    try:
        user_input = list(map(int, input("Enter initial board: ").split()))
    except Exception:
        print("Invalid input format.")
        raise SystemExit

    if len(user_input) != n or any(x < 0 or x >= n for x in user_input):
        print("Invalid input! Must be 8 numbers between 0 and 7.")
    else:
        # 1. Try hill climbing
        hc_result = hill_climbing(user_input, max_steps=200)

        if heuristic(hc_result) == 0:
            print(" Final Solution (Hill Climbing):", hc_result)
        else:
            # 2. Fall back to backtracking
            print("Falling back to Backtracking.\n")
            solution, steps = solve_backtracking(user_input)
            print(" Final Solution (Backtracking):", solution)
            print_board(solution)
            print(f"(Tried {steps} row placements in backtracking)")
