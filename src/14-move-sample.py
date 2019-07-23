# Python によるプログラミング：第 14 章
# 例題 14.1 移動する物体
# --------------------------
# プログラム名: 14-move-sample.py

import pygame

WHITE, RED=((255, 255, 255), (255, 0, 0))
D = 10
FPS = 20

class Ball:
    def __init__(self, x, y, vx, vy, color):
        self.vx, self.vy = (vx, vy)
        self.image = pygame.Surface((D, D))
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, D, D) # screen への blit 座標

    def move(self):
        # 描画位置を移動させる
        self.rect.move_ip(self.vx, self.vy)

screen = pygame.display.set_mode((640, 320))
clock = pygame.time.Clock()

# ボールを準備する
whites = []
reds = []
whites.append(Ball(100, 100, 10, 0, WHITE))
whites.append(Ball(100-100, 200, 10, 0, WHITE))
reds.append(Ball(400, 100, -10, 0, RED))
reds.append(Ball(400+100, 200, -10, 0, RED))

for i in range(60):
    for event in pygame.event.get():
        # 「閉じる」ボタンを処理する
        if event.type == pygame.QUIT: i = 60
    clock.tick(FPS)
    for ball in reds + whites:
        ball.move()
        screen.blit(ball.image, ball.rect)
    pygame.display.flip()
    screen.fill((0, 0, 0))
pygame.quit()

