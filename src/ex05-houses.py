# Python によるプログラミング：第 5 章　
#    練習問題 5.1 家クラスの定義
# --------------------------
# プログラム名: ex05-houses.py

from tkinter import *

class House:
    def __init__(self, w, h, roof_color, wall_color):
        # 属性の設定を行う
        self.w = w
        self.h = h
        self.roof_color = roof_color
        self.wall_color = wall_color

    def draw(self, x, y):
        # キャンバスに自分自身を描画する。(x,y) を家の左上の座標とする。
        rtop_x = x + self.w/2 # roof top x
        wtop_y = y + self.h/2 # wall top y
        bottom_x = x + self.w
        bottom_y = y + self.h
        canvas.create_polygon(
            rtop_x, y, x, wtop_y, x + self.w, wtop_y,
            outline=self.roof_color, fill=self.roof_color
            )
        canvas.create_rectangle(
            x, wtop_y, bottom_x, bottom_y,
            outline=self.wall_color, fill=self.wall_color
            )

tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=1, bg="whitesmoke")
canvas.pack()

houses = [
    House(50, 100, "green", "white"),
    House(100, 70, "blue", "gray"),
    House(70, 120, "blue", "white"),
    House(50, 50, "red", "orange")
    ]

x = 0
y = 100
PAD = 10
for house in houses:
    house.draw(x, y)
    x = x + house.w + PAD
