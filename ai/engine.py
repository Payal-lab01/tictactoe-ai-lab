
# Tic-Tac-Toe: Basic Game Engine

EMPTY = ""
HUMAN = "X"
AI = "O"

# All 8 possible winning combinations
WIN_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def new_board():
    """Create an empty board with 9 cells."""
    return [EMPTY] * 9


def available_moves(board):
    """Return the indexes of all empty cells."""
    return [
        index
        for index, cell in enumerate(board)
        if cell == EMPTY
    ]


def make_move(board, index, mark):
    """Place X or O on a copy of the board."""
    updated_board = board.copy()
    updated_board[index] = mark
    return updated_board


def winner(board):
    """Return the winning symbol, or None if nobody has won."""
    for a, b, c in WIN_LINES:
        if (
            board[a] != EMPTY
            and board[a] == board[b] == board[c]
        ):
            return board[a]

    return None


def is_draw(board):
    """Check whether the board is full and nobody has won."""
    return (
        winner(board) is None
        and len(available_moves(board)) == 0
    )



def minimax(board, is_maximizing, depth=0, stats=None):
    """Minimax with optional search-node counting."""

    if stats is not None:
        stats["nodes"] += 1

    result = winner(board)

    if result == AI:
        return 10 - depth

    if result == HUMAN:
        return depth - 10

    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = float("-inf")

        for move in available_moves(board):
            next_board = make_move(board, move, AI)
            score = minimax(
                next_board, False, depth + 1, stats
            )
            best_score = max(best_score, score)

        return best_score

    best_score = float("inf")

    for move in available_moves(board):
        next_board = make_move(board, move, HUMAN)
        score = minimax(
            next_board, True, depth + 1, stats
        )
        best_score = min(best_score, score)

    return best_score



def best_move(board):
    """Find the best move for the AI (O)."""

    best_score = float("-inf")
    chosen_move = None

    for move in available_moves(board):
        # Simulate placing O in this position
        next_board = make_move(board, move, AI)

        # Predict the outcome with Minimax
        score = minimax(next_board, False, 1)

        # Keep the move with the highest score
        if score > best_score:
            best_score = score
            chosen_move = move

    return chosen_move


def alphabeta(
    board, is_maximizing, alpha, beta, depth=0, stats=None
):
    """Minimax with Alpha-Beta Pruning and node counting."""

    if stats is not None:
        stats["nodes"] += 1

    result = winner(board)

    if result == AI:
        return 10 - depth

    if result == HUMAN:
        return depth - 10

    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = float("-inf")

        for move in available_moves(board):
            next_board = make_move(board, move, AI)
            score = alphabeta(
                next_board, False, alpha, beta, depth + 1, stats
            )

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if alpha >= beta:
                break

        return best_score

    best_score = float("inf")

    for move in available_moves(board):
        next_board = make_move(board, move, HUMAN)
        score = alphabeta(
            next_board, True, alpha, beta, depth + 1, stats
        )

        best_score = min(best_score, score)
        beta = min(beta, best_score)

        if alpha >= beta:
            break

    return best_score


def best_move_alphabeta(board):
    """Choose the best AI move using Alpha-Beta Pruning."""

    best_score = float("-inf")
    chosen_move = None
    alpha = float("-inf")
    beta = float("inf")

    for move in available_moves(board):
        next_board = make_move(board, move, AI)

        score = alphabeta(
            next_board,
            False,
            alpha,
            beta,
            depth=1
        )

        if score > best_score:
            best_score = score
            chosen_move = move

        alpha = max(alpha, best_score)

    return chosen_move


def evaluate_position(board):
    """Estimate how favorable a non-terminal board is for O."""
    score = 0

    for a, b, c in WIN_LINES:
        line = [board[a], board[b], board[c]]
        ai_count = line.count(AI)
        human_count = line.count(HUMAN)

        # Reward lines that O can potentially complete
        if human_count == 0:
            if ai_count == 1:
                score += 2
            elif ai_count == 2:
                score += 10

        # Penalize lines that X can potentially complete
        if ai_count == 0:
            if human_count == 1:
                score -= 2
            elif human_count == 2:
                score -= 10

    # The center belongs to two diagonal/row/column combinations
    if board[4] == AI:
        score += 3
    elif board[4] == HUMAN:
        score -= 3

    return score


def minimax_limited(board, is_maximizing, depth, max_depth):
    """Minimax with a cutoff and heuristic evaluation."""
    result = winner(board)

    if result == AI:
        return 10 - depth

    if result == HUMAN:
        return depth - 10

    if is_draw(board):
        return 0

    # Stop exploring when the depth limit is reached
    if depth >= max_depth:
        return evaluate_position(board)

    if is_maximizing:
        best_score = float("-inf")

        for move in available_moves(board):
            next_board = make_move(board, move, AI)
            score = minimax_limited(
                next_board, False, depth + 1, max_depth
            )
            best_score = max(best_score, score)

        return best_score

    best_score = float("inf")

    for move in available_moves(board):
        next_board = make_move(board, move, HUMAN)
        score = minimax_limited(
            next_board, True, depth + 1, max_depth
        )
        best_score = min(best_score, score)

    return best_score


def medium_move(board):
    """Choose an AI move with limited lookahead."""
    best_score = float("-inf")
    chosen_move = None

    for move in available_moves(board):
        next_board = make_move(board, move, AI)

        # Search a total of three plies, including this AI move
        score = minimax_limited(
            next_board, False, depth=1, max_depth=3
        )

        if score > best_score:
            best_score = score
            chosen_move = move

    return chosen_move


def explain_move(board, move):
    """Explain the strategic reason for a chosen AI move."""

    if move is None:
        return "No legal moves remain."

    # Check whether this move wins immediately.
    winning_board = make_move(board, move, AI)

    if winner(winning_board) == AI:
        return "I chose this cell because it gives me an immediate win!"

    # Check whether the human could win in this cell.
    blocking_board = make_move(board, move, HUMAN)

    if winner(blocking_board) == HUMAN:
        return "I chose this cell to block your immediate winning move."

    if move == 4:
        return "I chose the center because it offers strong strategic control."

    corners = {0, 2, 6, 8}

    if move in corners:
        return "I chose a corner because it can create useful future winning opportunities."

    return "I evaluated the available moves and chose this position based on the search algorithm."
