import tkinter

def create(infoWindowFrame):
    fightHistoryArea = tkinter.Text(infoWindowFrame)
    fightHistoryArea.grid(row = 0, column = 0)
    infoWindowFrame.update()
    return fightHistoryArea