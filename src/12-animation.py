# Python によるプログラミング：第 12 章
# 例題 12.4 アニメーション
# --------------------------
# プログラム名: 12-animation.py

import pygame

FPS = 60     # Frame per Second 毎秒のフレーム数
LOOP = True

# ボールの描画関数
def draw_ball(screen, x, y, radius=10):
    pygame.draw.circle(screen, (255, 255, 0), (x, y), radius)

screen = pygame.display.set_mode((640, 320))
clock = pygame.time.Clock()   # 時計オブジェクト
x, y = (100, 100)   # ボールの初期位置
vx = 10             # ボールの速度

while LOOP:  # 描画のループ
    for event in pygame.event.get():
        # 「閉じる」ボタンを処理する
        if event.type == pygame.QUIT: LOOP = False
    clock.tick(FPS)      # 毎秒の呼び出し回数に合わせて遅延
    x += vx
    if not (0 <= x <= 640):  # 画面の外に出たら、向きを変える
        vx = -vx
    draw_ball(screen, x, y)  # ボールを描画する
    pygame.display.flip() # ボール描画を画面に反映
    screen.fill((0, 0, 0))  # 塗潰し：次の flip まで反映されない
pygame.quit()   # 画面を閉じる
