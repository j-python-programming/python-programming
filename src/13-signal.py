# Python によるプログラミング：第 13 章
# 例題 13.1 時間経過の取得
# --------------------------
# プログラム名: 13-signal.py

import pygame

S_RED, S_GREEN, S_YELLOW = (0, 1, 2)
COLOR_LIST = [(255, 0, 0), (0, 255, 0), (255, 255, 0)]

screen = pygame.display.set_mode((640, 320))
clock = pygame.time.Clock()

signal = S_RED 
center, radius = (screen.get_rect().center, 100)
loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
    pygame.draw.circle(screen, COLOR_LIST[signal], center, radius)
    signal = (signal + 1) % len(COLOR_LIST) # トグル式に変える
    pygame.display.flip()
    clock.tick(1) # 1 秒経過を待つ
pygame.quit()

