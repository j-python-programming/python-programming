# Python によるプログラミング：第 3 章
#    例題 3.5 複数のブロック
# --------------------------
# プログラム名: 03-blocks.py

from tkinter import *
from dataclasses import dataclass
import time
import random

# 初期状態の設定 
DURATION = 0.002     # 描画間隔 (秒)
BALL_X0 = 400        # ボールの初期位置(x)
BALL_Y0 = 120        # ボールの初期位置(y)
BALL_D = 10          # ボールの大きさ
BALL_VX0 = 6         # ボールの初速(x)

PADDLE_X0 = 750      # パドルの初期位置(x)
PADDLE_Y0 = 80       # パドルの初期位置(y)
PAD_VY = 4           # パドルの速度

NUM_BLOCKS = 4       # ブロックの数
BLOCK_X = 10         # ブロックの位置(x)
BLOCK_Y = 100        # ブロックの位置(y)
BLOCK_W = 40         # ブロックの幅
BLOCK_H = 120        # ブロックの高さ

# 変える色を用意する。
COLORS = ["blue", "red", "green", "yellow", "brown", "gray"]

# -------------------------
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

@dataclass
class Block:
    id: int
    x: int
    y: int
    w: int
    h: int
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
# block
# ブロックの描画・登録
def make_block(x, y, w=40, h=120, c="green"):
    id = canvas.create_rectangle(x, y, x + w, y + h,
                                 fill=c, outline=c)
    return Block(id, x, y, w, h, c)

# ブロックを消す
def delete_block(block):
    canvas.delete(block.id)

# 複数のブロックを生成する
def make_blocks(n_rows, x0, y0, w, h, pad=10):
    blocks = []
    for x in range(n_rows):
        blocks.append(make_block(x0, y0, w, h))
        x0 = x0 + w + pad
    return blocks

# -------------------------
# wall
# 壁の生成
def make_walls(ox, oy, width, height):
    canvas.create_rectangle(ox, oy, ox + width, oy + height)

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

# ------------------
# 描画アイテムを準備する。
# ------------------
make_walls(0, 0, 800, 800)
ball = make_ball(BALL_X0, BALL_Y0, BALL_VX0, BALL_D)
paddle = make_paddle(PADDLE_X0, PADDLE_Y0)
blocks = make_blocks(NUM_BLOCKS, BLOCK_X, BLOCK_Y, BLOCK_W, BLOCK_H)

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
    if ball.x + ball.vx <= 0: # 左端の枠外：跳ね返す
        ball.vx = -ball.vx
    if ball.x + ball.d >= 800:# ボールを右に逸らした
        break

    # ボールがパドルの左に届き、ボールの高さがパドルの幅に収まっている
    if (ball.x + ball.d >= paddle.x \
        and paddle.y <= ball.y <= paddle.y + paddle.h):
        change_paddle_color(paddle, random.choice(COLORS))#色を変える
        ball.vx = -ball.vx     # ボールの移動方向が変わる

    for block in blocks:
        # ボールの X 位置がブロックに届き、Y 位置もブロックの範囲内
        if (ball.x <= block.x + block.w \
            and block.y <= ball.y <= block.y + block.h):
            ball.vx = - ball.vx      # ボールを跳ね返す
            delete_block(block)      # ブロックを消す
            blocks.remove(block)     # ブロックのリストから、このブロックを削除
            break
    if blocks == [] : break      # blocks リストが空になったら終了

    redraw_paddle(paddle)     # パドルの再描画
    redraw_ball(ball)         # ボールの再描画
    tk.update()               # 描画が画面に反映される。
    time.sleep(DURATION)      # 次に描画するまで、sleepする。

