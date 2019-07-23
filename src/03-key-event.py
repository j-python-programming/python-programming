# Python によるプログラミング：第 3 章
#    例題 3.1 Key が押された時、 keysym を表示
# --------------------------
# プログラム名: 03-key-event.py

from tkinter import *
tk = Tk()
canvas = Canvas(tk, width=400, height=300)
canvas.pack()

# Key Event Handler
def on_key_press(event):
    # 文字を表示する。
    print("key: {}".format(event.keysym))

# イベントハンドラとイベントを結びつける。
canvas.bind_all("<KeyPress>", on_key_press)
