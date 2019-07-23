import turtle

class CustomPen(turtle.Pen):
    def goto(self, x, y):
        self.up()
        super().goto(x, y)
        self.down()

t = CustomPen()
t.forward(100)
t.goto(0, 100)
t.forward(100)
