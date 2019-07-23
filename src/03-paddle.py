# Python によるプログラミング：第 3 章
#    例題 3.2 上下にパドルを動かす
# --------------------------
# プログラム名: 03-paddle.py

from tkinter import *
from dataclasses import dataclass
import time

# 初期状態の設定
DURATION = 0.01    # 描画間隔（秒）
PADDLE_X0 = 750    # パドルの初期位置(x)
PADDLE_Y0 = 200    # パドルの初期位置(y)
PAD_VY = 2         # パドルの速度

@dataclass
class Paddle:
    id: int
    x: int
    y: int
    w: int
    h: int
    vy: int
    c: str

# パドルの描画・登録
def make_paddle(x, y, w=20, h=100, c="blue"):
    id = canvas.create_rectangle(x, y, x + w, y + h,
                                 fill=c, outline=c)
    return Paddle(id, x, y, w, h, 0, c)

# パドルの移動（上下）
def move_paddle(pad):
    pad.y += pad.vy

# パドルの再描画
def redraw_paddle(pad):
    canvas.coords(pad.id, pad.x, pad.y,
                  pad.x + pad.w, pad.y + pad.h)

# -------------------------
# パドル操作のイベントハンドラ
def up_paddle(event):        # 速度を上向き（マイナス）に設定
    paddle.vy = -PAD_VY

def down_paddle(event):      # 速度を下向き（プラス）に設定
    paddle.vy = PAD_VY

def stop_paddle(event):      # 速度をゼロに設定
    paddle.vy = 0

# -------------------------

tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()
tk.update()

paddle = make_paddle(PADDLE_X0, PADDLE_Y0)

# イベントと、イベントハンドラを連結する。
canvas.bind_all('<KeyPress-Up>', up_paddle)
canvas.bind_all('<KeyPress-Down>', down_paddle)
canvas.bind_all('<KeyRelease-Up>', stop_paddle)
canvas.bind_all('<KeyRelease-Down>', stop_paddle)

# -------------------------
# プログラムのメインループ
while True:
    move_paddle(paddle)       # パドルの移動
    redraw_paddle(paddle)     # パドルの再描画
    # tk.update_idletasks()     # イベント取得に必要
    tk.update()               # 描画が画面に反映される。
    time.sleep(DURATION)      # 次に描画するまで、 sleep する。
