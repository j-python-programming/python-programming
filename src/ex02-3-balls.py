# Python によるプログラミング：第 2 章
# 練習問題 2.3 複数のボールを動かす
# --------------------------
# プログラム名: ex02-3-balls.py

from tkinter import *
from dataclasses import dataclass
import time

# 初期値を与える
DURATION = 0.001

@dataclass
class Ball:
    id: int
    x: int
    y: int
    vx: int
    vy: int
    d: int
    c: str

@dataclass
class Border:
    left: int
    right: int
    top: int
    bottom: int

# ボールを初期位置に描画し、生成されたdataclassを返す。
def make_ball(x, y, vx, vy, d=3, c="black"):
    id = canvas.create_rectangle(x, y, x + d, y + d,
                                 fill=c, outline=c)
    return Ball(id, x, y, vx, vy, d, c)

# ボールの移動: xとyのそれぞれに変位がある。
def move_ball( ball ):
    ball.x += ball.vx
    ball.y += ball.vy

# 左上の点と、幅と高さから、枠を描画する  
def make_walls(ox, oy, width, height):
    canvas.create_rectangle(ox, oy, ox+width, oy+height)

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

# ボールの初期化
balls = [
    make_ball(100, 100, 2, 1, 20, "darkblue"),
    make_ball(200, 200, -4, 3, 25, "orange"),
    make_ball(300, 300, -2, -1, 10, "green"),
    make_ball(400, 400, 4, 2, 5, "darkgreen")
    ]

while True:
    for ball in balls:  # すべてのボールについて、処理する
        move_ball(ball)  # ボールの移動
        # X座標が、左右の壁を超えるなら、Xの移動方向を反転する
        if (ball.x + ball.vx < border.left \
            or ball.x + ball.d >= border.right):
            ball.vx = -ball.vx
        # Y座標が、上下の壁を超えるなら、Yの移動方向を反転する
        if (ball.y + ball.vy < border.top \
            or ball.y + ball.d >= border.bottom):
            ball.vy = -ball.vy
        redraw_ball(ball)      # ボール移動の描画
    # ここで、インデントの深さがfor ballと同じ点に注意
    tk.update()              # 描画が画面に反映される。
    time.sleep(DURATION)     # 次に描画するまで、sleepする。
