# Python によるプログラミング：第 9 章　
# 練習問題 9.2  3x3 のコントローラ
# --------------------------
# プログラム名: ex09-mine-set.py

from tkinter import Tk, Canvas, CENTER
from dataclasses import dataclass, field
import math

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
    # 地雷の場所：空の集合を用意
    mine: set=field(default_factory=set)
    # 開いているマス：空の集合　
    is_open: set=field(default_factory=set)

    # マス目のインデックスが有効かどうかの判定
    def is_valid(self, i, j):
        return 0 <= i < self.width and 0 <= j < self.height

    # マス目を開く
    def open(self, i, j):
        if self.is_valid(i, j):     # マス目のインデックスが有効なら
            loc = (i, j)            # タプルを生成して、
            self.is_open.add(loc)   # 「開いているマス」の集合に追加

    # 周囲のマス目を表すタプルのリストを作成する。
    def neighbours(self, i, j):
        x = [(i-1, j-1), (i-1, j), (i-1, j+1), 
             (i,   j-1),           (i,   j+1), 
             (i+1, j-1), (i+1, j), (i+1, j+1)]
        return x

    # 周囲にある地雷の数を数える
    def count(self, i, j):
        c = 0
        for x in self.neighbours(i, j):   # 周囲のマス目のリストから
            if x in self.mine:            # 取り出したインデックスのタプルが
                 c = c + 1                # 地雷の集合に含まれていたら、加算
        return c

# ボードの描画
def draw_board(board):
    canvas.delete("all")                  # 一旦クリアすす。
    for i in range(board.width):          # xは幅方向の添え字
        for j in range(board.height):     # yは、高さ方向の添え字
            text = ""
            if (i, j) in board.is_open:   # マス目が開いていて
                if (i, j) in board.mine:  # 地雷だったら
                    text = "*"            # "*"
                else:                     # 地雷でないなら
                    text = str(board.count(i,j))  # カウント数表示
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

# クリックした時の処理
def on_click(event):
    x, y = (event.x, event.y)
    i = math.floor((x - OFFSET_X) / CELL_SIZE) # xからインデックスjを計算
    j = math.floor((y - OFFSET_Y) / CELL_SIZE) # yからインデックスiを計算
    print(i, j)  # デバッグの際に、計算が正しく確認する方法の例
    if board.is_valid(i, j):  # 有効なインデックスなら
        board.open(i, j)      # マス目を開き
        draw_board(board)     # 再描画する

# --------------------------
tk=Tk()
tk.title("Mine Sweeper")
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

canvas.bind('<Button-1>', on_click)  # イベントハンドラを登録

# ----------------------------------
# メインルーチン
board = Board(BOARD_WIDTH, BOARD_HEIGHT)
board.mine.add((1, 1))
board.mine.add((2, 2))
draw_board(board)
