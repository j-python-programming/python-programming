# Python によるプログラミング：第 6 章
#  6.1 複数オブジェクトのリスト化　準備
# --------------------------
# プログラム名: 06-ex0-ball.py

from tkinter import *
from dataclasses import dataclass
import time

# 定数
DURATION = 0.01

LEFT, RIGHT, TOP, BOTTOM = (100, 400, 100, 300)

@dataclass
class Ball:
    id: int
    x: int
    y: int
    d: int
    dx: int
    dy: int
    c: str = "black"

    def move(self):                         # 移動する。
        self.x += self.dx
        self.y += self.dy

    def redraw(self):                       # Canvas上に描画する。
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.d, self.y + self.d)

def create_ball(x, y, d, dx, dy):  # ボールを生成する
    id = canvas.create_rectangle(0, 0, 0, 0, fill="black")
    ball = Ball(id, x, y, d, dx, dy)
    return ball

def make_walls(ox, oy, width, height):
    canvas.create_rectangle(ox, oy, ox + width, oy + height)

def check_wall(ball):   # 壁で跳ね返る
    if (ball.x + ball.dx < LEFT \
        or ball.x + ball.d >= RIGHT):
        ball.dx = -ball.dx
    if (ball.y + ball.dy < TOP
        or ball.y + ball.d >= BOTTOM):
        ball.dy = -ball.dy

def animate(ball):
    while True:
        ball.move()
        check_wall(ball)
        ball.redraw()
        tk.update()
        time.sleep(DURATION)

# 描画の準備
tk=Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

# 初期化
make_walls(LEFT, TOP, RIGHT - LEFT, BOTTOM - TOP)

ball = create_ball(100, 100, 10, 3, 2)

# メインプログラム
animate(ball)
