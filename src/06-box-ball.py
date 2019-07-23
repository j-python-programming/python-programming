# Python によるプログラミング：第 6 章
# 例題 6.3 箱の中のボール
# --------------------------
# プログラム名: 06-box-ball.py

from tkinter import *
from dataclasses import dataclass
import time

@dataclass
class Ball:
    id: int
    x: int
    y: int
    d: int
    dx: int
    dy: int
    c: str = "black"

    def move(self):   # ボールを動かす
        self.x += self.dx
        self.y += self.dy

    def redraw(self):     # ボールの再描画
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.d, self.y + self.d)

# ゲーム環境のBox
class Box:
    def __init__(self, x, y, w, h, duration):  # コンストラクタ
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.balls = []
        self.duration = duration

    def create_ball(self, x, y, d, dx, dy):  # ボールを生成する
        id = canvas.create_oval(x, y, x + d, y + d, fill="black")
        return Ball(id, x, y, d, dx, dy)

    def make_walls(self):
        canvas.create_rectangle(self.west, self.north,
                                self.east, self.south)

    def check_wall(self, ball):  # 壁との衝突確認
        if ball.x <= self.west or ball.x + ball.d >= self.east:
            ball.dx = -ball.dx
        if ball.y + ball.dy < self.north \
           or ball.y + ball.d >= self.south:
            ball.dy = -ball.dy

    def set_balls(self, n):  # ボールを生成してリスト化
        for x in range(n):
            ball = self.create_ball(self.west + 10*x,
                                    self.north + 20*x + 10,
                                    2*x + 10, 10, 10)
            self.balls.append(ball)

    def animate(self):
        while True:
            for ball in self.balls:
                ball.move()    # ボールの移動
                self.check_wall(ball)  # 壁との衝突チェック
                ball.redraw()  # 再描画
            time.sleep(self.duration)
            tk.update()

# 描画の準備
tk=Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

# メインプログラム
box = Box(100, 100, 300, 200, 0.05)
box.make_walls()
box.set_balls(5)
box.animate()
