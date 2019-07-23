import turtle

class CustomPen(turtle.Pen):
    def triangle(self, size):
        for x in range(3):
            self.forward(size)
            self.left(120)

t = CustomPen()
t.triangle(50)
