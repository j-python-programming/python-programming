# Python によるプログラミング：第 9 章　
# 練習問題 9.4 隣接する地雷数の計算
# --------------------------
# プログラム名: 09-mine-list-2.py

from tkinter import Tk, Canvas, CENTER
from dataclasses import dataclass, field
import math
import random

# =================================================
# 初期設定値(定数)
OFFSET_X = 100
OFFSET_Y = 100
CELL_SIZE = 40
FONT_SIZE = 20
CELL_CENTER = CELL_SIZE/2
BOARD_WIDTH = 3
BOARD_HEIGHT = 3
NUM_MINE = 2
FONT = "Helvetica " + str(FONT_SIZE)

# -------------------
# ゲーム全体の盤面を管理する。
@dataclass
class Board:
    width: int
    height: int
    mine: list = field(init=False)
    is_open: list = field(init=False)

    def __post_init__(self):
        self.mine = self.false_list()
        self.is_open = self.false_list()
 
    def false_list(self):
        cells = [[False for y in range(self.height)]
                        for x in range(self.width)]
        return cells

    def is_valid(self, i, j):
        return 0 <= i < self.width and 0 <= j < self.height

    # マス目を開く
    def open(self, i, j):
        if self.is_valid(i, j):     # マス目のインデックスが有効なら
            self.is_open[i][j] = True
            print(i, j, "is opened.")

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

    # 周囲のマス目を表すタプルのリストを作成する。
    def neighbours(self, i, j):
        x = [(i-1, j-1), (i-1, j), (i-1, j+1), 
             (i,   j-1),           (i,   j+1), 
             (i+1, j-1), (i+1, j), (i+1, j+1)]
        value = [v for v in x if self.is_valid(v[0], v[1])]
        return value

    # 周囲にある地雷の数を数える
    def count(self, i, j):
        c = 0
        for x in self.neighbours(i, j):  # タプルを取り出す。
            # 有効なマス目で地雷の場所が True なら
            if (self.is_valid(x[0], x[1])
                and self.mine[x[0]][x[1]]):
                c = c + 1                # カウントアップする。 
        return c

# ボードの描画
def draw_board(board):
    canvas.delete("all")                  # 一旦クリアすす。
    for i in range(board.width):          # x は幅方向の添え字
        for j in range(board.height):     # y は、高さ方向の添え字
            text = ""
            if board.is_open[i][j]:  # マス目が開いていて
                if board.mine[i][j]:  # マス目が開いていて
                    text = "*"            # "*"
                else:                     # 地雷でないなら
                    text = str(board.count(i, j))  # カウント数表示
            else:                         # マス目が開いていないなら
                text = "-"                # "-"を表示
            draw_text(i, j, text)     # テキストの表示

# マス目の表示(枠と文字)
def draw_text(i, j, str):
    x = OFFSET_X + i * CELL_SIZE      # インデックスjからx座標を計算
    y = OFFSET_Y + j * CELL_SIZE      # インデックスiからy座標を計算
    canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE) # 枠
    canvas.create_text(x + CELL_CENTER, y + CELL_CENTER,
		       text=str, font=FONT, anchor=CENTER)

def on_click(event):
    x, y = (event.x, event.y)
    i = math.floor((x - OFFSET_X) / CELL_SIZE)
    j = math.floor((y - OFFSET_Y) / CELL_SIZE)
    print(i, j)
    if board.is_valid(i, j):
        board.open(i, j)
        draw_board(board)

# ---------------
tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

board = Board(BOARD_WIDTH, BOARD_HEIGHT)
board.set_mine(NUM_MINE)
board.is_open[0][0] = True
board.is_open[1][2] = True
print(board.mine)
print(board.is_open)
draw_board(board)

canvas.bind('<Button-1>', on_click)
