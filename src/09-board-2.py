# Python によるプログラミング：第 9 章　
# 例題 9.2 リストの使用
# --------------------------
# プログラム名: 09-board-2.py

from dataclasses import dataclass, field

@dataclass
class Board:
    height: int
    width: int
    mine: list = field(init=False)
    is_open: list = field(init=False)

    def __post_init__(self):
        self.mine = self.false_table()
        self.is_open = self.false_table()
    
    def false_table(self):
        cells = []
        for x in range(self.width):
            vert = []   # 縦方向のリスト
            for y in range(self.height):
                vert.append(False)
            cells.append(vert)
        return cells

board = Board(3, 3)
board.mine[1][1] = True
board.mine[2][2] = True
board.is_open[0][0] = True
board.is_open[1][2] = True
print(board.mine)
print(board.is_open)
