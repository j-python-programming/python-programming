# Python によるプログラミング：第 1 章
#    例題 1.1 「家」
# --------------------------
# プログラム名: 01-house-11.py

from tkinter import *

tk=Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

canvas.create_polygon(100, 100, 0, 200, 200, 200,
                      outline="red", fill="red")
canvas.create_rectangle(0, 200, 200, 300,
                        outline="gray", fill="gray")
