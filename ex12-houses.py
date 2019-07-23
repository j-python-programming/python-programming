# Python によるプログラミング：第 12 章
# 練習問題 12.1 例題 1.1 の「家」の描画
# --------------------------
# プログラム名: ex12-houses.py

import pygame
from dataclasses import dataclass

PAD = 10     # 家と家の間隔

RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LIGHTGRAY = (224, 224, 224)
GRAY = (128, 128, 128)
ORANGE = (255, 160, 96)

# House オブジェクト
@dataclass
class House:
    w: int
    h: int
    roof_color: str
    wall_color: str

# 家を特定の場所に描く
def draw_house_at(x, y, w, h, roof_color, wall_color):
    rtop_x = x + w/2 # roof top x
    wtop_y = y + h/2 # wall top y
    bottom_x = x + w
    bottom_y = y + h
    draw.polygon(screen, roof_color, ((rtop_x, y), (x, wtop_y),
                                      (bottom_x, wtop_y)))
    draw.rect(screen, wall_color, (x, wtop_y, w, h/2))

# 家の描画のWrapper関数
def draw_house(house, x, y):
    draw_house_at(x, y, house.w, house.h,
                  house.roof_color, house.wall_color )

screen = pygame.display.set_mode((640, 320))   # screenを準備する
draw = pygame.draw

houses = [
    House(50, 100, GREEN, LIGHTGRAY),
    House(100, 70, BLUE, GRAY),
    House(70, 120, BLUE, LIGHTGRAY),
    House(50, 50, RED, ORANGE),
    ]

x = 50
y = 50

screen.fill((255, 255, 255))   # 背景を白一色で塗りつぶす
for house in houses:
    draw_house(house, x, y)
    x += house.w + PAD
pygame.display.flip()   # 描画内容を画面に反映する

# pygame.quit()

