from tkinter import *

def create(infoWindowFrame):
    fightHistoryArea = Text(infoWindowFrame)
    fightHistoryArea.grid(row = 0, column = 0)
    infoWindowFrame.update()
    return fightHistoryArea