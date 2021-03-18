from tkinter import *

def create(infoWindowFrame):
    debugOutputArea = Text(infoWindowFrame)
    debugOutputArea.grid(row = 0, column = 1)
    infoWindowFrame.update()
    return debugOutputArea