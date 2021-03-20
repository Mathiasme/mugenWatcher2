import tkinter as tk

def create(infoWindowFrame):
    fightHistoryArea = tk.Text(infoWindowFrame, font="Helvetica 32 bold")
    fightHistoryArea.grid(row = 0, column = 0)
    infoWindowFrame.update()
    return fightHistoryArea