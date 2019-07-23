# Python によるプログラミング：第 7 章
#  例題 7.2 MovingObject クラス
# --------------------------
# プログラム名: 07-moving-obj.py

from tkinter import Tk, Canvas
from dataclasses import dataclass
import time

class CustomCanvas(Canvas):
    def __init__(self, width=300, height=300, bg="white"):
        super().__init__(tk, width=width, height=height, bg=bg)
        self.pack()

@dataclass
class MovingObject:
    id: int
    x: int
    y: int
    w: int
    h: int
    vx: int
    vy: int

    def redraw(self):
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.w, self.y + self.h)

    def move(self):
        pass

class Ball(MovingObject):
    def __init__(self, id, x, y, d, vx):
        MovingObject.__init__(self, id, x, y, d, d, vx, 0)
        # super().__init(id, x, y, d, d, vx, 0)  も可能
        self.d = d

    def move(self):
        self.x += self.vx

class Paddle(MovingObject):
    def __init__(self, id, x, y, w, h):
        MovingObject.__init__(self, id, x, y, w, h, 0, 0)
        # super().__init__(id, x, y, w, h, 0, 0) も可能

    def move(self):
        self.y += self.vy

    def set_v(self, v):
        self.vy = v

    def stop(self):
        self.vy = 0

tk = Tk()
canvas = CustomCanvas()
