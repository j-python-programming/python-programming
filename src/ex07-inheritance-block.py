# Python によるプログラミング：第 7 章
#  練習問題 7.1 Ball, Block Paddle の再定義
# --------------------------
# プログラム名: ex07-inheritance-block.py

from tkinter import *
from dataclasses import dataclass
import time

# 定数群
BOX_TOP_X = 100        # ゲーム領域の左上X座標
BOX_TOP_Y = 100        # ゲーム領域の左上Y座標
BOX_WIDTH = 300        # ゲーム領域の幅
BOX_HEIGHT = 300       # ゲーム領域の高さ

CANVAS_WIDTH = BOX_TOP_X + BOX_WIDTH + 100    # Canvasの幅
CANVAS_HEIGHT = BOX_TOP_Y + BOX_HEIGHT + 100  # Canvasの高さ
CANVAS_BACKGROUND = "lightgray"               # Canvasの背景色

DURATION = 0.05        # 描画間隔

BALL_Y0 = BOX_TOP_Y + BOX_HEIGHT/2   # ボールの初期位置(Y)
BALL_DIAMETER = 10     # ボールの直径
BALL_VX = 10           # ボールの速度
BALL_COLOR = "red"     # ボールの色

NUM_BLOCKS = 5                 # ブロックの数
BLOCK_WIDTH = 8                # ブロックの幅
BLOCK_HEIGHT = 20              # ブロックの高さ
BLOCK_COLOR = "green"          # ブロックの色
BLOCK_SPAN = BLOCK_WIDTH + 2   # ブロックの間隔
BLOCK_TOP = BALL_Y0 - BLOCK_HEIGHT/2    # ブロックの位置(Y)を計算

PADDLE_WIDTH = 10      # パドルの幅
PADDLE_HEIGHT = 40     # パドルの高さ
PADDLE_COLOR = "black" # パドルの色

# ----------------------------------
class CustomCanvas(Canvas):
    def __init__(self, width=300, height=300, bg="white"):
        super().__init__(tk, width=width, height=height, bg=bg)
        # Canvas.__init__(self, tk, width=width, height=height, bg=bg)
        self.pack()

# 共通の親クラスとして、MovingObjectを定義
@dataclass
class MovingObject:
    id: int
    x: int
    y: int
    w: int
    h: int
    vx: int
    vy: int

    def redraw(self):                   # 再描画(移動結果の画面反映)
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.w, self.y + self.h)

    def move(self):                     # 移動させる
        self.x += self.vx
        self.y += self.vy


# Ballは、MovingObjectを継承している。
class Ball(MovingObject):
    def __init__(self, id, x, y, d, vx):
        MovingObject.__init__(self, id, x, y, d, d, vx, 0)
        # super().__init__(id, x, y, d, d, vx, 0) # も可能
        self.d = d      # 直径として記録


# Paddleは、MovingObjectを継承している。
class Paddle(MovingObject):
    def __init__(self, id, x, y, w, h):
        MovingObject.__init__(self, id, x, y, w, h, 0, 0)
        # super().__init__(id, x, y, w, h, 0, 0) # も可能

    def set_v(self, v):
        self.vy = v     # 移動量の設定は、独自メソッド

    def stop(self):     # 停止も、Paddle独自のメソッド
        self.vy = 0


# ブロックも、MovingObjectを継承
class Block(MovingObject):
    def __init__(self, id, x, y, w, h): 
        MovingObject.__init__(self, id, x, y, w, h, 0, 0)
        # super().__init__(id, x, y, w, h, 0, 0) # も可能

# ----------------------------------
# Box(ゲーム領域)の定義
@dataclass
class Box:
    west: int
    north: int
    east: int
    south: int
    ball: Ball
    paddle: Paddle
    blocks: list
    duration: float

    def __init__(self, x, y, w, h, duration):
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.ball = None
        self.paddle = None
        self.paddle_v = 2
        self.blocks = []
        self.duration = duration

    def create_ball(self, x, y, d, vx):  # ボールの生成
        id = canvas.create_oval(x, y, x + d, y + d, fill=BALL_COLOR)
        return Ball(id, x, y, d, vx)

    def create_paddle(self, x, y, w, h): # パドルの生成
        id = canvas.create_rectangle(x, y, x + w, y + h, fill=PADDLE_COLOR)
        return Paddle(id, x, y, w, h)

    def create_block(self, x, y, w, h):  # ブロックの生成
        id = canvas.create_rectangle(x, y, x + w, y + h, fill=BLOCK_COLOR)
        return Block(id, x, y, w, h)

    def check_wall(self, ball):   # 壁に当たった時の処理
        if ball.x <= self.west or ball.x + ball.d >= self.east:
            ball.vx = - ball.vx

    def check_paddle(self, paddle, ball):  # ボールがパドルに当たった処理
        if (ball.x + ball.d >=paddle.x
            and paddle.y <= ball.y + ball.d
            and ball.y <= paddle.y + paddle.h):
            ball.vx = - ball.vx

    def check_block(self, block, ball):  # ボールがブロックに当たったか判定
        if (block.x + block.w >= ball.x  # X位置の確認
            and ball.y + ball.d/2 >= block.y              # 上端
            and ball.y + ball.d/2 <= block.y + block.h):  # 下端
            return True
        else:
            return False

    def up_paddle(self, event):   # パドルを上に移動(Event処理)
        self.paddle.set_v(- self.paddle_v)

    def down_paddle(self, event): # パドルを下に移動(Event処理)
        self.paddle.set_v(self.paddle_v)

    def stop_paddle(self, event): # パドルを止める(Event処理)
        self.paddle.stop()

    def set(self):   # 初期設定を一括して行う
        # ボールの生成
        self.ball = self.create_ball(self.west + NUM_BLOCKS * BLOCK_SPAN,
                                     BALL_Y0, BALL_DIAMETER, BALL_VX)
        # パドルの生成
        self.paddle = self.create_paddle(self.east - 20,
                                         BALL_Y0 - PADDLE_HEIGHT/2,
                                         PADDLE_WIDTH, PADDLE_HEIGHT)
        for x in range(NUM_BLOCKS): # ブロックの生成
            block = self.create_block(self.west + x * BLOCK_SPAN,
                                      BLOCK_TOP, BLOCK_WIDTH, BLOCK_HEIGHT)
            self.blocks.append(block)
        # イベント処理の登録
        canvas.bind_all('<KeyPress-Up>', self.up_paddle)
        canvas.bind_all('<KeyPress-Down>', self.down_paddle)
        canvas.bind_all('<KeyRelease-Up>', self.stop_paddle)
        canvas.bind_all('<KeyRelease-Down>', self.stop_paddle)

    def animate(self):
        movingObjs = [self.paddle, self.ball]   # 動くものを一括登録
        while True:
            for obj in movingObjs:
                obj.move()          # 座標を移動させる
            self.check_wall(self.ball)   # 壁との衝突処理
            self.check_paddle(self.paddle, self.ball)  # パドル反射
            for block in self.blocks:
                if self.check_block(block, self.ball): # ブロック衝突
                    self.ball.vx = - self.ball.vx
                    canvas.delete(block.id)
                    self.blocks.remove(block)
            if len(self.blocks) == 0:  # 最後のブロックを消したら
                break                  # 抜ける

            for obj in movingObjs:
                obj.redraw()    # 移動後の座標で再描画(画面反映)
            time.sleep(self.duration)
            tk.update()

# ----------------------------------
# メインルーチン
tk = Tk()
canvas = CustomCanvas(width=CANVAS_WIDTH,
                      height=CANVAS_HEIGHT, bg=CANVAS_BACKGROUND)

box = Box(BOX_TOP_X, BOX_TOP_Y, BOX_WIDTH, BOX_HEIGHT, DURATION)
box.set()       # ゲームの初期設定
box.animate()   # アニメーション
