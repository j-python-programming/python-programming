# Python によるプログラミング：第 12 章
# 例題 12.5 イベント処理
# --------------------------
# プログラム名: 12-event.py

import pygame

FPS = 60     # Frame per Second 毎秒のフレーム数
LOOP = True

# パドルの描画関数
def draw_paddle(screen, x, y):
    pygame.draw.rect(screen, (0, 255, 255), (x, y, 40, 100))

screen = pygame.display.set_mode((640, 320))
clock = pygame.time.Clock()     # 時計オブジェクト
paddle_x, paddle_y = (540, 100) # パドルの初期位置
paddle_vy = 10                  # パドルの速度

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
    draw_paddle(screen, paddle_x, paddle_y)  # パドルの描画
    pygame.display.flip()       # 画面への反映
    screen.fill((0, 0, 0))  # 塗潰し：次の flip まで反映されない
pygame.quit()
