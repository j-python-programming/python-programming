# Python によるプログラミング：第 2 章
#    例題 2.2 壁の導入
# --------------------------
# プログラム名: 02-ball-2.py

from tkinter import *
import time

DURATION = 0.001   # sleep 時間 = 描画の間隔
STEPS = 600        # ボールを書き直す回数
Y = 200            # ボールの Y 初期値
D = 10             # ボールの直径

# 壁を描画する関数の定義
def make_walls(ox, oy, width, height):
    canvas.create_rectangle(ox, oy, ox + width, oy + height)

tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()
tk.update()

x = 150            # ボールの X 初期値
vx = 2             # ボールの移動量

make_walls(100, 100, 600, 400)  # 実際にここで壁を描画
id = canvas.create_rectangle(x, Y, x + D, Y + D,
                             fill="darkblue", outline="black")
                   # 四角 ( ボール ) を描画して、その id( 識別子 ) を取得する。
for s in range(STEPS):
    x = x + vx          # x 座標の値を変える
    if x + D >= 700:
        # もしボールの右端が 700 を越えたら、
        vx = -vx        # 向きを反転させる
    canvas.coords(id, x, Y, x + D, Y + D)  # 新しい座標を設定
    tk.update()             # 描画が画面に反映される。
    time.sleep(DURATION)    # 次に描画するまで、 sleep する。

