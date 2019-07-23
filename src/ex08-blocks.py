# Python によるプログラミング：第 8 章
# 前半のまとめ ( ブロック崩し )
# --------------------------
# プログラム名: ex08-blocks.py

from tkinter import Tk, Canvas, SW
from dataclasses import dataclass, field
import random
import time

# =================================================
# 初期設定値(定数)
BOX_MARGIN = 50
BOX_TOP_X = BOX_MARGIN # ゲーム領域の左上X座標
BOX_TOP_Y = BOX_MARGIN # ゲーム領域の左上Y座標
BOX_WIDTH = 700        # ゲーム領域の幅
BOX_HEIGHT = 500       # ゲーム領域の高さ
BOX_CENTER = BOX_TOP_X + BOX_WIDTH/2 # ゲーム領域の中心

CANVAS_WIDTH = BOX_TOP_X + BOX_WIDTH + BOX_MARGIN    # Canvasの幅
CANVAS_HEIGHT = BOX_TOP_Y + BOX_HEIGHT + BOX_MARGIN  # Canvasの高さ
CANVAS_BACKGROUND = "lightgray"                      # Canvasの背景色

DURATION = 0.01        # 描画間隔

NUM_COLS = 8                    # x方向のブロックの数
NUM_ROWS = 3                    # y方向のブロックの数
BLOCK_WIDTH = 80                # ブロックの幅
BLOCK_HEIGHT = 30               # ブロックの高さ
BLOCK_PAD = 5                   # ブロックの間(パディング)
BLOCK_TOP = 50                  # ブロックの上の隙間(回り込み用)
BLOCK_POINTS = 10               # ブロックの基礎点
BLOCK_SPAN_X = BLOCK_WIDTH + BLOCK_PAD
BLOCK_SPAN_Y = BLOCK_HEIGHT + BLOCK_PAD
BLOCK_BOTTOM = BOX_TOP_Y + BLOCK_TOP + BLOCK_SPAN_Y * NUM_ROWS
BLOCK_COLORS = ["green", "blue", "darkgray"] #ブロックの色

VX0 = [-3, -2, -1, 1, 2, 3]     # ボールのx方向初速選択肢
BALL_DIAMETER = 10              # ボールの直径
BALL_X0 = BOX_CENTER - BALL_DIAMETER/2      # ボールの初期位置(X)
BALL_Y0 = BLOCK_BOTTOM + 10     # ボールの初期位置(Y)
BALL_VX = random.choice(VX0)    # ボールのx方向初速
BALL_VY = 3                     # ボールのy方向初速
SPEED_UP = 10                   # ボールを加速させる頻度
BALL_MAX_VY = 8                 # ボールの最高速度
MULTI_BALL_COUNT = 4            # ボールを分裂させる頻度
BALL_MAX_NUM = 5                # 分裂したボールの最大数
BALL_COLOR = "red"              # ボールの色

MESSAGE_Y = BALL_Y0 + 50        # メッセージ表示のY座標

PADDLE_WIDTH = 100              # パドルの幅
PADDLE_HEIGHT = 20              # パドルの高さ
PADDLE_X0 = BOX_TOP_X + (BOX_WIDTH - PADDLE_WIDTH)/2  # パドルの初期位置(x)
PADDLE_Y0 = BOX_TOP_Y + BOX_HEIGHT - 60    # パドルの初期位置(y)
PADDLE_VX = 5                   # パドルの速度
PADDLE_COLORS = ["blue", "red", "green", "yellow", "brown", "gray"]
                                # 変える色を用意する。
PADDLE_SHORTEN = 10             # 一回にパドルを短くする量
PADDLE_SHORTEN_COUNT = 5        # パドルを短くするヒット回数
PADDLE_MIN_W = 40               # パドルの最小の幅 

SPEAR_WIDTH = 1                 # 槍の横幅
SPEAR_HEIGHT = 40               # 槍の長さ
SPEAR_VY = 5                    # 槍の落ちる速さ
SPEAR_COLOR = "blue"            # 槍の色

CANDY_BONUS = 50                # ボーナス点
CANDY_WIDTH = 10                # ボーナスアイテムの幅
CANDY_HEIGHT = 10               # ボーナスアイテムの高さ
CANDY_VY = 4                    # ボーナスアイテムの落下速度
CANDY_COLOR = "RED"             # ボーナスアイテムの色

ADD_SCORE = 10                  # 得点の増加値

# ----------------------------------
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
    def __init__(self, id, x, y, d, vx, vy):
        MovingObject.__init__(self, id, x, y, d, d, vx, vy)
        self.d = d      # 直径として記録


# Paddleは、MovingObjectを継承している。
class Paddle(MovingObject):
    def __init__(self, id, x, y, w, h, c):
        MovingObject.__init__(self, id, x, y, w, h, 0, 0)
        self.c = c

    def set_v(self, v):
        self.vx = v     # 移動量の設定は、独自メソッド

    def stop(self):     # 停止も、Paddle独自のメソッド
        self.vx = 0


# Spearは、MovingObjectを継承している。
class Spear(MovingObject):
    def __init__(self, id, x, y, w, h, vy, c):
        MovingObject.__init__(self, id, x, y, w, h, 0, vy)


class Candy(MovingObject):
    def __init__(self, id, x, y, w, h, vy, c):
        MovingObject.__init__(self, id, x, y, w, h, 0, vy)


# ブロック
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


# ----------------------------------
# Box(ゲーム領域)の定義
@dataclass
class Box:
    west: int
    north: int
    east: int
    south: int
    balls: list
    paddle: Paddle
    paddle_v: int
    blocks: list
    duration: float
    run: int
    score: int
    paddle_count: int
    spear: Spear
    candy: Candy

    def __init__(self, x, y, w, h, duration):
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.balls = []
        self.paddle = None
        self.blocks = []
        self.paddle_v = PADDLE_VX
        self.duration = duration
        self.run = False
        self.score = 0  # 得点
        self.paddle_count = 0    # パドルでボールを打った回数
        self.spear = None
        self.candy = None

    # 壁の生成
    def make_walls(self):
        canvas.create_rectangle(self.west, self.north, self.east, self.south,
                                outline="black")

    def create_ball(self, x, y, d, vx, vy):  # ボールの生成
        id = canvas.create_oval(x, y, x + d, y + d, fill=BALL_COLOR)
        return Ball(id, x, y, d, vx, vy)

    # パドルの生成
    def create_paddle(self, x, y, w, h, c):
        id = canvas.create_rectangle(x, y, x + w, y + h, fill=c)
        return Paddle(id, x, y, w, h, c)

    # 槍の生成
    def create_spear(self, x, y, w=SPEAR_WIDTH, h=SPEAR_HEIGHT, c=SPEAR_COLOR):
        id = canvas.create_rectangle(x, y, x + w, y + h, fill=c)
        return Spear(id, x, y, w, h, SPEAR_VY, c)

    # ボーナスアイテムの生成
    def create_candy(self, x, y, w=CANDY_WIDTH, h=CANDY_HEIGHT, c=CANDY_COLOR):
        id = canvas.create_rectangle(x, y, x + w, y + h, fill=c)
        return Candy(id, x, y, w, h, CANDY_VY, c)

    def create_block(self, x, y, w, h, pt, bc, c):  # ブロックの生成
        id = canvas.create_rectangle(x, y, x + w, y + h, fill=c)
        return Block(id, x, y, w, h, pt, bc, c)

    def check_wall(self, ball):   # 壁に当たった時の処理
        if ball.y + ball.d + ball.vy >= self.south:  # 下に逃した
            return True
        if (ball.x + ball.vx <= self.west \
            or ball.x + ball.d + ball.vx >= self.east):
            ball.vx = -ball.vx
        if ball.y + ball.vy <= self.north:
            ball.vy = -ball.vy
        return False

    def check_paddle(self, paddle, ball):  # ボールがパドルに当たった処理
        hit = False
        # 左から当たる
        if (paddle.x <= ball.x + ball.d + ball.vx <= paddle.x + paddle.w
            and paddle.y <= ball.y + ball.d/2 + ball.vy <= paddle.y + paddle.h):
            hit = True
            ball.vx = - ball.vx
        # 上から当たる
        elif (paddle.y <= ball.y + ball.d + ball.vy <= paddle.y + paddle.h
            and paddle.x <= ball.x + ball.d/2 + ball.vx <= paddle.x + paddle.w):
            # ボールの位置によって、反射角度を変える
            hit = True
            ball.vx = int(6*(ball.x + ball.d/2 - paddle.x) / paddle.w) - 3
            ball.vy = - ball.vy
        # 右から当たる
        elif (paddle.x <= ball.x + ball.vx <= paddle.x + paddle.w \
            and paddle.y <= ball.y + ball.d/2 + ball.vy <= paddle.y + paddle.h):
            hit = True
            ball.vx = - ball.vx
        # パドルのボーダーチェック
        if paddle.x + paddle.vx <= self.west:
            paddle.stop()
            paddle.x = self.west
        elif self.east <= paddle.x + paddle.vx + paddle.w:
            paddle.stop()
            paddle.x = self.east - paddle.w
        if hit: # パドルにボールが当たった
            self.paddle_count += 1
            if self.paddle_count % MULTI_BALL_COUNT == 0: # ボールを発生
                if len(self.balls) < BALL_MAX_NUM:
                    ball = self.create_ball(BALL_X0, BALL_Y0,
                                            BALL_DIAMETER,
                                            random.choice(VX0), BALL_VY)
                    self.balls.append(ball)
                    self.movingObjs.append(ball)
            if self.paddle_count % PADDLE_SHORTEN_COUNT == 0: # パドルを短くするか？
                if paddle.w > PADDLE_MIN_W:  # まだ短くできる！
                    paddle.w -= PADDLE_SHORTEN
            if self.paddle_count % SPEED_UP == 0: # ボールを加速させるか？
                if ball.vy > -BALL_MAX_VY: # まだ加速できる！
                    ball.vy -= 1   # ボールが上向きになっていることに注意！

    def check_block(self, block, ball):  # ボールがブロックに当たったか判定
        # 上から当たる
        if (block.y <= ball.y + ball.d + ball.vy <= block.y + block.h \
            and block.x <= ball.x + ball.d/2 + ball.vx <= block.x + block.w):
            ball.vy = - ball.vy
            return True
        # 右から当たる
        elif (block.x <= ball.x + ball.vx <= block.x + block.w
            and block.y <= ball.y + ball.d/2 + ball.vy <= block.y + block.h):
            ball.vx = - ball.vx
            return True
        # 左から当たる
        elif (block.x <= ball.x + ball.d + ball.vx <= block.x + block.w
            and block.y <= ball.y + ball.d/2 + ball.vy <= block.y + block.h):
            ball.vx = - ball.vx
            return True
        # 下から当たる
        elif (block.y <= ball.y + ball.vy <= block.y + block.h
            and block.x <= ball.x + ball.d/2 + ball.vx <= block.x + block.w):
            ball.vy = - ball.vy
            return True
        else:
            return False

    def check_spear(self, spear, paddle):
        if (paddle.x <= spear.x <= paddle.x + paddle.w \
            and spear.y + spear.h > paddle.y \
            and spear.y <= paddle.y + paddle.h):  # 槍に当たった
            return True
        else:
            return False

    def check_candy(self, candy, paddle):
        if (paddle.x <= candy.x <= paddle.x + paddle.w \
            and candy.y + candy.h > paddle.y \
            and candy.y <= paddle.y + paddle.h):  # ボーナスゲット！
            return True
        else:
            return False

    def left_paddle(self, event):   # パドルを左に移動(Event処理)
        self.paddle.set_v(- self.paddle_v)

    def right_paddle(self, event):  # パドルを右に移動(Event処理)
        self.paddle.set_v(self.paddle_v)

    def stop_paddle(self, event):   # パドルを止める(Event処理)
        self.paddle.stop()

    def game_start(self, event):
        self.run = True

    def game_end(self, message):
        self.run = False
        canvas.create_text(BOX_CENTER, MESSAGE_Y,
                           text=message, font=('FixedSys', 16))
        tk.update()

    def update_score(self):
        canvas.itemconfigure(self.id_score,
                             text="score:" + str(self.score))

    def wait_start(self):
        # SPACEの入力待ち
        id_text = canvas.create_text(BOX_CENTER, MESSAGE_Y,
                                     text="Press 'SPACE' to start",
                                     font=('FixedSys', 16))
        tk.update()
        while not self.run:    # ひたすらSPACEを待つ
            tk.update()
            time.sleep(self.duration)
        canvas.delete(id_text)  # SPACE入力のメッセージを削除
        tk.update()

    def set(self):   # 初期設定を一括して行う
        # 壁の描画
        self.make_walls()
        # スコアの表示
        self.id_score = canvas.create_text(
            BOX_TOP_X,
            BOX_TOP_Y - 2,
            text=("score: " + str(self.score)),
            font=("FixedSys", 16), justify="left",
            anchor=SW
            )
        # ボールの生成
        ball = self.create_ball(BALL_X0, BALL_Y0,
                                BALL_DIAMETER, BALL_VX, BALL_VY)
        self.balls.append(ball)
        # パドルの生成
        self.paddle = self.create_paddle(PADDLE_X0, PADDLE_Y0,
                                         PADDLE_WIDTH, PADDLE_HEIGHT,
                                         random.choice(PADDLE_COLORS))
        # ブロックの生成
        for y in range(NUM_ROWS):
            bc = NUM_ROWS - y   # ブロックの硬さ(1〜NUM_ROWS)
            for x in range(NUM_COLS):
                block = self.create_block(
                    self.west + x * BLOCK_SPAN_X + BLOCK_PAD,
                    self.north + y * BLOCK_SPAN_Y + BLOCK_TOP,
                    BLOCK_WIDTH, BLOCK_HEIGHT,
                    BLOCK_POINTS * bc, bc,
                    BLOCK_COLORS[bc - 1]
                    )
                self.blocks.append(block)
        # イベント処理の登録
        canvas.bind_all('<KeyPress-Right>', self.right_paddle)
        canvas.bind_all('<KeyPress-Left>', self.left_paddle)
        canvas.bind_all('<KeyRelease-Right>', self.stop_paddle)
        canvas.bind_all('<KeyRelease-Left>', self.stop_paddle)
        canvas.bind_all('<KeyPress-space>', self.game_start)  # SPACEが押された

    def animate(self):
        # 動くものを一括登録
        self.movingObjs = [self.paddle] + self.balls
        while self.run:
            for obj in self.movingObjs:
                obj.move()          # 座標を移動させる
            if self.spear:
                if self.check_spear(self.spear, self.paddle):
                    self.game_end("You are destroyed!")  # ゲームオーバの表示
                    break               # 槍に当たった
            if self.candy:
                if self.check_candy(self.candy, self.paddle):
                    self.score += CANDY_BONUS
                    self.update_score()
                    canvas.delete(self.candy.id)
                    self.movingObjs.remove(self.candy)
                    self.candy = None
            for ball in self.balls:
                if self.check_wall(ball):  # 壁との衝突処理
                    canvas.delete(ball.id)
                    self.balls.remove(ball)
                    self.movingObjs.remove(ball)
                self.check_paddle(self.paddle, ball)  # パドル反射
                for block in self.blocks:
                    if self.check_block(block, ball): # ブロック衝突
                        block.bc -= 1  # 硬さが一つ減る
                        if block.bc > 0:
                            canvas.itemconfigure(block.id,
                                                 fill=BLOCK_COLORS[block.bc - 1])
                        else:  # 硬さがゼロになった。
                            self.score = self.score + block.pt
                            self.update_score()
                            canvas.delete(block.id)
                            self.blocks.remove(block)
            if len(self.balls) == 0:
                self.game_end("Game Over!")  # ゲームオーバの表示
                break               # 最後のボールを下に逃した
            if len(self.blocks) == 0:   # 最後のブロックを消したら
                self.game_end("Clear!")  # ゲームオーバの表示
                break                   # 抜ける
            if self.spear==None and random.random() < 0.01:  # 確率1%で発生
                self.spear = self.create_spear(
                    random.randint(self.west, self.east),
                    self.north)
                self.movingObjs.append(self.spear)
            if self.candy==None and random.random() < 0.005:  # 確率0.5%で発生
                self.candy = self.create_candy(
                    random.randint(self.west, self.east),
                    self.north)
                self.movingObjs.append(self.candy)

            if self.spear and self.spear.y + self.spear.h >= self.south:
                canvas.delete(self.spear.id)
                self.movingObjs.remove(self.spear)
                self.spear = None
            if self.candy and self.candy.y + self.candy.h >= self.south:
                canvas.delete(self.candy.id)
                self.movingObjs.remove(self.candy)
                self.candy = None

            for obj in self.movingObjs:
                obj.redraw()    # 移動後の座標で再描画(画面反映)
            time.sleep(self.duration)
            tk.update()

# -------------------
tk=Tk()
tk.title("Game")

canvas = Canvas(tk, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=CANVAS_BACKGROUND)
canvas.pack()

# ----------------------------------
# メインルーチン
box = Box(BOX_TOP_X, BOX_TOP_Y, BOX_WIDTH, BOX_HEIGHT, DURATION)
box.set()           # ゲームの初期設定
box.wait_start()    # 開始待ち
box.animate()       # アニメーション
