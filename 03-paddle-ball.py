# Python によるプログラミング：第 3 章
#    例題 3.3 パドルの色を変え、ボールを跳ね返す
# --------------------------
# プログラム名: 03-paddle-ball.py

from tkinter import *
from dataclasses import dataclass
import time
import random

# 初期状態の設定
DURATION = 0.01    # 描画間隔 ( 秒 )
PADDLE_X0 = 750    # パドルの初期位置(x)
PADDLE_Y0 = 200    # パドルの初期位置(y)
BALL_Y0 = PADDLE_Y0 + 20 # ボールの初期位置(y)

PAD_VY = 2         # パドルの速度
BALL_VX = 5        # ボールの速度

# 変える色を用意する。
COLORS = ["blue", "red", "green", "yellow", "brown", "gray"]

@dataclass
class Ball:
    id: int
    x: int
    y: int
    vx: int
    d: int
    c: str

@dataclass
class Paddle:
    id: int
    x: int
    y: int
    w: int
    h: int
    vy: int
    c: str

# -------------------------
# ball
# ボールの描画・登録
def make_ball(x, y, vx, d=3, c="black"):
    id = canvas.create_rectangle(x, y, x + d, y + d,
                                 fill=c, outline=c)
    return Ball(id, x, y, vx, d, c)

# ボールの移動(左右)
def move_ball(ball):
    ball.x += ball.vx

# ボールの再描画
def redraw_ball(ball):
    canvas.coords(ball.id, ball.x, ball.y,
                  ball.x + ball.d, ball.y + ball.d)

# -------------------------
# paddle
# パドルの描画・登録
def make_paddle(x, y, w=20, h=100, c="blue"):
    id = canvas.create_rectangle(x, y, x + w, y + h,
                                 fill=c, outline=c)
    return Paddle(id, x, y, w, h, 0, c)

# パドルの移動(上下)
def move_paddle(pad):
    pad.y += pad.vy

# パドルの色を変える
def change_paddle_color(pad, c="red"):
    canvas.itemconfigure(pad.id, fill=c)
    canvas.itemconfigure(pad.id, outline=c)
    redraw_paddle(pad)

# パドルの再描画
def redraw_paddle(pad):
    canvas.coords(pad.id, pad.x, pad.y,
                  pad.x + pad.w, pad.y + pad.h)

# -------------------------
# パドル操作のイベントハンドラ
def up_paddle(event):        # 速度を上向き(マイナス)に設定
    paddle.vy = -PAD_VY

def down_paddle(event):      # 速度を下向き(プラス)に設定
    paddle.vy = PAD_VY

def stop_paddle(event):      # 速度をゼロに設定
    paddle.vy = 0

# -------------------------
tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()
tk.update()

paddle = make_paddle(PADDLE_X0, PADDLE_Y0)
ball = make_ball(200, BALL_Y0, BALL_VX, 10)

# イベントと、イベントハンドラを連結する。
canvas.bind_all('<KeyPress-Up>', up_paddle)
canvas.bind_all('<KeyPress-Down>', down_paddle)
canvas.bind_all('<KeyRelease-Up>', stop_paddle)
canvas.bind_all('<KeyRelease-Down>', stop_paddle)

# -------------------------
# プログラムのメインループ
while True:
    move_paddle(paddle)       # パドルの移動
    move_ball(ball)           # ボールの移動
    if ball.x + ball.vx <= 0: # ボールが左端に着いた
        ball.vx = -ball.vx
    if ball.x + ball.d >= 800:# ボールを右に逸らした
        break
    # ボールがパドルの左に届き、ボールの高さがパドルの幅に収まっている
    if (ball.x + ball.d >= paddle.x \
        and paddle.y < ball.y + ball.d \
        and ball.y < paddle.y + paddle.h):
        change_paddle_color(paddle, random.choice(COLORS)) # 色を変える
        ball.vx = -ball.vx    # ボールの移動方向が変わる
    redraw_paddle(paddle)     # パドルの再描画
    redraw_ball(ball)         # ボールの再描画
    tk.update_idletasks()     # イベント取得に必要
    tk.update()               # 描画が画面に反映される。
    time.sleep(DURATION)      # 次に描画するまで、sleep する。
