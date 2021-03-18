import tkinter

def create(infoWindowFrame):
    debugOutputArea = tkinter.Text(infoWindowFrame)
    debugOutputArea.grid(row = 0, column = 1)
    infoWindowFrame.update()
    return debugOutputArea