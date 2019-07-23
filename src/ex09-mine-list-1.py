# Python によるプログラミング：第 9 章　
# 例題 9.3 乱数利用の地雷生成
# --------------------------
# プログラム名: 09-mine-list-1.py

from tkinter import Tk, Canvas, CENTER
from dataclasses import dataclass, field
import math
import random

# 初期設定値(定数)
OFFSET_X = 100
OFFSET_Y = 100
CELL_SIZE = 40
FONT_SIZE = 20
CELL_CENTER = CELL_SIZE / 2
BOARD_WIDTH = 3
BOARD_HEIGHT = 3
FONT = "Helvetica " + str(FONT_SIZE)

# =================================================
# ゲーム全体の盤面を管理する。
@dataclass
class Board:
    width: int
    height: int
    mine: list = field(init=False)
    is_open: list = field(init=False)

    def __post_init__(self):
        self.mine = self.false_table()
        self.is_open = self.false_table()
 
    def false_table(self):
        cells = [[False for y in range(self.height)]
                        for x in range(self.width)]
        return cells

    # 地雷を設定する
    def set_mine(self, num):
        num_mine = 0
        while num_mine < num:  # 指定の個数だけ地雷を生成
            x = random.randrange(self.width)   # 横方向
            y = random.randrange(self.height)  # 縦方向
            if not self.mine[x][y]:  # もし、まだ地雷が未設定なら
                self.mine[x][y] = True  # ここに地雷を設定する
                num_mine += 1  # 生成済みの地雷数を、1 増やす
                print("mine =", x, ",", y)     # 開発時の確認用

tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

board = Board(BOARD_WIDTH, BOARD_HEIGHT)
board.set_mine(2)
board.is_open[0][0] = True
board.is_open[1][2] = True
print(board.mine)
print(board.is_open)
