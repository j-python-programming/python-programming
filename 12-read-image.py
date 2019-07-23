# Python によるプログラミング：第 12 章
# 例題 12.3 背景画像を表示する
# --------------------------
# プログラム名: 12-read-image.py

import pygame

screen = pygame.display.set_mode((640, 320))   # screen を準備する
background = pygame.image.load("background.png")  # 背景画像を読み込む
ball = pygame.image.load("ball.png")              # ボール画像を読み込む
ball = ball.convert()                          # 画像を変換する。
ball.set_colorkey(ball.get_at((0, 0))) # 左上の (0, 0) を背景色に指定
background.blit(ball, (100, 100))   # 背景画像上にボールを転送
background.blit(ball, (200, 200))
screen.blit(background, (0, 0))     # screen に背景ごと画像を転送
pygame.display.flip()
