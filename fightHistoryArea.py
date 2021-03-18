from tkinter import *

def create(infoWindowFrame):
    fightHistoryArea = Text(infoWindowFrame, height = 250, width = 700)
    fightHistoryArea.pack()
    infoWindowFrame.update()
    return fightHistoryArea