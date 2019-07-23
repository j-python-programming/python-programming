# Python によるプログラミング：第 12 章
# 練習問題 12.2 例題 6.4 の箱の中のボール移動
#  draw の利用
# --------------------------
# プログラム名: ex12-bouncing-draw.py

import pygame
from dataclasses import dataclass
import random

WIDTH = 640
HEIGHT = 640

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
COLORS = [RED, GREEN, BLUE, YELLOW]

FPS = 60     # Frame per Second 毎秒のフレーム数

@dataclass
class Ball:
    x: int
    y: int
    d: int
    vx: int
    vy: int
    color: str

    def move(self):
        self.x += self.vx
        self.y += self.vy 

    def draw(self):
        draw.circle(screen, self.color, (self.x, self.y), self.d)

@dataclass
class Box:
    west: int
    north: int
    east: int
    south: int
    def __init__(self, x, y, w, h):
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)

    def check_wall(self, ball):
        if ball.x <= self.west or ball.x + ball.d >= self.east:
            ball.vx = -ball.vx
        if ball.y <= self.north or ball.y + ball.d >= self.south:
            ball.vy = -ball.vy

    def set_ball(self):
        self.ball = Ball(random.randint(self.west, self.east),
                         random.randint(self.north, self.south),
                         random.randint(5, 10),
                         random.randint(3, 8),
                         random.randint(3, 8),
                         random.choice(COLORS))

    def animate(self):
        loop = True
        screen.fill(WHITE)   # 背景を白一色で塗りつぶす
        while loop: # 無限ループ
            for event in pygame.event.get():
                # 「閉じる」ボタンを処理する
                if event.type == pygame.QUIT: loop = False

            clock.tick(FPS)      # 毎秒の呼び出し回数に合わせて遅延
            self.ball.move()
            self.check_wall(self.ball)
            self.ball.draw()
            pygame.display.flip()   # 描画内容を画面に反映する
            screen.fill(WHITE)   # 背景を白一色で塗りつぶす

# ---------------------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # screen を準備する
clock = pygame.time.Clock()   # 時計オブジェクト
draw = pygame.draw

box = Box(0, 0, WIDTH, HEIGHT) # 盤面の初期化
box.set_ball()                 # ボールを生成する
box.animate()                  # メインルーチン
pygame.quit()                  # 画面を閉じる
