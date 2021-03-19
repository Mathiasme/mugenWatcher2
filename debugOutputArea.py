import tkinter as tk
import tkinter.scrolledtext as tkscrolled

def create(infoWindowFrame):
    debugOutputArea = tkscrolled.ScrolledText(infoWindowFrame)
    debugOutputArea.grid(row = 0, column = 1)
    infoWindowFrame.update()
    return debugOutputArea