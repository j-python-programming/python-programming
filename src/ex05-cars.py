# Python によるプログラミング：第 5 章
#  練習問題 5.2 　車クラスの定義
# --------------------------
# プログラム名: ex05-cars.py

from tkinter import *

class Car:
    def __init__(self, w, h, wh, body_color, wheel_color):
        self.w = w
        self.h = h
        self.wh = wh
        self.body_color = body_color
        self.wheel_color = wheel_color

    def draw(self, x, y):
        bottom_x = x + self.w
        bottom_y = y + self.h
        r = self.w/4
        canvas.create_rectangle(
            x, y, bottom_x, bottom_y,
            outline=self.body_color, fill=self.body_color
            )
        canvas.create_oval(
            x + self.w/4 - self.wh, bottom_y - self.wh,
            x + self.w/4 + self.wh, bottom_y + self.wh,
            outline=self.wheel_color, fill=self.wheel_color
            )
        canvas.create_oval(
            x + 3*self.w/4 - self.wh, bottom_y-self.wh,
            x + 3*self.w/4 + self.wh, bottom_y+self.wh,
            outline=self.wheel_color, fill=self.wheel_color
            )

tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=0, bg="whitesmoke")
canvas.pack()

cars = [
    Car(120, 50, 10, "blue", "gray"),
    Car(120, 70, 6, "red", "gray"),
    Car(80, 40, 12, "orange", "gray"),
    Car(60, 90, 14, "white", "gray")
    ]

x = 0
y = 100
PAD = 10
for car in cars:
    car.draw(x, y)
    x = x + car.w + PAD
