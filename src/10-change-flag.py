# Python によるプログラミング：第 10 章
# 例題 10.1 Flag の状態変化
# --------------------------
# プログラム名: 10-change-flag.py

from tkinter import Tk, Canvas
from dataclasses import dataclass, field

CELL_SIZE = 40

@dataclass
class Flag:
    flag: int = field(init=False, default=0)

    def update(self):  # 色をローテーションする
        self.flag = (self.flag + 1) % 3

def draw_flag(x, y, color):
    canvas.create_oval(x - CELL_SIZE/2, y - CELL_SIZE/2,
                       x + CELL_SIZE/2, y + CELL_SIZE/2,
                       outline=color, fill=color)

def on_right_click(event):
    x, y = (event.x, event.y)
    canvas.delete("all")
    f.update()
    if f.flag == 1:
        draw_flag(x, y, "red")
    elif f.flag == 2:
        draw_flag(x, y, "yellow")

tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

f = Flag()
canvas.bind('<Button-3>', on_right_click)
