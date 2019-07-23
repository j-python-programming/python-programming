# Pythonによるプログラミング：第1章
#    練習問題 1-1 (1)
# --------------------------
# プログラム名: ex01-car-1.py

from tkinter import *

tk=Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

# 車体部分を描画する
canvas.create_rectangle(0, 0, 400, 200,
                        outline="black", fill="blue")
# 左のタイヤ
canvas.create_oval(60, 170, 120, 230,
                   outline="black", fill="gray")
# 右のタイヤ
canvas.create_oval(280, 170, 340, 230,
                   outline="black", fill="gray")
