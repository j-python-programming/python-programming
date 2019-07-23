# Python によるプログラミング：第 2 章　
# 練習問題 2.1 「車」を動かす
# --------------------------
# プログラム名: ex02-1-cars.py

from tkinter import *
from dataclasses import dataclass
import time

# 初期データ
DURATION = 0.01    # sleep時間=描画の間隔
STEPS = 20000      # コマ数
RIGHT = 700        # 右側の「折り返し」位置
LEFT = 100         # 左側の「折り返し」位置

@dataclass
class Car:
    ids: list
    x: int
    y: int
    l: int
    h: int
    wr: int
    vx: int
    bcolor: str

# 自動車を初期位置に描画する。
def make_car(x, y, l, h, wr, vx, bcolor):
    #　座標の0,0,0,0は、ダミーの値
    id0 = canvas.create_rectangle(0, 0, 0, 0,
                                  fill=bcolor, outline=bcolor)
    id1 = canvas.create_oval(0, 0, 0, 0,
                             fill="black", outline="black")
    id2 = canvas.create_oval(0, 0, 0, 0,
                             fill="black", outline="black")
    ids = [id0, id1, id2]
    return Car(ids, x, y, l, h, wr, vx, bcolor)

# 自動車の動き
def move_car(car):
  car.x += car.vx

# 自動車の再描画
def redraw_car(car):
    ids = car.ids
    x = car.x
    y = car.y
    l = car.l       # 車の長さ
    h = car.h       # 車の高さ
    wr = car.wr     # タイヤの半径
    wh_1_x = x + l/4 - wr    # 前輪の中心は、全体の1/4の位置とする
    wh_2_x = x + 3*l/4 - wr  # 後輪の中心は、全体の3/4の位置とする
    wh_y = y + h - wr
    canvas.coords(ids[0], x, y, x + l, y + h)
    canvas.coords(ids[1], wh_1_x, wh_y, wh_1_x + 2*wr, wh_y + 2*wr)
    canvas.coords(ids[2], wh_2_x, wh_y, wh_2_x + 2*wr, wh_y + 2*wr)

# プログラム本文
tk=Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()
tk.update()

# 車のデータ
cars = [
    make_car(150, 100, 100, 50, 10, 1, "blue"),
    make_car(200, 250, 100, 70, 5, 2, "red"),
    make_car(250, 400, 200, 40, 10, 1, "orange"),
    ]

# 全体のプログラムのループ
for s in range(STEPS):
    for car in cars:      # すべての車について反復
        # 左側が次に壁を抜けるか、
        if (car.x + car.vx <= LEFT \
           or car.x + car.l >= RIGHT):   # 右側が壁を抜けるなら、
           car.vx = -car.vx    # 移動方向を反転
        move_car(car)     # 車を動かす
        redraw_car(car)     # 描画を反映させる。
    tk.update()           # 描画が画面に反映される。
    time.sleep(DURATION)  # 次に描画するまで、sleepする。
