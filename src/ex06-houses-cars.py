# Python によるプログラミング：第 6 章
#  練習問題 6.5 ポリモーフィズムの利用
# --------------------------
# プログラム名: ex06-houses-cars.py

from tkinter import *
from dataclasses import dataclass

@dataclass
class House:
    w: int
    h: int
    roof_color: str
    wall_color: str

    def draw(self, x, y):
        # キャンバスに自分自身を描画する。(x,y)を家の左上の座標とする。
        rtop_x = x + self.w/2 # roof top x
        wtop_y = y + self.h/2 # wall top y
        bottom_x = x + self.w
        bottom_y = y + self.h
        canvas.create_polygon(  # 多角形の頂点
            rtop_x, y,
            x, wtop_y,
            x + self.w, wtop_y,
            outline=self.roof_color, fill=self.roof_color)
        canvas.create_rectangle(
            x, wtop_y, bottom_x, bottom_y,
            outline=self.wall_color, fill=self.wall_color)

    def width(self):  # 図形の幅を返す
        return self.w

@dataclass
class Car:
    w: int
    h: int
    wh: int
    body_color: str
    wheel_color: str

    def draw(self, x, y):  # 車を描画する。
        bottom_x = x + self.w
        bottom_y = y + self.h
        r = self.w/4
        canvas.create_rectangle(x, y, bottom_x, bottom_y,
                                outline=self.body_color,
                                fill=self.body_color)
        canvas.create_oval(x + self.w/4 - self.wh, bottom_y - self.wh,
                           x + self.w/4 + self.wh, bottom_y + self.wh,
                           outline=self.wheel_color, fill=self.wheel_color)
        canvas.create_oval(x + 3*self.w/4 - self.wh, bottom_y - self.wh,
                           x + 3*self.w/4 + self.wh, bottom_y + self.wh,
                           outline=self.wheel_color, fill=self.wheel_color)

    def width(self):  # 図形の幅を返す
        return self.w

tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=0, bg="whitesmoke")
canvas.pack()

objects = [
    House(50, 100, "green", "white"),
    House(100, 70, "blue", "gray"),
    Car(120, 50, 10, "blue", "gray"),
    Car(120, 70, 6, "red", "gray")
    ]

x = 0
PAD = 10
for obj in objects:
    obj.draw(x, 100)
    x = x + obj.width() + PAD
