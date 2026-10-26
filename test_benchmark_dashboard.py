
from ai.benchmark import run_benchmark

results = run_benchmark()

for algorithm, metrics in results.items():
    print(f"\n{algorithm}")
    print(f"Score: {metrics['score']}")
    print(f"Nodes explored: {metrics['nodes']}")
    print(f"Execution time: {metrics['time_ms']:.3f} ms")

minimax_nodes = results["Minimax"]["nodes"]
alphabeta_nodes = results["Alpha-Beta"]["nodes"]

if minimax_nodes:
    reduction = (1 - alphabeta_nodes / minimax_nodes) * 100
    print(f"\nNode reduction: {reduction:.2f}%")
