# Python によるプログラミング：第 9 章
# 例題 9.1 マスと状態の表示
# --------------------------
# プログラム名: 09-board-1.py

from dataclasses import dataclass, field

@dataclass
class Board:
    height: int
    width: int
    mine: set=field(default_factory=set)
    is_open: set=field(default_factory=set)

board = Board(3, 3)
board.mine.add((1, 1))
board.mine.add((2, 2))
board.is_open.add((0, 0))
board.is_open.add((1, 2))
print(board.mine)
print(board.is_open)
