# Python によるプログラミング：第 13 章
# 例題 13.2 マウスイベントの取得
# --------------------------
# プログラム名: 13-click-signal.py

import pygame

S_RED, S_GREEN, S_YELLOW = (0, 1, 2)
COLOR_LIST = [(255, 0, 0), (0, 255, 0), (255, 255, 0)]

def handles_mouseup(event):
    global signal      # 関数外で宣言されたsignalを使う
    print("pressed")   # 動作確認用
    print(event.button)
    # 最初は以下のif文全体が無い状態で試しにプログラムを動かしてみましょう。
    if event.button == 1 and rect.collidepoint(event.pos):
        signal = (signal + 1) % len(COLOR_LIST) # 色をローテーションする
        color = COLOR_LIST[signal]
        pygame.draw.circle(screen, color, center, radius) # 円の描画
        pygame.display.flip()

screen = pygame.display.set_mode((640, 320))
clock = pygame.time.Clock()

signal = S_RED 
center, radius = (screen.get_rect().center, 100)
color = COLOR_LIST[signal]   # 初期設定の色
rect = pygame.draw.circle(screen, color, center, radius)
pygame.display.flip()

loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        if event.type == pygame.MOUSEBUTTONUP:
            handles_mouseup(event)
    clock.tick(50)

pygame.quit()
