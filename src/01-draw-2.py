# Python によるプログラミング：第 1 章
#    例題 1-4 (2) y = x * x のプロット
# --------------------------
# プログラム名: 01-draw-1.py

from tkinter import *
import math

def draw_point(x, y, r=1, c="black"):
    canvas.create_oval(x - r, y - r, x + r, y + r,
                       fill=c, outline=c)

def f(x):
    return x * x

tk = Tk()
canvas = Canvas(tk, width=1000, height=800, bd=0)
canvas.pack()

for x in range(0, 800):
    draw_point(x, f(x))
