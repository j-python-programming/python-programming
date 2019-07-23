# Python によるプログラミング：第 3 章
#    練習問題 3.2
# ボールは上部、左、右の3方向の壁で跳ね返る
# ボールが画面の下部に出てしまった場合ゲームオーバ
# --------------------------
# プログラム名: ex03-2-paddle.py

from tkinter import *
from dataclasses import dataclass
import random
import time

# 初期状態の設定
SPEEDS = [-3, -2, -1, 1, 2, 3]  # ボールのx方向初速選択肢
DURATION = 0.01                 # 描画間隔(秒)
BALL_X0 = 400                   # ボールの初期位置(x)
BALL_Y0 = 100                   # ボールの初期位置(y)
PADDLE_X0 = 350                 # パドルの初期位置(x)
PADDLE_Y0 = 500                 # パドルの初期位置(y)
PADDLE_VX = 5                   # パドルの速度

BALL_VX = random.choice(SPEEDS) # ボールのx方向初速
BALL_VY = 3                     # ボールのy方向初速

# 変える色を用意する。
COLORS = ["blue", "red", "green", "yellow", "brown", "gray"]

# -------------------------
@dataclass
class Ball:
    id: int
    x: int
    y: int
    vx: int
    vy: int
    d: int
    c: str

@dataclass
class Paddle:
    id: int
    x: int
    y: int
    w: int
    h: int
    vx: int
    c: str
# -------------------------
# ball
# ボールの描画・登録
def make_ball(x, y, vx, vy, d=3, c="black"):
    id = canvas.create_oval(x, y, x + d, y + d,
                            fill=c, outline=c)
    return Ball(id, x, y, vx, vy, d, c)

# ボールの移動
def move_ball(ball):
    ball.x += ball.vx
    ball.y += ball.vy

# ボールの再描画
def redraw_ball(ball):
    canvas.coords(ball.id, ball.x, ball.y,
                  ball.x + ball.d, ball.y + ball.d)

# -------------------------
# paddle
# パドルの描画・登録
def make_paddle(x, y, w=100, h=20, c="blue"):
    id = canvas.create_rectangle(x, y, x + w, y + h,
                                 fill=c, outline=c)
    return Paddle(id, x, y, w, h, 0, c)

# パドルの移動(左右)
def move_paddle(pad):
    pad.x += pad.vx

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
def left_paddle(event):        # 速度を左向き(マイナス)に設定
    paddle.vx = -PADDLE_VX

def right_paddle(event):       # 速度を右向き(マイナス)に設定
    paddle.vx = PADDLE_VX

def stop_paddle(event):        # 速度をゼロに設定
    paddle.vx = 0

# =================================================
tk = Tk()
tk.title("Game")

canvas = Canvas(tk, width=800, height=600, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

# ------------------
# 描画アイテムを準備する。
paddle = make_paddle(PADDLE_X0, PADDLE_Y0)
ball = make_ball(BALL_X0, BALL_Y0, BALL_VX, BALL_VY, 10)

# イベントと、イベントハンドラを連結する。
canvas.bind_all('<KeyPress-Left>', left_paddle)
canvas.bind_all('<KeyPress-Right>', right_paddle)
canvas.bind_all('<KeyRelease-Left>', stop_paddle)
canvas.bind_all('<KeyRelease-Right>', stop_paddle)

# -------------------------
# プログラムのメインループ
while True:
    move_paddle(paddle)       # パドルの移動
    move_ball(ball)           # ボールの移動
    if ball.x + ball.vx <= 0:  # 左側の壁で跳ね返る
        ball.vx = -ball.vx
    if ball.x + ball.d + ball.vx  >= 800: # 右の壁
        ball.vx = -ball.vx
    if ball.y + ball.vy <= 0:  # 上の壁
        ball.vy = -ball.vy
    if ball.y + ball.d + ball.vy >= 600 : # 下に逸らした
        break
    # ボールの下側がパドルの上面に届き、横位置がパドルと重なる
    if (paddle.y <= ball.y + ball.d <= paddle.y + paddle.h \
        and paddle.x < ball.x + ball.d/2 < paddle.x + paddle.w):
        change_paddle_color(paddle, random.choice(COLORS))#色を変える
        ball.vy = -ball.vy    # ボールの移動方向が変わる

    redraw_paddle(paddle)     # パドルの再描画
    redraw_ball(ball)         # ボールの再描画
    tk.update_idletasks()     # イベント取得に必要
    tk.update()               # 描画が画面に反映される。
    time.sleep(DURATION)      # 次に描画するまで、sleep する。
