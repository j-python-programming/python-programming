# Python によるプログラミング：第 11 章
# 練習問題 11.2 深さ優先自動探索
# --------------------------
# プログラム名: ex11-depth.py

from tkinter import Tk, Canvas
from dataclasses import dataclass, field
import math
import random

from p10flag import Flag

# =================================================
# 初期設定値(定数)
OFFSET_X = 50
OFFSET_Y = 50
CELL_SIZE = 30
FONT_SIZE = 20

BOARD_WIDTH = 8
BOARD_HEIGHT = 5
NUM_MINES = 2

BOARD_RIGHT = 2 * OFFSET_X + CELL_SIZE * BOARD_WIDTH
BOARD_BOTTOM = 2 * OFFSET_Y + CELL_SIZE * BOARD_HEIGHT

FONT = "Helvetica " + str(FONT_SIZE)

# -------------------
# ゲーム全体の盤面を管理する。
@dataclass
class Board:
    canvas: Canvas
    width: int
    height: int
    cell_size: int
    offset_x: int
    offset_y: int
    font: str
    mine: set = field(init=False, default_factory=set)
    flag: Flag = field(init = False)

    def __post_init__(self):
        self.flag = Flag(self.canvas, self.width, self.height,
                         self.cell_size, self.offset_x, self.offset_y,
                         self.font)
        for i in range(self.width):
            for j in range(self.height):
                self.flag.draw(i, j)

    # ゲームの準備をする
    def setup(self, num_mines):
        # イベントハンドラを登録
        canvas.bind('<Button-1>', self.on_click_left)
        canvas.bind('<Button-2>', self.on_click_right)
        self.set_mine(num_mines)

    # 地雷を設定する
    def set_mine(self, num):
        num_mine = 0
        while num_mine < num:  # 指定の個数だけ地雷を生成
            i = random.randrange(self.width)   # 横方向
            j = random.randrange(self.height)  # 縦方向
            if not (i, j) in self.mine: # もし、まだ地雷が未設定なら
                self.mine.add((i, j))   # ここに地雷を設定する
                num_mine += 1  # 生成済みの地雷数を、1増やす
                print("mine =", i, ",", j)     # 開発時の確認用

    # マス目のインデックスが有効かどうかの判定
    def is_valid(self, i, j):
        return 0 <= i < self.width and 0 <= j < self.height

    # マス目を開く
    def open(self, i, j):
        if self.is_valid(i, j):       # マス目のインデックスが有効なら
            if (i, j) in self.mine:   # 地雷なら
                text = "*"            # "*"
            else:                     # 地雷でないなら
                text = str(self.count(i, j))  # カウント数表示
            self.flag.open(i, j) # マス目を開く
            self.flag.draw(i, j, text)  # 再描画する

    # 周囲のマス目を表すタプルのリストを作成する。
    def neighbours(self, i, j):
        x = [(i-1, j-1), (i-1, j), (i-1, j+1), 
             (i,   j-1),           (i,   j+1), 
             (i+1, j-1), (i+1, j), (i+1, j+1)]
        value = [v for v in x if self.is_valid(v[0], v[1])]
        return value

    # 深さ優先で、周囲を探索する
    # is_validのチェックは、openやneighboursで行なっている。
    def depth_open(self, i, j):
        s = [(i, j)]   # 連鎖的に開けるマス= [(i, j)]
        while s != []:  # while 「連鎖的に開けるマス」が空でない:
            (top_i, top_j) = s.pop()   # スタックの先頭を取り出す。
            # print("(", top_i, ",", top_j,") popped.")
            # 先頭(i', j') に隣接する各マス X について:
            for (xi, xj) in self.neighbours(top_i, top_j):
                if not self.flag.is_open(xi, xj): # X が開いていない、ならば:
                    self.open(xi, xj)  # マス X を開く
                    if self.count(xi, xj)==0:  # X のマスの数字が0 ならば:
                        # 「連鎖的に開けるマス」の最後尾にX を積む
                        s.append((xi, xj))
                        # print("Pushed: (", xi, ",", xj, ")")

    # 周囲にある地雷の数を数える
    def count(self, i, j):
        c = 0
        for x in self.neighbours(i, j):  # タプルを取り出す。
            if x in self.mine:           # もし地雷なら
                c = c + 1                # カウントアップする。 
        return c

    # 画面の座標(x, y)からインデックス(i, j)を求める
    def get_index(self, x, y):
        i = math.floor((x - OFFSET_X) / CELL_SIZE) # xからインデックスjを計算
        j = math.floor((y - OFFSET_Y) / CELL_SIZE) # yからインデックスiを計算
        return (i, j)

    # 右クリックした時の処理
    def on_click_right(self, event):
        (i, j) = self.get_index(event.x, event.y)
        if self.is_valid(i, j):  # 有効なインデックスなら
            if not self.flag.is_open(i, j):  # まだ開いていないなら
                self.flag.update(i, j)   # フラグの状態を変える
                self.flag.draw(i, j)     # 再描画する

    # 左クリックした時の処理
    def on_click_left(self, event):
        (i, j) = self.get_index(event.x, event.y)
        if self.is_valid(i, j):  # 有効なインデックスなら
            if not self.flag.is_open(i, j):  # まだ開いていないなら
                self.open(i, j)  # マス目を開き
                if self.count(i, j)==0:  # もし、ゼロなら連鎖的に周囲を開く
                    self.depth_open(i, j)

# -------------------
tk = Tk()
tk.title("Mine Sweeper")

canvas = Canvas(tk, width=BOARD_RIGHT, height=BOARD_BOTTOM, bd=0)
canvas.pack()
# ----------------------------------
# メインルーチン
board = Board(canvas, BOARD_WIDTH, BOARD_HEIGHT,
              CELL_SIZE, OFFSET_X, OFFSET_Y, FONT)
board.setup(NUM_MINES)
