# Python によるプログラミング：第 2 章　
#    例題 2.3  ボールと壁
# (3) 複数のボール
# --------------------------
# プログラム名: 02-ball-5.py

from tkinter import *
from dataclasses import dataclass
import time

# パラメータは、１か所にまとめておく。
DURATION = 0.001    # sleep 時間 = 描画の間隔

@dataclass
class Ball:
    id: int
    x: int
    y: int
    d: int
    vx: int
    c: str

@dataclass
class Border:
    left: int
    right: int
    top: int
    bottom: int

# ボールを初期位置に描画し、生成された「辞書」を返す。
# 直径 d は、省略されたら 3 に、色 c は、省略されたら "black" になる
def make_ball(x, y, d=3, vx=2, c="black"):
    id = canvas.create_rectangle(x, y, x + d, y + d,
                                 fill=c, outline=c)
    return Ball(id, x, y, d, vx, c)

# ボールの移動を、プログラム本体から抜き出した。
def move_ball( ball ):
    ball.x = ball.x + ball.vx

# 壁を描画する関数の定義
def make_walls(ox, oy, width, height):
    canvas.create_rectangle(ox, oy, ox + width, oy + height)

# ボールを再描画する関数。coords をラップしている。
def redraw_ball(ball):
    d = ball.d
    canvas.coords(ball.id, ball.x, ball.y,
                  ball.x + d, ball.y + d)

tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()
tk.update()

# 壁の座標を与える。(left, right, top, bottom)
border = Border(100, 700, 100, 500)

# 初期化処理
make_walls(
    border.left,
    border.top,
    border.right - border.left,
    border.bottom - border.top
    )

# 複数のボールを「リスト」として準備する。
balls = [
    make_ball(100, 150, 20, 2, "darkblue"),
    make_ball(200, 250, 25, -4, "orange"),
    make_ball(300, 350, 10, -2, "green"),
    make_ball(400, 450, 5, 4, "darkgreen")
    ]

while True:
    for ball in balls:   # すべてのボールに、処理を反復
        move_ball( ball )   # まず、ボールを移動させる
        # ボールが壁に当たるなら、
        if (ball.x + ball.vx < border.left \
            or ball.x + ball.d  >= border.right):
            ball.vx = - ball.vx    # ボールの移動方向を反転させる
        redraw_ball( ball )  # ボール移動の描画
    tk.update()              # 描画が画面に反映される。
    time.sleep(DURATION)     # 次に描画するまで、sleep する。
