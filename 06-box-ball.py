# Python によるプログラミング：第 6 章
# 例題 6.4 箱の中のボール
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
    vx: int

    def move(self):
        self.x += self.vx

    def redraw(self):
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.d, self.y + self.d)

class Box:
    def __init__(self, x, y, w, h, duration):
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.balls = []
        self.duration = duration

    def create_ball(self, x, y, d, vx):
        id = canvas.create_oval(x, y, x + d, y + d, fill="black")
        return Ball(id, x, y, d, vx)

    def check_wall(self, ball):
        if ball.x <= self.west or ball.x + ball.d >= self.east:
            ball.vx = -ball.vx

    def set_balls(self, n):
        for x in range(n):
            ball = self.create_ball(self.west,
                                    self.north + 20 * x + 10,
                                    10, 10)
            self.balls.append(ball)

    def animate(self):
        for x in range(100): #iterate 50 times
            for ball in self.balls:
                ball.move()
                self.check_wall(ball)
                ball.redraw()
            time.sleep(self.duration)
            tk.update()

tk=Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

box = Box(0, 0, 400, 400, 0.05)
box.set_balls(5)
box.animate()
