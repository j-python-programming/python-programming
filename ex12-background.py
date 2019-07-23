# Python によるプログラミング：第 12 章
# 発展問題 12.4 背景画像を描画させる
# --------------------------
# プログラム名: ex12-background.py

from dataclasses import dataclass
import pygame
import random

WIDTH = 640
HEIGHT = 320

# 色の定義
FPS = 60     # Frame per Second 毎秒のフレーム数

# --------------------------
# ボールクラス
@dataclass
class Ball:
    x: int
    y: int
    dx: int
    dy: int
    vx: int
    vy: int
    image: pygame.Surface

    def move(self):
        self.x += self.vx
        self.y += self.vy 

    def draw(self, to_image):
        to_image.blit(self.image, (self.x, self.y))

# ---------------------------------
# ボックスクラス
@dataclass
class Box:
    west: int
    north: int
    east: int
    south: int
    balls: list
    def __init__(self, x, y, w, h):
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.balls = []

    def check_wall(self, ball):
        if ball.x <= self.west or ball.x + ball.dx >= self.east:
            ball.vx = -ball.vx
        if ball.y <= self.north or ball.y + ball.dy >= self.south:
            ball.vy = -ball.vy

    def set(self, files):
        self.background = pygame.image.load("background.png")  # 背景画像を読み込む
        for file in files:
            image = pygame.image.load(file).convert()   # ボール画像を読み込む
            image.set_colorkey(image.get_at((0, 0)))
            rect = image.get_rect()
            dx, dy = (rect.width, rect.height)
            # 初期位置を乱数化 : 壁の中に生成しないようにする
            ball_x = random.randint(self.west + 1, self.east - dx - 1)
            ball_y = random.randint(self.north + 1, self.south - dy - 1)
            ball = Ball(ball_x, ball_y, dx, dy, 
                        random.randint(1, 8), random.randint(1, 8), image)
            self.balls.append(ball)

    def animate(self):
        loop = True
        screen.blit(self.background, (0, 0))     # screen に背景ごと画像を転送
        while loop: # 無限ループ
            for event in pygame.event.get():
                # 「閉じる」ボタンを処理する
                if event.type == pygame.QUIT: loop = False

            clock.tick(FPS)      # 毎秒の呼び出し回数に合わせて遅延
            for ball in self.balls:
                ball.move()
                self.check_wall(ball)
                ball.draw(screen)
            pygame.display.flip()   # 描画内容を画面に反映する
            screen.blit(self.background, (0, 0)) # screen に背景ごと画像を転送

# ---------------------------------------
# メインプログラム
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # screenを準備する
clock = pygame.time.Clock()   # 時計オブジェクト
draw = pygame.draw

ball_files = ["ball.png", "ball2.png", "ball2.png"]

box = Box(0, 0, WIDTH, HEIGHT) # 盤面の初期化
box.set(ball_files)            # ボールを生成する
box.animate()                  # メインルーチン
pygame.quit()                  # 画面を閉じる
