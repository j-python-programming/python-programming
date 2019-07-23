# Python によるプログラミング：第 2 章　
# 練習問題 2.1 「車」を動かす
# エラーの例
# --------------------------
# プログラム名: ex02-1-cars-err.py

from tkinter import *
from dataclasses import dataclass
import time

# 初期データ
DURATION = 0.01    # sleep時間=描画の間隔
steps = 20000      # コマ数
RIGHT = 700        # 右側の「折り返し」位置
LEFT = 100         # 左側の「折り返し」位置

@dataclass
class Car:
    x: int
    y: int
    l: int
    h: int
    wr: int
    vx: int
    c: str

# 個々の自動車を生成する。「辞書」を返す。
def create_car(x, y, l, h, wr, bcolor):
    canvas.create_rectangle(x, y, x + l, y + h,
                            fill=bcolor, outline=bcolor)
    wh_1_x = x + l/4 - wr      # 前輪の中心は、全体の1/4の位置とする
    wh_2_x = x + 3*l/4 - wr  # 後輪の中心は、全体の3/4の位置とする
    wh_y = y + h - wr
    canvas.create_oval(wh_1_x, wh_y, wh_1_x + 2*wr,  wh_y + 2*wr,
                       fill="black", outline="black")
    canvas.create_oval(wh_2_x, wh_y, wh_2_x + 2*wr, wh_y + 2*wr,
                       fill="black", outline="black")

tk=Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()
tk.update()

# 車のデータ
cars = [
    Car(150, 100, 100, 50, 10, 1, "blue"),
    Car(200, 250, 100, 70, 5, 2, "red"),
    Car(250, 400, 200, 40, 10, 1, "orange")
    ]

# 全体のプログラムのループ
for s in range(steps):
    for car in cars:      # すべての車について反復
        # 左側が次に壁を抜けるか、
        if (car.x + car.vx <= LEFT \
            or car.x + car.l >= RIGHT):   # 右側が壁を抜けるなら、
            car.vx = -car.vx    # 移動方向を反転
        car.x = car.x + car.vx
        create_car(car.x, car.y, car.l, car.h, car.wr, car.c)
    tk.update()           # 描画が画面に反映される。
    time.sleep(DURATION)  # 次に描画するまで、sleepする。

