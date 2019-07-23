# Pythonによるプログラミング：第1章
#    練習問題 1-1 (2)
# --------------------------
# プログラム名: ex01-car-2.py

from tkinter import *

# 車を描画するメソッド
def draw_car_at(x, y, w, h, wheel, body_color, wheel_color):
    # 車体
    bottom_x = x + w
    bottom_y = y + h
    canvas.create_rectangle(x, y, bottom_x, bottom_y,
                            outline=body_color, fill=body_color)
    # 左側の車輪
    wheel1_top_x = x + w/4 - wheel  # 中心は、左側1/4の位置
    wheel1_top_y = y + h - wheel
    wheel1_bottom_x = x + w/4 + wheel
    wheel1_bottom_y = y + h + wheel
    canvas.create_oval(wheel1_top_x, wheel1_top_y,
                       wheel1_bottom_x, wheel1_bottom_y,
                       outline=wheel_color, fill=wheel_color)
    # 右側の車輪
    wheel2_top_x = x + 3*w/4 - wheel  # 中心は、左から3/4の位置
    wheel2_top_y = y + h - wheel
    wheel2_bottom_x = x + 3*w/4 + wheel
    wheel2_bottom_y = y + h + wheel
    canvas.create_oval(wheel2_top_x, wheel2_top_y,
                       wheel2_bottom_x, wheel2_bottom_y,
                       outline=wheel_color, fill=wheel_color)

tk=Tk()
canvas = Canvas(tk, width=500, height=400, bd=0, bg="whitesmoke")
canvas.pack()

draw_car_at(0, 100, 120, 50, 10, "blue", "gray")
draw_car_at(140, 100, 120, 70, 6, "red", "gray")
draw_car_at(280, 100, 80, 40, 12, "orange", "gray")
draw_car_at(380, 100, 60, 90, 14, "white", "gray")
