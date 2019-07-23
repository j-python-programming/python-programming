# Python によるプログラミング：第 13 章
# 例題 13.3 テキストの表示
# --------------------------
# プログラム名: 13-signal-text.py

import pygame

COLOR_NAMES = ["red", "green", "yellow"]
COLOR_LIST = [pygame.Color(COLOR_NAMES[i])
              for i in range(len(COLOR_NAMES))]
    
pygame.init() # pygame.font.init()

screen = pygame.display.set_mode((640, 320))

clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsansms', 32)

signal = 0
loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
    color = COLOR_LIST[signal]
    text = font.render(COLOR_NAMES[signal] + " Light !",
                       True, color)
    screen.blit(text, (0, 0))  # テキストを画面に転送する
    pygame.display.flip()  # 描画内容を更新する。
    clock.tick(1)
    screen.fill((0, 0, 0))
    signal = (signal + 1) % len(COLOR_LIST)
pygame.quit()
