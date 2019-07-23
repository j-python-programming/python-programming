# Pythonによるプログラミング：第14章　SpriteとGroup
# --------------------------
# プログラム名: 14-sprite-sample.py

import pygame

WHITE, RED=((255, 255, 255), (255, 0, 0))
D = 10
FPS = 20

class Ball(pygame.sprite.Sprite):# ← pygame.sprite.Sprite
    def __init__(self, x, y, vx, vy, color):
        super().__init__() # ←この一行
        self.vx, self.vy = (vx, vy)
        self.image = pygame.Surface((D, D))
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, D, D)

    def update(self):# ← このupdate
        # 描画位置を移動させる
        self.rect.move_ip(self.vx, self.vy)

    def change_color(self, color):
        self.image.fill(color)

screen = pygame.display.set_mode((640, 320))
clock = pygame.time.Clock()

# ボールを準備する
whites = []
reds = []
whites.append(Ball(100, 100, 10, 0, WHITE))
whites.append(Ball(100-100, 200, 10, 0, WHITE))
reds.append(Ball(400, 100, -10, 0, RED))
reds.append(Ball(400+100, 200, -10, 0, RED))

done = False
for i in range(60):
    for event in pygame.event.get():
        # 「閉じる」ボタンを処理する
        if event.type == pygame.QUIT: done = True
    if done: break
    clock.tick(FPS)
    collided = [] # 衝突判定用
    for white in whites:
        for red in reds:
            if pygame.sprite.collide_rect(white, red):  # 衝突判定
                collided.append(white)
    for white in collided: # 衝突判定後の処理
        white.change_color(RED)
        whites.remove(white)
        reds.append(white)
    for ball in reds + whites:
        ball.update()  # ←　このupdateの実行
        screen.blit(ball.image, ball.rect)
    pygame.display.flip()
    screen.fill((0, 0, 0))
pygame.quit()
