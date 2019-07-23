# Python によるプログラミング：第 2 章
#    例題 2.1 動きのプログラミング
# --------------------------
# プログラム名: 02-ball-1.py

from tkinter import *
import time

DURATION = 0.001   # sleep 時間 = 描画の間隔
X_RIGHT = 400      # x の最大値
X = 0              # ボールの X 初期値
Y = 100            # ボールの Y 初期値
D = 10             # ボールの直径

tk = Tk()
canvas = Canvas(tk, width=600, height=400, bd=0)
canvas.pack()
tk.update()

id = canvas.create_rectangle(X, Y, X + D, Y + D,
                             fill="darkblue", outline="black")
                   # 四角を描画して、その id( 識別子 ) を取得する。
for x in range(X, X_RIGHT):
    canvas.coords(id, x, Y, x + D, Y + D)  # 「新しい座標」を設定
    tk.update()             # 描画が画面に反映される。
    time.sleep(DURATION)    # 次に描画するまで、sleep する。
