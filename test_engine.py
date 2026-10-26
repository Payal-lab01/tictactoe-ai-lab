
from ai.engine import (
    new_board,
    make_move,
    winner,
    is_draw,
    available_moves,
    HUMAN,
)

board = new_board()

board = make_move(board, 0, HUMAN)
board = make_move(board, 1, HUMAN)
board = make_move(board, 2, HUMAN)

print("Board:", board)
print("Winner:", winner(board))
print("Empty cells:", len(available_moves(board)))
print("Is draw:", is_draw(board))

assert winner(board) == HUMAN
assert len(available_moves(board)) == 6

print("All basic tests passed!")

