# Python によるプログラミング：第 2 章
# 練習問題 2.4 ウイルス感染のシミュレーション
# --------------------------
# プログラム名: ex02-2-epidemic.py

from tkinter import *
from dataclasses import dataclass
import time
import random      # この課題では、「乱数」を使用する。

# パラメータの初期化
NUM_PERSONS = 15   # 人の数を規定する
DURATION = 0.001
NORMAL_COLOR = "lightgray"
EPI_COLOR = "black"

@dataclass
class Person:
    id: int
    x: int
    y: int
    w: int
    h: int
    vx: int
    vy: int
    c: str

@dataclass
class Border:
    left: int
    right: int
    top: int
    bottom: int

# 人を描画し、生成されたdataclassを返す。
def make_person(x, y, w, h, vx, vy, c="black"):
    id = canvas.create_rectangle(x, y, x + w, y + h, fill=c, outline=c)
    return Person(id, x, y, w, h, vx, vy, c)

# 人を移動させる。
def move_person(person):
    person.x += person.vx
    person.y += person.vy

# 壁の描画  
def make_walls(ox, oy, width, height):
    canvas.create_rectangle(ox, oy, ox + width, oy + height)

# 人の再描画
def redraw_person(person):
    canvas.coords(person.id, person.x, person.y,
                  person.x + person.w, person.y + person.h)

# 「人々」を準備する。
def prepare_persons():
    for i in range(NUM_PERSONS):
        if i==0:      # 先頭のデータだけ「感染」とする
            c = EPI_COLOR
        else:
            c = NORMAL_COLOR
        w = random.randint(5, 10)   # 乱数を生成する。
        x = random.randint(border.left, border.right - w)
        h = random.randint(5, 10)
        y = random.randint(border.top, border.bottom - h)
        vx = random.randint(-3, 3)
        vy = random.randint(-3, 3)
        persons.append(make_person(x, y, w, h, vx, vy, c))

# 「人」と「人」とのコンタクトをチェック
# どちらかが感染していて、接触したなら「感染」
def check_contact(p1, p2):
    # 同じ「人」だったら、何もしない
    if p1.id == p2.id: return
    # 二人とも同じ状態だったら、チェックしない
    if p1.c == p2.c: return
    # X軸上も、Y軸上も、相手との「重なり」があることを判定
    if (p1.x < p2.x + p2.w \
        and p1.x + p1.w > p2.x \
        and p1.y < p2.y + p2.h \
        and p1.y + p2.h > p2.y):
        if p1.c == EPI_COLOR:
            p2.c = EPI_COLOR # 設定上の色を変える
            # 画面上の色を変える
            canvas.itemconfig(p2.id, fill=EPI_COLOR)
            canvas.itemconfig(p2.id, outline=EPI_COLOR)
        else:
            p1.c = EPI_COLOR # 設定上の色を変える
            # 画面上の色を変える
            canvas.itemconfig(p1.id, fill=EPI_COLOR)
            canvas.itemconfig(p1.id, outline=EPI_COLOR)

tk = Tk()
canvas = Canvas(tk, width=500, height=400, bd=0, bg="white")
canvas.pack()
tk.update()

persons = []  # 最初は空のリストとして用意し、生成した順に登録

# 壁の座標を与える。(left, right, top, bottom)
border = Border(100, 400, 100, 300)

make_walls(
    border.left,
    border.top,
    border.right - border.left,
    border.bottom - border.top
    )

prepare_persons()   # ここで、「人々」を初期設定する。
# 最初の一人に「感染」を色を変える。
canvas.itemconfig(persons[0].id, fill=EPI_COLOR)

while True:
    num_infected = 0
    for person in persons:  # 全ての人について、実施する。
        move_person(person)  # 人の移動
        if (person.x + person.vx < border.left \
            or person.x + person.w >= border.right):
            person.vx = -person.vx
        if (person.y + person.vy <  border.top \
            or person.y + person.h  >= border.bottom):
            person.vy = -person.vy
        for p in persons:  # 自分を含めた全員を「相手」としてチェック
            check_contact(p, person)  # 相手との接触確認
        redraw_person(person)
        if person.c == EPI_COLOR: # 感染者の数を数える
            num_infected = num_infected + 1
    tk.update()
    # もし、全員が感染していたら、終了
    if num_infected == NUM_PERSONS: break
    time.sleep(DURATION)
