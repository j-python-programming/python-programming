# Python によるプログラミング：第 12 章
# 例題 12.6 衝突処理
# --------------------------
# プログラム名: 12-collision.py

import pygame

FPS = 60     # Frame per Second 毎秒のフレーム数
LOOP = True

# ボールの描画関数
def draw_ball(screen, x, y, radius=10):
    return pygame.draw.circle(screen, (255, 255, 0), (x, y), radius)

# パドルの描画関数
def draw_paddle(screen, x, y):
    return pygame.draw.rect(screen, (0, 255, 255), (x, y, 40, 100))

screen = pygame.display.set_mode((640, 320))
clock = pygame.time.Clock()   # 時計オブジェクト

x, y= (100, 100)   # ボールの初期位置
vx = 10            # ボールの速度
paddle_x, paddle_y= (540, 100) # パドルの初期位置
paddle_vy = 10                 # パドルの速度

while LOOP:  # メインループ
    for event in pygame.event.get():
        # 「閉じる」ボタンを処理する
        if event.type == pygame.QUIT: LOOP = False

    clock.tick(FPS)      # 毎秒の呼び出し回数に合わせて遅延
    pressed_keys = pygame.key.get_pressed() # キー情報を取得
    if pressed_keys[pygame.K_UP]:    # 上が押されたら
        paddle_y -= paddle_vy        # y 座標を小さく
    if pressed_keys[pygame.K_DOWN]:  # 下が押されたら
        paddle_y += paddle_vy        # y 座標を大きく
    # パドルを取得する
    paddle_rect = draw_paddle(screen, paddle_x, paddle_y)

    x += vx              # ボールの移動
    if not (0 <= x <= 640):  # 画面の外に出たら、向きを変える
        vx = -vx
    ball_rect = draw_ball(screen, x, y)   # ボールの取得
    if (ball_rect.colliderect(paddle_rect)):
        vx = -vx    # パドルと衝突したら、ボールを反転
    pygame.display.flip() # パドルとボールの描画を画面に反映
    screen.fill((0, 0, 0))  # 塗潰し：次の flip まで反映されない

pygame.quit()   # 画面を閉じる
