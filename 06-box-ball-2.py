# Python によるプログラミング：第 6 章
#  例題 6.5 イベント処理でボールを増やす
# --------------------------
# プログラム名: 06-box-ball-2.py

from tkinter import *
from dataclasses import dataclass
import time

@dataclass
class Ball:
    id: int
    x: int
    y: int
    d: int
    vx: int

    def move(self):   # ボールを動かす
        self.x = self.x + self.vx

    def redraw(self):     # ボールの再描画
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.d, self.y + self.d)

# ゲーム環境のBox
class Box:
    def __init__(self, x, y, w, h, duration):  # コンストラクタ
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.h = h
        self.balls = []
        self.duration = duration

    def create_ball(self, x, y, d, vx):  # ボールを生成する
        id = canvas.create_oval(x, y, x + d, y + d, fill="black")
        return Ball(id, x, y, d, vx)

    def check_wall(self, ball):  # 壁との衝突確認
        if ball.x <= self.west or ball.x + ball.d >= self.east:
            ball.vx = - ball.vx

    def set_balls(self, n):  # ボールを生成してリスト化
        for x in range(n):
            ball = self.create_ball(self.west,
                                    self.north + 20 * x + 10,
                                    10, 10)
            self.balls.append(ball)

    def animate(self):
        for x in range(100): # 100回繰り返す
            for ball in self.balls:
                ball.move()    # ボールの移動
                self.check_wall(ball)  # 壁との衝突チェック
                ball.redraw()  # 再描画
            time.sleep(self.duration)
            tk.update()

    def on_press_space(self, event):
        self.balls.append(
            self.create_ball(
                self.west, (self.north + self.h)/2, 10, 10
                )
            )

tk=Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

box = Box(100, 100, 200, 200, 0.05)
canvas.bind_all("<KeyPress-space>", box.on_press_space)
box.set_balls(5)
box.animate()
