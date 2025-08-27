
import math
import random
from typing import List, Tuple, Optional

EMPTY = "."
HUMAN = "X"
AI = "O"

# Board Utilities

def make_board(n: int) -> List[List[str]]:
    return [[EMPTY for _ in range(n)] for _ in range(n)]

def print_board(board: List[List[str]]) -> None:
    n = len(board)
    header = "   " + " ".join(f"{j+1:2d}" for j in range(n))
    print(header)
    for i, row in enumerate(board):
        print(f"{i+1:2d} " + " ".join(f"{c:2s}" for c in row))
    print()

def available_moves(board: List[List[str]]) -> List[Tuple[int, int]]:
    moves = []
    for i, row in enumerate(board):
        for j, c in enumerate(row):
            if c == EMPTY:
                moves.append((i, j))
    return moves

def in_bounds(n: int, r: int, c: int) -> bool:
    return 0 <= r < n and 0 <= c < n

# Win / Draw Detection 

def check_winner(board: List[List[str]], K: int) -> Optional[str]:
    """Return 'X' or 'O' if someone has K in a row, else None."""
    n = len(board)
    dirs = [(1,0), (0,1), (1,1), (1,-1)]
    for r in range(n):
        for c in range(n):
            if board[r][c] == EMPTY: 
                continue
            player = board[r][c]
            for dr, dc in dirs:
                cnt = 0
                rr, cc = r, c
                while in_bounds(n, rr, cc) and board[rr][cc] == player:
                    cnt += 1
                    if cnt == K:
                        return player
                    rr += dr
                    cc += dc
    return None

def is_full(board: List[List[str]]) -> bool:
    return all(cell != EMPTY for row in board for cell in row)

# Heuristic Evaluation

def evaluate_window(window: List[str], me: str, opp: str) -> int:
    
    if opp in window and me in window:
        return 0  
    me_cnt = window.count(me)
    opp_cnt = window.count(opp)
    if opp_cnt == 0 and me_cnt > 0:
        # 1, 2, 3 in a row... scale up
        return 10 ** me_cnt
    if me_cnt == 0 and opp_cnt > 0:
        return -(10 ** opp_cnt)
    return 0  # all empty contributes nothing

def score_board(board: List[List[str]], K: int, me: str) -> int:
    """Heuristic score from 'me' perspective."""
    n = len(board)
    opp = AI if me == HUMAN else HUMAN
    total = 0

    # helper to extract K-length windows in a direction
    def scan_direction(dr: int, dc: int):
        nonlocal total
        for r in range(n):
            for c in range(n):
                window = []
                rr, cc = r, c
                for _ in range(K):
                    if not in_bounds(n, rr, cc):
                        window = []
                        break
                    window.append(board[rr][cc])
                    rr += dr
                    cc += dc
                if window:
                    total += evaluate_window(window, me, opp)

    # rows, cols, diag, anti-diag
    scan_direction(0, 1)
    scan_direction(1, 0)
    scan_direction(1, 1)
    scan_direction(1, -1)

    return total

#Minimax with Alpha-Beta 

def terminal_state(board: List[List[str]], K: int) -> Optional[int]:
    """Return a large +/- score if terminal, else None."""
    winner = check_winner(board, K)
    if winner == AI:
        return +10**6
    if winner == HUMAN:
        return -10**6
    if is_full(board):
        return 0
    return None

def minimax(board: List[List[str]], K: int, depth: int, alpha: int, beta: int, maximizing: bool) -> Tuple[int, Optional[Tuple[int,int]]]:
    term = terminal_state(board, K)
    if term is not None:
        return term, None
    if depth == 0:
        return score_board(board, K, AI), None

    moves = available_moves(board)

    # Move ordering: try near center first to speed pruning
    n = len(board)
    center = (n-1)/2
    moves.sort(key=lambda m: abs(m[0]-center)+abs(m[1]-center))

    if maximizing:
        best_val = -math.inf
        best_move = None
        for (r, c) in moves:
            board[r][c] = AI
            val, _ = minimax(board, K, depth-1, alpha, beta, False)
            board[r][c] = EMPTY
            if val > best_val:
                best_val, best_move = val, (r, c)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return best_val, best_move
    else:
        best_val = math.inf
        best_move = None
        for (r, c) in moves:
            board[r][c] = HUMAN
            val, _ = minimax(board, K, depth-1, alpha, beta, True)
            board[r][c] = EMPTY
            if val < best_val:
                best_val, best_move = val, (r, c)
            beta = min(beta, val)
            if beta <= alpha:
                break
        return best_val, best_move

# Game Loop 

def get_int(prompt: str, lo: int, hi: int) -> int:
    while True:
        try:
            x = int(input(prompt))
            if lo <= x <= hi:
                return x
            print(f"Enter an integer in [{lo}, {hi}]")
        except ValueError:
            print("Enter a valid integer.")

def get_move(board: List[List[str]]) -> Tuple[int,int]:
    n = len(board)
    while True:
        raw = input(f"Enter your move as 'row col' (1..{n} 1..{n}): ").strip()
        try:
            r, c = map(int, raw.split())
            r -= 1; c -= 1
            if in_bounds(n, r, c) and board[r][c] == EMPTY:
                return r, c
            print("Invalid or occupied cell. Try again.")
        except Exception:
            print("Invalid format. Try again (e.g., 2 3).")

def ai_move(board: List[List[str]], K: int, depth: int) -> Tuple[int,int]:
    # For large boards, consider a random move if the board is empty to speed up
    if len(available_moves(board)) == len(board) * len(board):
        n = len(board)
        return n//2, n//2  # start near center
    _, move = minimax(board, K, depth, -math.inf, math.inf, True)
    # Fallback (shouldn't happen)
    if move is None:
        move = random.choice(available_moves(board))
    return move

def play():
    print("=== N x N Tic-Tac-Toe (with AI) ===")
    n = get_int("Enter board size N (3..7 recommended): ", 3, 15)
    K = get_int(f"Enter win length K (3..{n}): ", 3, n)

    print("\nModes:")
    print("1) Human vs Human")
    print("2) Human vs AI")
    print("3) AI vs AI")
    mode = get_int("Choose mode (1/2/3): ", 1, 3)

    # AI search depth suggestion
    if n <= 3:
        DEPTH = 8
    elif n <= 4:
        DEPTH = 5
    elif n <= 5:
        DEPTH = 3
    else:
        DEPTH = 2
    print(f"(AI search depth set to {DEPTH} for performance.)\n")

    board = make_board(n)
    current = HUMAN  # X starts

    if mode == 2:
        first = get_int("Who starts? 1) You (X)  2) AI (O): ", 1, 2)
        current = HUMAN if first == 1 else AI

    print_board(board)

    while True:
        winner = check_winner(board, K)
        if winner or is_full(board):
            break

        if mode == 1:
            # Human vs Human
            print(f"Turn: {current}")
            r, c = get_move(board)
            board[r][c] = current
            current = AI if current == HUMAN else HUMAN

        elif mode == 2:
            if current == HUMAN:
                print("Your turn (X).")
                r, c = get_move(board)
                board[r][c] = HUMAN
                current = AI
            else:
                print("AI thinking (O)...")
                r, c = ai_move(board, K, DEPTH)
                board[r][c] = AI
                current = HUMAN

        else:  # AI vs AI
            print(f"{current} thinking...")
            if current == HUMAN:
                r, c = ai_move(board, K, DEPTH)
                board[r][c] = HUMAN
                current = AI
            else:
                r, c = ai_move(board, K, DEPTH)
                board[r][c] = AI
                current = HUMAN

        print_board(board)

    winner = check_winner(board, K)
    if winner:
        print_board(board)
        print(f"Winner: {winner}")
    else:
        print_board(board)
        print("It's a draw.")

if __name__ == "__main__":
    play()
