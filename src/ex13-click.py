# Python によるプログラミング：第 13 章
# 練習問題 13.2 クリック回数をカウント表示
# --------------------------
# プログラム名: ex13-click.py

import pygame
from dataclasses import dataclass

BOX_SIZE = 100  # サイズ
BOX_GAP = 20    # 間隔

BLACK = (0, 0, 0)
NUM_BOXES = 4
# 箱の数だけ、色も用意する
COLOR_LIST = [(255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255)]

@dataclass
class Box:
    pos: tuple
    color: tuple
    count: int
    # コンストラクタ
    def __init__(self, x, y, width, height, color):
        self.pos = (x, y, width, height)
        self.color = color
        self.count = 0

    def draw(self):
        self.rect = pygame.draw.rect(screen, self.color, self.pos)
        text = font.render(str(self.count), True, BLACK)
        position = text.get_rect()
        position.center = self.rect.center # 中央に表示
        screen.blit(text, position)  # テキストを画面に転送する
        pygame.display.flip()

    def countup(self, event):
        if (event.button == 1 \
            and self.rect.collidepoint(event.pos)):
            # event 座標が自分の箱の中だったら、処理
            self.count += 1
            self.draw()

def set_boxes(num):
    boxes = []
    (x, y) = screen.get_rect().center
    x -= (num/2 * BOX_SIZE + (num - 1) * BOX_GAP/2)
    y -= BOX_SIZE/2
    for i in range(num):
        box = Box(x, y, BOX_SIZE, BOX_SIZE, COLOR_LIST[i])
        box.draw()
        boxes.append(box)
        x += BOX_SIZE + BOX_GAP
    return boxes

pygame.init() # pygame.font.init()
screen = pygame.display.set_mode((640, 320))
clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsansms', 32)

boxes = set_boxes(NUM_BOXES)
loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif event.type == pygame.MOUSEBUTTONUP:
            for box in boxes:
                box.countup(event)
    clock.tick(50)

pygame.quit()

