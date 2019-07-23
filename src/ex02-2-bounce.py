# Python によるプログラミング：第 2 章　
# 練習問題 2.2 二次元的にボールを動かす
# --------------------------
# プログラム名: ex02-2-bounce.py

from tkinter import *
from dataclasses import dataclass
import time

DURATION = 0.001    # sleep 時間 = 描画の間隔

@dataclass
class Ball:
    id: int
    x: int
    y: int
    d: int
    vx: int
    vy: int
    c: str

@dataclass
class Border:
    left: int
    right: int
    top: int
    bottom: int

# ボールを初期位置に描画し、生成されたdataclassを返す。
def make_ball(x, y, d, vx, vy, c="black"):
    id = canvas.create_rectangle(x, y, x + d, y + d,
                            fill=c, outline=c)
    return Ball(id, x, y, d, vx, vy, c)

# ボールの移動: xとyのそれぞれに変位がある。
def move_ball(ball):
    ball.x += ball.vx
    ball.y += ball.vy

# 左上の点と、幅と高さから、枠を描画する  
def make_walls(ox, oy, width, height):
    canvas.create_rectangle(ox, oy, ox + width, oy + height)

# ボール(パッド)の再描画 
def redraw_ball(ball):
    canvas.coords(ball.id, ball.x, ball.y,
                ball.x + ball.d, ball.y + ball.d)

tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()
tk.update()

# 壁の座標を与える。(left, right, top, bottom)
border = Border(100, 700, 100, 500)

make_walls(
    border.left,
    border.top,
    border.right - border.left,
    border.bottom - border.top
    )

ball = make_ball(100, 100, 60, 20, 10, "darkblue")  # ボールの初期化

while True:
    move_ball(ball)
    # X座標が、左右の壁を超えるなら、Xの移動方向を反転する
    if (ball.x + ball.vx < border.left \
        or ball.x + ball.d >= border.right):
        ball.vx = -ball.vx
    # Y座標が、上下の壁を超えるなら、Yの移動方向を反転する
    if (ball.y + ball.vy < border.top \
        or ball.y + ball.d >= border.bottom):
        ball.vy = -ball.vy
    redraw_ball(ball)        # ボール移動の描画
    tk.update()              # 描画が画面に反映される。
    time.sleep(DURATION)     # 次に描画するまで、sleepする。
