# Python によるプログラミング：第 12 章
# 例題 12.2 blit を試す
# --------------------------
# プログラム名: 12-blit.py

import pygame

RED = (255, 0, 0)

screen = pygame.display.set_mode((640, 320))  # 描画領域を準備する
image = pygame.Surface((100, 100))   # 画像描画用の Surface を用意
image.fill((0, 0, 0))                # 背景を黒一色で塗りつぶす

pygame.draw.circle(image, (255, 0, 0), (50, 50), 50)  # 一番外側
pygame.draw.circle(image, (191, 0, 0), (50, 50), 40)
pygame.draw.circle(image, (127, 0, 0), (50, 50), 30)
pygame.draw.circle(image, (63, 0, 0), (50, 50), 20)
pygame.draw.circle(image, (0, 0, 0), (50, 50), 10)    # 一番内側

screen.blit(image, (100, 100))   # screen の (100,100) に円を転送
screen.blit(image, (150, 150))   
screen.blit(image, (200, 200))
pygame.display.flip()           # 描画内容を画面に反映させる。
