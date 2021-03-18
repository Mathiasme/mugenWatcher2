from tkinter import *

def create(infoWindowFrame):
    debugOutputArea = Text(infoWindowFrame, height = 250, width = 700)
    debugOutputArea.pack()
    infoWindowFrame.update()
    return debugOutputArea