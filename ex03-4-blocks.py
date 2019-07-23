# Python によるプログラミング：第 3 章　
#    発展問題 3.4
# パドルの位置で、跳ね返る角度を変えよ。
# --------------------------
# プログラム名: ex03-4-blocks.py

from tkinter import *
from dataclasses import dataclass
import random
import time

# 初期状態の設定
SPEEDS = [-3, -2, -1, 1, 2, 3]  # ボールのx方向初速選択肢
DURATION = 0.01                 # 描画間隔(秒)
BALL_X0 = 400                   # ボールの初期位置(x)
BALL_Y0 = 100                   # ボールの初期位置(y)
BALL_D = 10                     # ボールの大きさ
BALL_VX = random.choice(SPEEDS) # ボールのx方向初速
BALL_VY = 3                     # ボールのy方向初速

PADDLE_X0 = 350                 # パドルの初期位置(x)
PADDLE_Y0 = 500                 # パドルの初期位置(y)
PADDLE_VX = 5                   # パドルの速度

NUM_BLOCKS = 5       # ブロックの数
BLOCK_X = 10         # ブロックの位置(x)
BLOCK_Y = 50         # ブロックの位置(y)
BLOCK_W = 120        # ブロックの幅
BLOCK_H = 40         # ブロックの高さ

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

@dataclass
class Block:
    id: int
    x: int
    y: int
    w: int
    h: int
    c: str

@dataclass
class Game:
    start: int
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

# ------------------
# block
# ブロックの描画・登録
def make_block(x, y, w=40, h=120, c="green"):
    id = canvas.create_rectangle(x, y, x + w, y + h, fill=c, outline=c)
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

# ------------------
# SPACE Keyを待つ
def game_start(event):
    game.start = True

# -------------------------
# パドル操作のイベントハンドラ
def left_paddle(event):        # 速度を左向き(マイナス)に設定
    paddle.vx = -PADDLE_VX

def right_paddle(event):       # 速度を右向き(プラス)に設定
    paddle.vx = PADDLE_VX

def stop_paddle(event):        # 速度をゼロに設定
    paddle.vx = 0

# =================================================
tk = Tk()
tk.title("Game")
canvas = Canvas(tk, width=800, height=600, bd=0,
                highlightthickness=0)
canvas.pack()
tk.update()

game = Game(False)

# ------------------
# 描画アイテムを準備する。
make_walls(0, 0, 800, 600)
paddle = make_paddle(PADDLE_X0, PADDLE_Y0)
ball = make_ball(BALL_X0, BALL_Y0, BALL_VX, BALL_VY, BALL_D)
blocks = make_blocks(NUM_BLOCKS, BLOCK_X, BLOCK_Y,
                     BLOCK_W, BLOCK_H)

# イベントと、イベントハンドラを連結する。
canvas.bind_all('<KeyPress-Left>', left_paddle)
canvas.bind_all('<KeyPress-Right>', right_paddle)
canvas.bind_all('<KeyRelease-Left>', stop_paddle)
canvas.bind_all('<KeyRelease-Right>', stop_paddle)
canvas.bind_all('<KeyPress-space>', game_start)  # SPACE が押された

# -------------------------
# SPACE の入力待ち
id_text = canvas.create_text(400, 200, text="Press 'SPACE' to start",
                             font = ('FixedSys', 16))
tk.update()

while not game.start:    # ひたすら SPACE を待つ
    tk.update_idletasks()
    tk.update()
    time.sleep(DURATION)

canvas.delete(id_text)  # SPACE入力のメッセージを削除
tk.update()

# -------------------------
# プログラムのメインループ
while True:
    move_paddle(paddle)          # パドルの移動
    move_ball(ball)           # ボールの移動
    if ball.x + ball.vx <= 0: # 左端の枠外：跳ね返す
        ball.vx = -ball.vx
    if ball.x + ball.d + ball.vx >= 800: # 右の壁
        ball.vx = -ball.vx
    if ball.y + ball.vy <= 0: # 上の壁
        ball.vy = -ball.vy
    if ball.y + ball.d + ball.vy >= 600 : # 下に逸らした
        canvas.create_text(400, 200, text="Game Over!", font = ('FixedSys', 16))
        break
    # ボールの下側がパドルの上面に届き、横位置がパドルと重なる
    if (paddle.y <= ball.y + ball.d <= paddle.y + paddle.h \
        and paddle.x < ball.x + ball.d/2 < paddle.x + paddle.w):
        change_paddle_color(paddle, random.choice(COLORS)) # 色を変える
        ball.vy = -ball.vy    # ボールの移動方向が変わる
        # ボールの位置によって、反射角度を変える
        ball.vx = int(6 * (ball.x + ball.d/2 - paddle.x) / paddle.w) - 3

    for block in blocks: # 全てのブロックについて、調べる
        # ボールのX位置がブロックの範囲内で、ボールのY位置がブロックの範囲内
        if (block.x < ball.x + ball.d/2 < block.x + block.w \
            and block.y <= ball.y <= block.y + block.h):
            ball.vy = -ball.vy
            delete_block(block)
            blocks.remove(block)
            break
    if len(blocks) == 0:  # 配列が空の、別のチェック方法
        canvas.create_text(400, 200, text="Clear!", font = ('FixedSys', 16))
        break

    redraw_paddle(paddle)     # パドルの再描画
    redraw_ball(ball)         # ボールの再描画
    tk.update_idletasks()     # イベント取得に必要
    tk.update()               # 描画が画面に反映される。
    time.sleep(DURATION)      # 次に描画するまで、sleepする。
  
