# Python によるプログラミング：第 9 章　
# 発展問題 9.6 終了判定と 3×3 の完成
# --------------------------
# プログラム名: ex09-mine.py

from tkinter import Tk, Canvas, CENTER, NW
from dataclasses import dataclass, field
import math
import random
import sys

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
        self.mine = self.false_table()     # 地雷の場所:リストを初期化
        self.is_open = self.false_table()  # 開いているマス：:リストを初期化
        self.unopened = self.height * self.width    # まだ開いていないマスの数
        self.exploded = False             # 爆発した！

    # Falseだけの二次元リストを作成する。
    def false_table(self):
        cells = [[False for y in range(self.height)]
                        for x in range(self.width)]
        return cells

    # ゲームの準備をする
    def setup(self, num_mines):
        canvas.bind('<Button-1>', self.on_click)  # イベントハンドラを登録
        self.set_mine(num_mines)
        self.unopened -= num_mines
        self.draw()                     # 最初の画面を表示する

    # 地雷を設定する
    def set_mine(self, num):
        num_mine = 0
        while num_mine < num:  # 指定の個数だけ地雷を生成
            i = random.randrange(self.width)   # 横方向
            j = random.randrange(self.height)  # 縦方向
            if not self.mine[i][j]:  # もし、まだ地雷が未設定なら
                self.mine[i][j] = True  # ここに地雷を設定する
                num_mine += 1  # 生成済みの地雷数を、1増やす
                print("mine = ({}, {})".format(i, j)) # 開発時の確認用

    # マス目のインデックスが有効かどうかの判定
    def is_valid(self, i, j):
        return 0 <= i < self.width and 0 <= j < self.height

    def open(self, i, j):
        self.is_open[i][j] = True   # 「開かれている」をTrueに設定
        if self.mine[i][j]:
            self.exploded = True    # 地雷を踏んだ！
        else:
            self.unopened -= 1

    # マス目を開く: on_click からのみ呼ばれる
    # マス目のインデックスの有効性は、on_click でチェック済
    def try_open(self, i, j):
        if self.is_valid(i, j):  # 有効なインデックスなら
            self.open(i, j)      # マス目を開き
            self.draw()          # 再描画する

    # 周囲のマス目を表すタプルのリストを作成する。
    def neighbors(self, i, j):
        x = [(i-1, j-1), (i, j-1), (i+1, j-1),
             (i-1, j  ),           (i+1, j  ),
             (i-1, j+1), (i, j+1), (i+1, j+1)]
        value = [v for v in x if self.is_valid(v[0], v[1])]
        return value

    # 周囲にある地雷の数を数える
    # neighboursの中で、is_validは確認済み
    def count(self, i, j):
        c = 0
        for x in self.neighbors(i, j):  # タプルを取り出す。
            if self.mine[x[0]][x[1]]: # 有効なマス目で地雷の場所がTrueなら
                c = c + 1                # カウントアップする。 
        return c

    # ===== Controller =====
    # クリックした時の処理
    def on_click(self, event):
        x, y = (event.x, event.y)
        i = math.floor((x - OFFSET_X) / CELL_SIZE) # xからインデックスiを計算
        j = math.floor((y - OFFSET_Y) / CELL_SIZE) # yからインデックスjを計算
        print(i, j)  # デバッグの際に、計算が正しく確認する方法の例
        self.try_open(i, j)

    def play(self):
        self.setup(NUM_MINES)   # ゲームを設定する
        while self.unopened > 0 and not self.exploded:
            tk.update()
        if self.exploded:       # 地雷を踏んで終了
            str = "Bang !"
        else:                   # 全部開いて終了
            str = "Cleared !"
        canvas.create_text(OFFSET_X, OFFSET_Y + CELL_SIZE * self.height + 2,
			   text=str, font=FONT, anchor=NW)
        canvas.unbind('<Button-1>')  # イベントハンドラを解放

    # ===== View =====
    # ボードの描画
    def draw(self):
        canvas.delete("all")                # 一旦クリアすす。
        for i in range(self.width):         # iは幅方向の添え字
            for j in range(self.height):    # jは、高さ方向の添え字
                text = ""
                if self.is_open[i][j]:   # マス目が開いていて
                    if self.mine[i][j]:  # 地雷だったら
                        text = "*"            # "*"
                    else:                     # 地雷でないなら
                        text = str(self.count(i, j))  # カウント数表示
                else:                         # マス目が開いていないなら
                    text = "-"                # "-"を表示
                self.draw_text(i, j, text)     # テキストの表示

    # マス目の表示(枠と文字)
    def draw_text(self, i, j, text):
        x = OFFSET_X + i * CELL_SIZE      # インデックスiからx座標を計算
        y = OFFSET_Y + j * CELL_SIZE      # インデックスjからy座標を計算
        canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE) # 枠
        canvas.create_text(x + CELL_CENTER, y + CELL_CENTER,
			   text=text, font=FONT, anchor=CENTER)

# -------------------
tk = Tk()
tk.title("Mine Sweeper")

canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

# ----------------------------------
# メインルーチン
board = Board(BOARD_WIDTH, BOARD_HEIGHT)
board.play()
sys.exit()
