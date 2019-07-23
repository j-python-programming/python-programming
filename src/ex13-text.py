# Python によるプログラミング：第 13 章
# 練習問題 13.1 文字列の表示位置
# --------------------------
# プログラム名: ex13-text.py

import pygame

S_RED, S_GREEN, S_YELLOW = (0, 1, 2)
COLOR_LIST = [(255, 0, 0), (0, 255, 0), (255, 255, 0)]
COLOR_NAMES = ["red", "green", "yellow"]

pygame.init() # pygame.font.init()

screen = pygame.display.set_mode((640, 320))

clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsansms', 32)

signal = S_RED
loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
    color = COLOR_LIST[signal]
    text = font.render(COLOR_NAMES[signal] + " Light !", True, color)
    position = text.get_rect()
    position.center = screen.get_rect().center
    screen.blit(text, position)  # テキストを画面に転送する
    pygame.display.flip()  # 描画内容を更新する。
    clock.tick(1)
    screen.fill((0, 0, 0))
    signal = (signal + 1) % len(COLOR_LIST)
pygame.quit()

