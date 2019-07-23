# Pythonによるプログラミング：第1章
#    例題 1.1  4軒の家(同じ家)
# --------------------------
# プログラム名: 01-house-13.py

from tkinter import *

def draw_house_at(x, y, w, h, roof_color, wall_color):
    rtop_x = x + w/2   # 家根のtop x
    wtop_y = y + h/2   # 壁のtop y
    bottom_x = x + w   # 家のbottom x
    bottom_y = y + h   # 家のbottom y
    # 三角形で家根を描く(三つの点の座標を指定する。)
    canvas.create_polygon(rtop_x, y,     # 頂点
                          x, wtop_y,     # 左下
                          x + w, wtop_y, # 右下
                          outline=roof_color, fill=roof_color)
    # 四角形で家を描く(左上と右下の座標を指定する。)
    canvas.create_rectangle(x, wtop_y, bottom_x, bottom_y,
                            outline=wall_color, fill=wall_color)

tk=Tk()
canvas = Canvas(tk, width=500, height=400, bd=0)
canvas.pack()

x0 = 0
W = 100
H = 150
PAD = 10
for x in range(4):
    draw_house_at(x0, 50, W, H, "red", "gray")
    x0 += W + PAD
