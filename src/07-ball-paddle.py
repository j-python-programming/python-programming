# Python によるプログラミング：第 7 章
#  例題 7.1 ポリモーフィズムの応用
# --------------------------
# プログラム名: 07-ball-paddle.py

from tkinter import Tk, Canvas
from dataclasses import dataclass, field
import time

@dataclass
class Ball:
    id: int
    x: int
    y: int
    d: int
    vx: int

    def move(self):   # ボールを動かす
        self.x += self.vx

    def redraw(self):     # ボールの再描画
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.d, self.y + self.d)

@dataclass
class Paddle:
    id: int
    x: int
    y: int
    w: int
    h: int
    vy: int = field(init=False, default=0)

    def move(self):       # パドルを動かす
        self.y += self.vy

    def redraw(self):     # パドルの再描画
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.w, self.y + self.h)

    def set_v(self, v):
        self.vy = v

    def stop(self):       # パドルを止める
        self.vy = 0

@dataclass
class Box:
    id: int
    west: int
    north: int
    east: int
    south: int
    ball: Ball
    paddle: Paddle
    paddle_v: int
    duration: float

    def __init__(self, x, y, w, h, duration):  # ゲーム領域のコンストラクタ
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.ball = None
        self.paddle = None
        self.paddle_v = 2
        self.duration = duration

    def create_ball(self, x, y, d, vx):  # ボールを生成し、初期描画する
        id = canvas.create_oval(x, y, x + d, y + d, fill="black")
        return Ball(id, x, y, d, vx)

    def create_paddle(self, x, y, w, h): # パドルを初期表示し、戻す。
        id = canvas.create_rectangle(x, y, x + w, y + h, fill="blue")
        return Paddle(id, x, y, w, h)

    def check_wall(self, ball):  # ボールの壁での反射
        if ball.x <= self.west or ball.x + ball.d >= self.east:
            ball.vx = - ball.vx

    def check_paddle(self, paddle, ball):  # ボールのパドルでの反射
        center = ball.y + ball.d/2
        if center >= paddle.y and center <= paddle.y + paddle.h:
            if ball.x + ball.d >= paddle.x:
                ball.vx = - ball.vx

    def up_paddle(self, event):
        self.paddle.set_v(- self.paddle_v)

    def down_paddle(self, event):
        self.paddle.set_v(self.paddle_v)

    def stop_paddle(self, event):
        self.paddle.stop()

    def set(self):
        ball_y0 = (self.north + self.south)/2
        self.ball = self.create_ball(self.west, ball_y0, 10, 10)
        self.paddle = self.create_paddle(self.east - 20, ball_y0 - 20, 10, 40)
        canvas.bind_all("<KeyPress-Up>", self.up_paddle)
        canvas.bind_all("<KeyRelease-Up>", self.stop_paddle)
        canvas.bind_all("<KeyPress-Down>", self.down_paddle)
        canvas.bind_all("<KeyRelease-Down>", self.stop_paddle)

    def animate(self):
        movingObjs = [self.paddle, self.ball]
        while True:
            for obj in movingObjs:
                obj.move()
            self.check_wall(self.ball)
            self.check_paddle(self.paddle, self.ball)
            for obj in movingObjs:
                obj.redraw()
            time.sleep(self.duration)
            tk.update_idletasks()
            tk.update()

tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

box = Box(100, 100, 200, 200, 0.1)
box.set()
box.animate()
