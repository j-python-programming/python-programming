# Python によるプログラミング：第 10 章　
# 実習課題 10.1 Cell ファイルの分割
# --------------------------
# プログラム名: p10cell.py

from tkinter import Tk, Canvas, CENTER
from dataclasses import dataclass, field

@dataclass
class Cell:
    canvas: Canvas
    width: int
    height: int
    cell_size: int
    offset_x: int
    offset_y: int
    font: str
    opened: list = field(init=False)
    flag: list = field(init=False)
    id_flag: list = field(init=False)
    id_text: list = field(init=False)

    def __post_init__(self):
        self.opened = [[False for y in range(self.height)]
                              for x in range(self.width)]
        self.flag = [[0 for y in range(self.height)]
                        for x in range(self.width)]
        self.id_flag = [[None for y in range(self.height)]
                              for x in range(self.width)]
        self.id_text = [[None for y in range(self.height)]
                              for x in range(self.width)]
        for i in range(self.width):
            x = i * self.cell_size + self.offset_x
            for j in range(self.height):
                y = j * self.cell_size + self.offset_y
                self.canvas.create_rectangle(
                    x, y, x + self.cell_size, y + self.cell_size
                    )
                self.id_flag[i][j] = self.canvas.create_oval(
                    x + 1, y + 1, x + self.cell_size - 1,
                    y + self.cell_size - 1,
                    outline="white", fill="white"
                    )
                self.id_text[i][j] = self.canvas.create_text(
                    x + self.cell_size/2,
                    y + self.cell_size/2,
                    text="-", font=self.font, anchor=CENTER
                    )

    def is_open(self, i, j):
        return self.opened[i][j]

    def update(self, i, j):  # 色をローテーションする
        self.flag[i][j] = (self.flag[i][j] + 1) % 3

    def draw(self, i, j, text=""):
        if self.opened[i][j]:  # 開いている場合は、テキストを表示する
            self.canvas.itemconfigure(self.id_text[i][j], text=text)
        elif self.flag[i][j] == 0:  # 印なしの状態
            self.canvas.itemconfigure(self.id_flag[i][j],
                                      outline="white", fill="white")
            self.canvas.itemconfigure(self.id_text[i][j], text="-")
        elif self.flag[i][j] == 1:  # 危険印：赤マル
            self.canvas.itemconfigure(self.id_flag[i][j],
                                      outline="red", fill="red")
        else:   # self.flag[i][j] == 2  # 疑問形：黄色
            self.canvas.itemconfigure(self.id_flag[i][j],
                                      outline="yellow",
                                      fill="yellow")

    def open(self, i, j):
        self.opened[i][j] = True
        # 開かれたら、もはや「旗」マークは表示しない。
        self.canvas.delete(self.id_flag[i][j])
