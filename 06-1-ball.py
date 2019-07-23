# Python によるプログラミング：第 6 章
#  例題 6.2 複数ボールのリスト化
# --------------------------
# プログラム名: 06-1-ball.py

from tkinter import *
from dataclasses import dataclass

@dataclass
class Ball:
    id: int
    x: int
    y: int
    d: int

    def redraw(self):   # 再描画
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.d, self.y + self.d)

def create_ball(x,y,d):
    id = canvas.create_oval(x, y, x + d, y + d, fill="black")
    return Ball(id, x, y, d)

tk = Tk()
canvas = Canvas( tk, width=500, height=400, bd=0 )
canvas.pack()

balls = [
    create_ball(10, 100, 20),
    create_ball(50, 150, 30),
    create_ball(90, 200, 50)
    ]

for ball in balls:
    ball.redraw()
