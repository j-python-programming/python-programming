# Pythonによるプログラミング：第4章　ゲームの拡張
# --------------------------
# プログラム名: ex04-blocks.py

from tkinter import *
from dataclasses import dataclass
import random
import time

# =================================================
# 初期設定値(定数)
WALL_EAST = 800                 # 壁の東側最大値(X最大)
WALL_SOUTH = 600                # 壁の南側最大値(Y最大)

VX0 = [-3, -2, -1, 1, 2, 3]     # ボールのx方向初速選択肢
BALL_X0 = WALL_EAST / 2         # ボールの初期位置(x)
BALL_Y0 = 150                   # ボールの初期位置(y)
BALL_D = 10                     # ボールの大きさ
BALL_VX = random.choice(VX0)    # ボールのx方向初速
BALL_VY = 3                     # ボールのy方向初速
SPEED_UP = 10                   # ボールを加速させる頻度
BALL_MAX_VY = 10                # ボールの最高速度
MULTI_BALL_COUNT = 4            # ボールを分裂させる頻度
BALL_MAX_NUM = 5                # 分裂したボールの最大数

PADDLE_X0 = WALL_EAST / 2 - 50  # パドルの初期位置(x)
PADDLE_Y0 = WALL_SOUTH - 100    # パドルの初期位置(y)
PADDLE_W = 100                  # パドルの幅(w)
PADDLE_H = 20                   # パドルの高さ(h)
PADDLE_VX = 5                   # パドルの速度
                                # 変える色を用意する。
PADDLE_COLORS = ["blue", "red", "green", "yellow", "brown", "gray"]
PADDLE_SHORTEN = 10             # 一回にパドルを短くする量
PADDLE_SHORTEN_COUNT = 10       # パドルを短くするヒット回数
PADDLE_MIN_W = 20               # パドルの最小の幅 

NUM_ROWS = 9         # x方向のブロックの数
NUM_COLS = 3         # y方向のブロックの数
BLOCK_X = 10         # ブロックの位置(x)
BLOCK_Y = 50         # ブロックの位置(y)
BLOCK_W = 80         # ブロックの幅
BLOCK_H = 30         # ブロックの高さ
BLOCK_PAD = 5        # ブロックの間(パディング)
BLOCK_COLORS = ["green", "blue", "darkgray"] #ブロックの色

CANDY_BONUS = 50
CANDY_W = 10
CANDY_H = 10

ADD_SCORE = 10                  # 得点の増加値
DURATION = 0.01                 # 描画間隔(秒)

# -----------------------------------
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
    pt: int
    bc: int
    c: str

@dataclass
class Spear:
    id: int
    x: int
    y: int
    w: int
    h: int
    vy: int
    c: str

@dataclass
class Candy:
    id: int
    x: int
    y: int
    w: int
    h: int
    vy: int
    c: str

@dataclass
class Game:
    start: int
# -------------------------
# ball
# ボールの描画・登録
def make_ball(x, y, vx, vy, d=3, c="black"):
    id = canvas.create_oval(x, y, x + d, y + d, fill=c, outline=c)
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
def make_paddle(x, y, w=PADDLE_W, h=PADDLE_H, c="blue"):
    id = canvas.create_rectangle(x, y, x + w, y + h, fill=c, outline=c)
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
def make_block(x, y, w=120, h=40, pt=10, bc=1, c="green"):
    id = canvas.create_rectangle(x, y, x + w, y + h, fill=c, outline=c)
    return Block(id, x, y, w, h, pt, bc, c)

# ブロックを消す
def delete_block(block):
    canvas.delete(block.id)

# 複数のブロックを生成する
def make_blocks(n_rows, n_cols, x0, y0, w, h, pad, colors):
    blocks = []
    x0_save = x0
    for y in range(n_cols):
        x0 = x0_save
        bc = n_cols - y
        pt = 10 * bc
        for x in range(n_rows):
            blocks.append(make_block(x0, y0, w, h, pt, bc,
                                     colors[bc - 1]))
            x0 = x0 + w + pad
        y0 = y0 + h + pad
    return blocks

# ------------------
# spear
# 槍の描画・登録
def make_spear(x, y, w=1, h=40, vy=5, c="red"):
    id = canvas.create_rectangle(x, y, x + w, y + h,
                                 fill=c, outline=c)
    return Spear(id, x, y, w, h, vy, c)

# 槍を消す
def delete_spear(spear):
    canvas.delete(spear.id)

# 槍の移動(上下)
def move_spear(spear):
    spear.y += spear.vy

# 槍の再描画
def redraw_spear(spear):
    canvas.coords(spear.id, spear.x, spear.y,
                  spear.x + spear.w, spear.y + spear.h)

# ------------------
# candy(ボーナスアイテム)
# キャンディの描画・登録
def make_candy(x, y, w=5, h=5, vy=5, c="green"):
    id = canvas.create_rectangle(x, y, x + w, y + h,
                                 fill=c, outline=c)
    return Candy(id, x, y, w, h, vy, c)

# キャンディを消す
def delete_candy(candy):
    canvas.delete(candy.id)

# キャンディの移動(上下)
def move_candy(candy):
    candy.y += candy.vy

# キャンディの再描画
def redraw_candy(candy):
    canvas.coords(candy.id, candy.x, candy.y,
                  candy.x + candy.w, candy.y + candy.h)

# -------------------------
# wall
# 壁の生成
def make_walls(ox, oy, width, height):
    canvas.create_rectangle(ox, oy, ox + width, oy + height)

# ------------------
# SPACE Keyを待つ
def game_start(event):
    game.start = True

def game_over():
    canvas.create_text(WALL_EAST/2, 200, text="Game Over!",
                       font = ('FixedSys', 16))

# -------------------------
# パドル操作のイベントハンドラ
def left_paddle(event):        # 速度を左向き(マイナス)に設定
    paddle.vx = -PADDLE_VX

def right_paddle(event):       # 速度を右向き(プラス)に設定
    paddle.vx = PADDLE_VX

def stop_paddle(event):        # 速度をゼロに設定
    paddle.vx = 0

# =================================================
# 初期設定
tk = Tk()
tk.title("Game")

canvas = Canvas(tk, width=WALL_EAST, height=WALL_SOUTH, bd=0,
                highlightthickness=0)
canvas.pack()
tk.update()

game = Game(False)

score = 0           # 得点
spear = None
candy = None
paddle_count = 0    # パドルでボールを打った回数
balls = []          # ボールの配列

# 描画アイテムを準備する。
make_walls(0, 0, WALL_EAST, WALL_SOUTH)
paddle = make_paddle(PADDLE_X0, PADDLE_Y0)
balls.append(make_ball(BALL_X0, BALL_Y0, BALL_VX, BALL_VY, BALL_D))
blocks = make_blocks(NUM_ROWS, NUM_COLS, BLOCK_X, BLOCK_Y,
                     BLOCK_W, BLOCK_H, BLOCK_PAD, BLOCK_COLORS)

# イベントと、イベントハンドラを連結する。
canvas.bind_all('<KeyPress-Left>', left_paddle)
canvas.bind_all('<KeyPress-Right>', right_paddle)
canvas.bind_all('<KeyRelease-Left>', stop_paddle)
canvas.bind_all('<KeyRelease-Right>', stop_paddle)
canvas.bind_all('<KeyPress-space>', game_start)  # SPACE が押された

# -------------------------
# スコアの表示
id_score = canvas.create_text(
    10, 10, text=("score: " + str(score)), font=("FixedSys", 16),
    justify="left", anchor=NW
    )

# SPACEの入力待ち
id_text = canvas.create_text(
    WALL_EAST/2, 200, text="Press 'SPACE' to start",
    font=('FixedSys', 16)
    )

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
    move_paddle(paddle)       # パドルの移動
    if spear:
        move_spear(spear)     # 槍の落下
    if candy:
        move_candy(candy)     # キャンディの落下
    for ball in balls:
        move_ball(ball)       # ボールの移動
        if ball.x + ball.vx <= 0:  # 左側の壁で跳ね返る
            ball.vx = - ball.vx
        if ball.x + ball.d + ball.vx  >= WALL_EAST: # 右の壁
            ball.vx = - ball.vx
        if ball.y + ball.vy <= 0:  # 上の壁
            ball.vy = - ball.vy
        if ball.y + ball.d + ball.vy >= WALL_SOUTH : # 下に逸らした
            canvas.delete(ball.id)   # ボールを画面から消す
            balls.remove(ball)
    if len(balls)==0:   # 最後のボールを逃した
        game_over()
        break
    if spear:
        if (paddle.x <= spear.x <= paddle.x + paddle.w \
            and spear.y + spear.h > paddle.y \
            and spear.y <= paddle.y + paddle.h):  # 槍に当たった
            redraw_paddle(paddle)
            redraw_spear(spear)
            game_over()
            break
    if candy:
        if (paddle.x <= candy.x <= paddle.x + paddle.w \
            and candy.y + candy.h > paddle.y \
            and candy.y <= paddle.y + paddle.h):  # ボーナスアイテムゲット
            score += CANDY_BONUS
            canvas.itemconfigure(id_score, text="score:" + str(score))
            delete_candy(candy)
            candy = None

    for ball in balls:
        # ボールの下側がパドルの上面に届き、横位置がパドルと重なる
        if (paddle.y <= ball.y + ball.d <= paddle.y + paddle.h \
            and paddle.x < ball.x + ball.d/2 < paddle.x + paddle.w):
            change_paddle_color(paddle, random.choice(PADDLE_COLORS))
            ball.vy = -ball.vy    # ボールの移動方向が変わる
            # 移動後もパドルと重なる：横から重なった場合
            if paddle.y <= ball.y + ball.d + ball.vy <= paddle.y + paddle.h:
                ball.y = paddle.y - ball.d # パドルの上に戻す
            paddle_count += 1
            if paddle_count % PADDLE_SHORTEN_COUNT == 0: # パドルを短くするか？
                if paddle.w > PADDLE_MIN_W:  # まだ短くできる！
                    paddle.w -= PADDLE_SHORTEN
            if paddle_count % SPEED_UP == 0: # ボールを加速させるか？
                if ball.vy > - BALL_MAX_VY: # まだ加速できる！
                    ball.vy -= 1   # ボールが上向きになっていることに注意！
            # ボールの位置によって、反射角度を変える
            ball.vx = int(6 * (ball.x + ball.d/2 - paddle.x)
                             / paddle.w) - 3
            if paddle_count % MULTI_BALL_COUNT == 0: # ボールを発生
                if len(balls) < BALL_MAX_NUM:
                    balls.append(
                        make_ball(
                            BALL_X0, BALL_Y0, random.choice(VX0),
                            BALL_VY, BALL_D
                            ))

        for block in blocks: # 全てのブロックについて、調べる
            # ボールのX位置がブロックの範囲内で、ボールのY位置がブロックの範囲内
            if (block.x < ball.x + ball.d/2 < block.x + block.w \
                and (block.y <= ball.y <= block.y + block.h
                     or block.y <= ball.y + ball.d \
                         <= block.y + block.h)):
                ball.vy = -ball.vy
                block.bc -= 1
                if block.bc == 0:  # 硬さの残りが0
                    score += block.pt  # ブロックごとに得点が異なる
                    canvas.itemconfigure(id_score, text="score:" + str(score))
                    delete_block(block)
                    blocks.remove(block)
                    break
                else:   # ブロックの色で硬さを表す
                    canvas.itemconfigure(block.id,
                                         fill=BLOCK_COLORS[block.bc - 1])
                    canvas.itemconfigure(block.id,
                                         outline=BLOCK_COLORS[block.bc - 1])

    if len(blocks) == 0:  # 配列が空の、別のチェック方法
        canvas.create_text(WALL_EAST/2, 200,
                           text="Clear!", font=('FixedSys', 16))
        break

    if spear==None and random.random() < 0.01:  # 確率1%で発生
        spear = make_spear(random.randint(100, WALL_EAST - 100), 10)
    if spear and spear.y + spear.h >= WALL_SOUTH:
        delete_spear(spear)
        spear = None

    if candy==None and random.random() < 0.005:
        candy = make_candy(random.randint(100, WALL_EAST - 100), 10,
                           CANDY_W, CANDY_H)
    if candy and candy.y + candy.h >= WALL_SOUTH:
        delete_candy(candy)
        candy = None

    redraw_paddle(paddle)        # パドルの再描画
    for ball in balls:
        redraw_ball(ball)     # ボールの再描画
    if spear:
        redraw_spear(spear)   # 槍の再描画
    if candy:
        redraw_candy(candy)   # キャンディの再描画
    tk.update_idletasks()     # Window描画を更新する。
    tk.update()               # 描画が画面に反映される。
    time.sleep(DURATION)      # 次に描画するまで、sleepする。
