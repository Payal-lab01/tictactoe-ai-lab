
from ai.engine import (
    new_board,
    make_move,
    minimax,
    alphabeta,
    best_move,
    best_move_alphabeta,
    winner,
    HUMAN,
    AI,
)

board = new_board()

# Both algorithms should evaluate the empty board as a draw.
plain_score = minimax(board, True)

pruned_score = alphabeta(
    board, True,
    float("-inf"), float("inf")
)

print("Minimax score:", plain_score)
print("Alpha-Beta score:", pruned_score)

assert plain_score == pruned_score == 0

# Both should find the immediate winning move.
board = [
    "O", "O", "",
    "X", "X", "",
    "",  "",  "",
]

move1 = best_move(board)
move2 = best_move_alphabeta(board)

print("Minimax winning move:", move1)
print("Alpha-Beta winning move:", move2)

assert move1 == 2
assert move2 == 2
assert winner(make_move(board, move2, AI)) == AI

print("All Alpha-Beta tests passed!")
