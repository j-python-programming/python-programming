# Python によるプログラミング：第 6 章
#  練習問題 6.1 Paddleクラスの実装
# --------------------------
# プログラム名: ex06-block-1.py

from tkinter import *
from dataclasses import dataclass, field
import time

# 定数定義
BOX_LEFT = 100      # ゲーム領域の左端
BOX_TOP  = 100      # ゲーム領域の上位置
BOX_WIDTH  = 300    # ゲーム領域の幅
BOX_HEIGHT = 300    # ゲーム領域の高さ

BALL_INITIAL_X = BOX_LEFT + 100  # ボールの最初のX位置
BALL_INITIAL_Y = BOX_TOP + 20    # ボールの最初のY位置
BALL_DIAMETER = 10               # ボールの直径
BALL_SPEED = 10                  # ボールのスピード

DURATION = 0.05      # アニメーションのスピード

PADDLE_WIDTH = 10     # パドルの幅
PADDLE_HEIGHT = 50    # パドルの高さ
PADDLE_START_POS = 20 # パドルの最初の位置

CANVAS_WIDTH = BOX_LEFT + BOX_WIDTH + 100   # キャンバスの大きさ
CANVAS_HEIGHT = BOX_TOP + BOX_HEIGHT + 100

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
    dy: int = field(init=False, default=0)

    def move(self):       # パドルを動かす
        self.y += self.dy

    def redraw(self):     # パドルの再描画
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.w, self.y + self.h)

@dataclass
class Box:
    id: int
    west: int
    north: int
    east: int
    south: int
    balls: list
    duration: float
    paddle: Paddle
    def __init__(self, x, y, w, h, duration):  # ゲーム領域のコンストラクタ
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.balls = []
        self.duration = duration
        self.paddle = None
        self.id = canvas.create_rectangle(x, y, x + w, y + h, fill="white")

    def create_ball(self, x, y, d, vx):  # ボールを生成し、初期描画する
        id = canvas.create_oval(x, y, x + d, y + d, fill="black")
        return Ball(id, x, y, d, vx)

    def set_balls(self, n):
        for x in range(n):
            ball = self.create_ball(BALL_INITIAL_X,
                                    BALL_INITIAL_Y + 20*x + BALL_DIAMETER,
                                    BALL_DIAMETER, BALL_SPEED )
            self.balls.append(ball)

    def create_paddle(self, x, y, w, h):
        id = canvas.create_rectangle(x, y, x + w, y + h, fill="blue")
        return Paddle(id, x, y, w, h )

    def set_paddle(self):
        self.paddle = self.create_paddle(
            self.east - PADDLE_WIDTH,
            self.north + PADDLE_START_POS,
            PADDLE_WIDTH, PADDLE_HEIGHT
            )

    def check_wall(self, ball):
        if ball.x <= self.west or ball.x + ball.d >= self.east:
            ball.vx = - ball.vx

    def animate(self):
        for x in range(100): #iterate 100 times
            for ball in self.balls:
                ball.move()
                self.check_wall(ball)
                ball.redraw()
            self.paddle.move()
            self.paddle.redraw()
            time.sleep(self.duration)
            tk.update()

#main
tk = Tk()
canvas = Canvas(tk, width=CANVAS_WIDTH,
                height=CANVAS_HEIGHT, bd=0)
canvas.pack()

box = Box(BOX_LEFT, BOX_TOP, BOX_WIDTH, BOX_HEIGHT, duration=DURATION)

box.set_balls(1)
box.set_paddle()
box.animate()
