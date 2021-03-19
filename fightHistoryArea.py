import tkinter as tk
import tkinter.scrolledtext as tkscrolled

def create(infoWindowFrame):
    fightHistoryArea = tkscrolled.ScrolledText(infoWindowFrame)
    fightHistoryArea.grid(row = 0, column = 0)
    infoWindowFrame.update()
    return fightHistoryArea