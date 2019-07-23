from tkinter import Tk, Canvas

class CustomCanvas(Canvas):
    def __init__(self):
        Canvas.__init__(self, tk, width=300, height=300, bg="white")
        self.pack()

tk = Tk()
canvas = CustomCanvas()
canvas.create_line(100, 100, 200, 200)
