# Python によるプログラミング：第 5 章
# 練習問題 5.3　ボールクラスの導入
# --------------------------
# プログラム名: ex05-bounce.py

from tkinter import *
import time

# 定数
DURATION = 0.01

class Border:
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top= top
        self.bottom = bottom

class Ball:
    def __init__(self, id, x, y, d, dx, dy, c="black"):
        # Ballオブジェクトを生成する際に属性を定義する
        self.id = id
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.d = d
        self.c = c

    def move(self):
        # 移動する。
        self.x = self.x + self.dx
        self.y = self.y + self.dy

    def redraw(self):
        # canvas上に描画する
        canvas.coords(self.id, self.x, self.y, self.x + self.d, self.y + self.d)

def create_ball(x, y, d, dx, dy):
    id = canvas.create_rectangle(0, 0, 0, 0, fill="black")
    ball = Ball(id, x, y, d, dx, dy)
    return ball

def make_walls(ox, oy, width, height):
    canvas.create_rectangle(ox, oy, ox + width, oy + height)

tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

border = Border(100, 400, 100, 300)

make_walls(
    border.left,
    border.top,
    border.right - border.left,
    border.bottom - border.top
    )

ball = create_ball(100, 100, 10, 3, 2) #ボールオブジェクトを一個作成

# 以下メインルーチン
while True:
    ball.move()
    if (ball.x + ball.dx < border.left \
        or ball.x + ball.d >= border.right):
        ball.dx = -ball.dx
    if (ball.y + ball.dy < border.top \
        or ball.y + ball.d >= border.bottom):
        ball.dy = -ball.dy
    ball.redraw()
    tk.update()
    time.sleep(DURATION)
