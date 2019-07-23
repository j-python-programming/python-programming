# Python によるプログラミング：第 6 章
#  例題 6.5 Polymorphism
# --------------------------
# プログラム名: 06-area-1.py

from dataclasses import dataclass, field

@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)
    def __post_init__(self):
        self.area = self.width * self.height

@dataclass
class Circle:
    radius: float
    area: float = field(init=False)
    def __post_init__(self):
        self.area = 3.14 * self.radius * self.radius

shapes = [Rectangle(3, 4), Circle(5)]
for shape in shapes:
    print("面積: {}".format(shape.area))
