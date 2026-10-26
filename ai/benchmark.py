
import time

from ai.engine import minimax, alphabeta, new_board


def run_benchmark():
    board = new_board()
    results = {}

    # Standard Minimax
    minimax_stats = {"nodes": 0}
    start = time.perf_counter()

    minimax_score = minimax(
        board, is_maximizing=True, stats=minimax_stats
    )

    minimax_time = (time.perf_counter() - start) * 1000

    # Minimax with Alpha-Beta Pruning
    alphabeta_stats = {"nodes": 0}
    start = time.perf_counter()

    alphabeta_score = alphabeta(
        board,
        is_maximizing=True,
        alpha=float("-inf"),
        beta=float("inf"),
        stats=alphabeta_stats,
    )

    alphabeta_time = (time.perf_counter() - start) * 1000

    results["Minimax"] = {
        "score": minimax_score,
        "nodes": minimax_stats["nodes"],
        "time_ms": minimax_time,
    }

    results["Alpha-Beta"] = {
        "score": alphabeta_score,
        "nodes": alphabeta_stats["nodes"],
        "time_ms": alphabeta_time,
    }

    return results

