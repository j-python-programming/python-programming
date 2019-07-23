# Pythonによるプログラミング：第1章
#    練習問題 1-1 (3)
# --------------------------
# プログラム名: ex01-car-3.py

from tkinter import *
from dataclasses import dataclass

@dataclass
class Car:
    length: int
    height: int
    wd: int
    body_color: str
    wheel_color: str

def draw_car_at(x, y, length, height, wd, body_color, wheel_color):
    bottom_x = x + length
    bottom_y = y + height
    canvas.create_rectangle(x, y, bottom_x, bottom_y,
                            outline=body_color, fill=body_color)
    canvas.create_oval(x + length/4 - wd, bottom_y - wd,
                       x + length/4 + wd, bottom_y + wd,
                       outline=wheel_color, fill=wheel_color)
    canvas.create_oval(x + 3*length/4 - wd, bottom_y - wd,
                       x + 3*length/4 + wd, bottom_y + wd,
                       outline=wheel_color, fill=wheel_color)

def draw_car(car, x, y):
    length = car.length
    height = car.height
    wd = car.wd
    body_color = car.body_color
    wheel_color = car.wheel_color
    draw_car_at(x, y, length, height, wd, body_color, wheel_color)

tk=Tk()
canvas = Canvas(tk, width=500, height=400, bg="whitesmoke")
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
    draw_car(car, x, y)
    x += car.length + PAD
