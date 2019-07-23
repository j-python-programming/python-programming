# Pythonによるプログラミング：第1章
#    発展問題 1-4
# --------------------------
# プログラム名: ex01-taylor.py

from tkinter import *
import math

OX = 400    # (OX, OY)がキャンバス上での原点の位置
OY = 300
MAX_X = 800  # 座標軸の最大(キャンバス座標)
MAX_Y = 600
SCALE_X = 20 # キャンバス座標への変換係数
SCALE_Y = 20

N = 30

START = -4*math.pi
END = 4*math.pi
DELTA = 0.05

def draw_point(x, y, r=1, c="black"):
    canvas.create_oval(x - r, y - r, x + r, y + r, fill=c, outline=c)

def make_axes(ox, oy, width, height):
    canvas.create_line(0, oy, width, oy)
    canvas.create_line(ox, 0, ox, height)

def plot(x, y, r=1, c="black"):
    draw_point(SCALE_X * x + OX, OY - SCALE_Y * y, r, c)

def taylor_param(x, n):
    if(n > 0):
        # 再帰的な呼出しを行なう
        p = taylor_param(x, n - 1)
        param[n] = x * p / n
        return param[n]
    else:
        param[n] = 1
        return param[0]

def taylor_sin(x, n):
  s = 0;
  taylor_param(x, n)
  for i in range(n + 1):
    s += mult[i % 4] * param[i]
  return s

tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()

mult = (0, 1, 0, -1) # 要素数4のタプル：変更の必要がない
param = [1] * N  # 要素数Nのリストを、1で初期化

make_axes(OX, OY, MAX_X, MAX_Y)

c = ["black", "blueviolet", "black", "darkblue", "black", "navy",
     "black", "blue", "black", "darkgreen",  "black", "green",
     "black", "yellow", "black", "magenta", "black", "red",
     "black", "darkred", "black", "cyan", "black", "darkmagenta",
     "black", "darkred", "black", "darkcyan", "black", "darkmagenta"
     ]

for n in range(1, N, 2):
    x = START
    while x < END:
        v = taylor_sin(x, n)
        plot(x, v, 1, c[n])
        x = x + DELTA
