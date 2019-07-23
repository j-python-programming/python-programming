# Python によるプログラミング：第 9 章　
# 練習問題 9.5 マウスイベントの実装
# --------------------------
# プログラム名: ex09-mine-list-3.py

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
NUM_MINES = 2

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

    # Falseだけの二次元リストを作成する。
    def false_list(self):
        cells = [[False for y in range(self.height)]
                        for x in range(self.width)]
        return cells

    # ゲームの準備をする
    def setup(self, num_mines):
        canvas.bind('<Button-1>', self.on_click)  # イベントハンドラを登録
        self.set_mine(num_mines)

    # 地雷を設定する
    def set_mine(self, num):
        num_mine = 0
        print(self.mine)
        while num_mine < num:  # 指定の個数だけ地雷を生成
            i = random.randrange(self.width)   # 横方向
            j = random.randrange(self.height)  # 縦方向
            print("i, j=", i, ",", j)
            if not self.mine[i][j]:  # もし、まだ地雷が未設定なら
                self.mine[i][j] = True  # ここに地雷を設定する
                num_mine += 1  # 生成済みの地雷数を、1増やす
                print("mine =", i, ",", j)     # 開発時の確認用

    # マス目のインデックスが有効かどうかの判定
    def is_valid(self, i, j):
        return 0 <= i < self.width and 0 <= j < self.height

    # マス目を開く
    def open(self, i, j):
        if self.is_valid(i, j):    # マス目のインデックスが有効なら
            self.is_open[i][j] = True   # 「開かれている」をTrueに設定

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
            if self.mine[x[0]][x[1]]: # 有効なマス目で地雷の場所がTrueなら
                c = c + 1                # カウントアップする。 
        return c

    # ボードの描画
    def draw(self):
        canvas.delete("all")                  # 一旦クリアすす。
        for i in range(self.width):          # xは幅方向の添え字
            for j in range(self.height):     # yは、高さ方向の添え字
                text = ""
                if self.is_open[i][j]:  # マス目が開いていて
                    if self.mine[i][j]:  # マス目が開いていて
                        text = "*"            # "*"
                    else:                     # 地雷でないなら
                        text = str(self.count(i,j))  # カウント数表示
                else:                         # マス目が開いていないなら
                    text = "-"                # "-"を表示
                self.draw_text(i, j, text)     # テキストの表示

    # マス目の表示(枠と文字)
    def draw_text(self, i, j, str):
        x = OFFSET_X + i * CELL_SIZE      # インデックスjからx座標を計算
        y = OFFSET_Y + j * CELL_SIZE      # インデックスiからy座標を計算
        canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE) # 枠
        canvas.create_text(x + CELL_CENTER, y + CELL_CENTER,
			   text=str, font=FONT, anchor=CENTER)

    # クリックした時の処理
    def on_click(self, event):
        x, y = (event.x, event.y)
        i = math.floor((x - OFFSET_X) / CELL_SIZE) # xからインデックスjを計算
        j = math.floor((y - OFFSET_Y) / CELL_SIZE) # yからインデックスiを計算
        print(i, j)  # デバッグの際に、計算が正しく確認する方法の例
        if self.is_valid(i, j):  # 有効なインデックスなら
            self.open(i, j)      # マス目を開き
            self.draw()     # 再描画する

# ----------------------------------
# メインルーチン
tk = Tk()
tk.title("Mine Sweeper")

canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

board = Board(BOARD_WIDTH, BOARD_HEIGHT)
board.setup(NUM_MINES)
board.draw()
