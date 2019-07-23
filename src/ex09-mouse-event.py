# Python によるプログラミング：第 9 章　
# 練習問題 9.1 マウスイベントの処理
# --------------------------
# プログラム名: ex09-mouse-event.py

from tkinter import Tk, Canvas
from dataclasses import dataclass, field
import math

OFFSET_X = 100
OFFSET_Y = 100
CELL_SIZE = 40
FONT_SIZE = 20

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

def on_click(event):
    x, y = (event.x, event.y)
    i = math.floor((x - OFFSET_X) / CELL_SIZE)
    j = math.floor((y - OFFSET_Y) / CELL_SIZE)
    print(i, j)

tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

board = Board(3, 3)
board.mine[1][1] = True
board.mine[2][2] = True
board.is_open[0][0] = True
board.is_open[1][2] = True
print(board.mine)
print(board.is_open)

canvas.bind('<Button-1>', on_click)
