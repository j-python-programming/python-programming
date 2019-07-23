# Python によるプログラミング：第 6 章
#  例題 6.6 Polymorphism
# --------------------------
# プログラム名: 06-area.py

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.area = width * height

class Circle:
    def __init__(self, radius):
        self.radius = radius
        self.area = 3.14 * radius * radius

shapes = [Rectangle(3, 4), Circle(5)]
for shape in shapes:
    print("面積: {}".format(shape.area))
