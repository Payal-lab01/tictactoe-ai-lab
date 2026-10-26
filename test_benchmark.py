
import time

from ai.engine import (
    new_board,
    minimax,
    alphabeta,
)

board = new_board()

# Benchmark ordinary Minimax
minimax_stats = {"nodes": 0}
start = time.perf_counter()

minimax_score = minimax(
    board, True, stats=minimax_stats
)

minimax_time = (time.perf_counter() - start) * 1000

# Benchmark Alpha-Beta Pruning
alphabeta_stats = {"nodes": 0}
start = time.perf_counter()

alphabeta_score = alphabeta(
    board,
    True,
    float("-inf"),
    float("inf"),
    stats=alphabeta_stats,
)

alphabeta_time = (time.perf_counter() - start) * 1000

# Print the comparison
print("\n--- AI Algorithm Performance ---")
print(
    f"Minimax: {minimax_stats['nodes']} nodes, "
    f"{minimax_time:.3f} ms"
)
print(
    f"Alpha-Beta: {alphabeta_stats['nodes']} nodes, "
    f"{alphabeta_time:.3f} ms"
)

print("Minimax score:", minimax_score)
print("Alpha-Beta score:", alphabeta_score)

assert minimax_score == alphabeta_score

reduction = (
    1 - alphabeta_stats["nodes"] / minimax_stats["nodes"]
) * 100

print(f"Node reduction: {reduction:.2f}%")
