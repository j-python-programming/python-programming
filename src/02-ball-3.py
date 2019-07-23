# Python によるプログラミング：第 2 章
#    例題 2.3 ボールと壁
#  (1) アニメーション
# --------------------------
# プログラム名: 02-ball-3.py

from tkinter import *
from dataclasses import dataclass
import time

DURATION= 0.001    # sleep 時間 = 描画の間隔
X = 0              # ボールの X 初期値
Y = 100            # ボールの Y 初期値
D = 10             # ボールの直径

@dataclass
class Ball:
    id: int
    x: int
    y: int
    d: int
    c: str

# 直径 d は、省略されたら 3 に、色 c は、省略されたら "black" になる
def make_ball(x, y, d=3, c="black"):
    id = canvas.create_rectangle(x, y, x + d, y + d,
                                 fill=c, outline=c)
    return Ball(id, x, y, d, c)

# ボールを再描画する関数。coords をラップしている。
def redraw_ball(ball):
    d = ball.d
    canvas.coords(ball.id, ball.x, ball.y,
                  ball.x + d, ball.y + d)

tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()
tk.update()

ball = make_ball(X, Y, D, "darkblue") # 実際のボールを作成

for p in range(0, 600, 2):   # 媒介変数 p を変化させる
    ball.x = p               # ボールの X 座標に、p を代入
    redraw_ball(ball)        # ラップした関数を呼び出して、移動
    tk.update()              # 描画が画面に反映される。
    time.sleep(DURATION)
