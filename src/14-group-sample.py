# Pythonによるプログラミング：第14章　SpriteとGroup
# --------------------------
# プログラム名: 14-group-sample.py

import pygame

WHITE, RED = ((255, 255, 255), (255, 0, 0))
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
whites = pygame.sprite.Group()   # ⇦ Group クラス
reds = pygame.sprite.Group()     # ⇦ Group クラス
whites.add(Ball(100, 100, 10, 0, WHITE))     # ← add メソッド
whites.add(Ball(100-100, 200, 10, 0, WHITE)) # ← add メソッド
reds.add(Ball(400, 100, -10, 0, RED))        # ← add メソッド
reds.add(Ball(400+100, 200, -10, 0, RED))    # ← add メソッド

done = False
for i in range(60):
    for event in pygame.event.get():
        # 「閉じる」ボタンを処理する
        if event.type == pygame.QUIT: done = True
    if done: break
    clock.tick(FPS)
    reds.update()    # ⇦ update メソッド
    whites.update()  # ← update メソッド
    collided = pygame.sprite.groupcollide(whites, reds, False, False)
                     # ⇦ groupcollide メソッドで衝突判定は一行
    if collided != {} : print(collided)   # デバッグ用
    for white in collided: # 衝突判定後の処理
        white.change_color(RED)
        whites.remove(white)  # remove メソッドはそのまま
        reds.add(white)       # ← add メソッド
    reds.draw(screen)         # ⇦ draw メソッド 
    whites.draw(screen)       # ⇦ draw メソッド 
    pygame.display.flip()
    screen.fill((0, 0, 0))
pygame.quit()

