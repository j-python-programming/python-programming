# Python によるプログラミング：第 2 章
#    例題 2.3 ボールと壁
#  (2) 壁ではね返る
# --------------------------
# プログラム名: 02-ball-4.py

from tkinter import *
from dataclasses import dataclass
import time

# パラメータ定義は、1か所にまとめておく。
DURATION = 0.001    # sleep 時間 = 描画の間隔
X0 = 150            # ボールの X 初期値
Y0 = 150            # ボールの Y 初期値
D = 15              # ボールの直径
VX0 = 2             # ボールの移動量

@dataclass
class Ball:
    id: int
    x: int
    y: int
    vx: int
    d: int
    c: str

@dataclass
class Border:
    left: int
    right: int
    top: int
    bottom: int

# 直径 d は、省略されたら 3 に、色 c は、省略されたら "black" になる
def make_ball(x, y, vx, d=3, c="black"):
    id = canvas.create_rectangle(x, y, x + d, y + d,
                                 fill=c, outline=c)
    return Ball(id, x, y, vx, d, c)

# ボールの移動を、プログラム本体から抜き出した。
def move_ball(ball):
    ball.x = ball.x + ball.vx

# 壁を描画する関数の定義
def make_walls(ox, oy, width, height):
    canvas.create_rectangle(ox, oy, ox + width, oy + height)

# ボールを再描画する関数。coords をラップしている。
def redraw_ball(ball):
    d = ball.d
    canvas.coords(ball.id, ball.x, ball.y,
                  ball.x + d, ball.y + d)

tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0 )
canvas.pack()
tk.update()

# 壁の座標を与える。(left, right, top, bottom)
border = Border(100, 700, 100, 500)

# 初期化処理
make_walls(
    border.left,
    border.top,
    border.right - border.left,
    border.bottom - border.top
    )
ball = make_ball(X0, Y0, VX0, D)

while True:
    move_ball(ball)   # まず、ボールを移動させる
    # もし、移動後のボールの左上座標が、左の壁よりもさらに左になるか、
    # または、ボールの右端が、右の壁よりも右になるならば、
    if (ball.x + ball.vx < border.left \
        or ball.x + ball.d  >= border.right):
        ball.vx = - ball.vx    # ボールの移動方向を反転させる
    redraw_ball(ball)      # ラップした関数を呼び出して、移動
    tk.update()            # 描画が画面に反映される。
    time.sleep(DURATION)
