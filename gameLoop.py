import time
import subprocess
import pymem.process
import random
import sys
import psutil
import pymem
import tkinter as tk

import infoWindowFrame as iwf
import fightHistoryArea as fha
import dbAccess as db

def start(stages, infoWindowFrame, fightHistoryArea, base_address, win_address_offset, red_offset, blue_offset, numPlayers, debugOutputArea):

    # This loop advances only when the fighters change pairings
    # It picks a random stage, 
    # starts the fight, 
    # monitors the fight for the winner in an inner loop,
    # loser is eliminated, 
    # replacement fighter is chosen, 
    # loop advances
    while True:

        fightHistoryArea.delete(0.0, tk.END)

        p1Name = db.getRandChar(debugOutputArea)
        p2Name = db.getContender(p1Name, debugOutputArea)

        stage = random.choice(stages)

        # open our target process with the fight parameters
        subprocess.Popen("mugen.exe -p1 \"" + p1Name + "\" -p2 \"" + p2Name +"\"" + "-rounds 1 -p1.life 1200 -p2.life 1200 -p1.ai 9 -p2.ai 9 -s \"" + stage + "\"")

        time.sleep(1) # sleep for a second after opening the process before hooking in
        pm = pymem.Pymem("mugen.exe")
        pid = pm.process_id

        p1Elo = db.getCharScore(p1Name, debugOutputArea)
        p2Elo = db.getCharScore(p2Name, debugOutputArea)
        p1ChanceOfWinning = (1.0 / (1.0 + pow(10, ((p2Elo - p1Elo) / 400))))
        p2ChanceOfWinning = (1.0 / (1.0 + pow(10, ((p1Elo - p2Elo) / 400))))

        fightHistoryArea.insert(tk.END, p1Name + '\n')
        fightHistoryArea.insert(tk.END, 'Elo: ' + str(p1Elo) + ' | ' + str(int(p1ChanceOfWinning * 100)) + '%\n')
        fightHistoryArea.insert(tk.END, ' - vs - ' + '\n')
        fightHistoryArea.insert(tk.END, p2Name + '\n')
        fightHistoryArea.insert(tk.END, 'Elo: ' + str(p2Elo) + ' | ' + str(int(p2ChanceOfWinning * 100)) + '%\n')
        fightHistoryArea.see(tk.END)
        
        # calculating our addresses, win_address changes each time mugen.exe is re-run (after every matchup)
        win_address = pm.read_int(base_address + win_address_offset)
        p1_win_address = win_address + red_offset
        p2_win_address = win_address + blue_offset

        # before each fight set each fighters wins to zero
        P1Wins = 0
        P2Wins = 0

        # every 0.5 seconds check to see if the mugen process is running
        # if it's not running, that means the fight is over beacuse
        # mugen auto closes itself after a fight completes
        while True:
            # try to read values from memory.
            # target process can close at any time, so wrap it in try
            try:
                temp = pm.read_int(p1_win_address)
                temp2 = pm.read_int(p2_win_address)         
                if temp != P1Wins and temp <= 2 and temp != 0: # if we successfully read both values, let's save them
                    db.updateCharScore(p1Name, p2Name, debugOutputArea, fightHistoryArea)
                    P1Wins = temp
                if temp2 != P2Wins and temp2 <= 2 and temp2 != 0:
                    db.updateCharScore(p2Name, p1Name, debugOutputArea, fightHistoryArea)
                    P2Wins = temp2
            except Exception as e:
                print(e)
                break
            try:  
                infoWindowFrame.update()
            except:
                p = psutil.Process(pid)
                p.terminate()  #or p.kill()
                sys.exit()
            time.sleep(0.5) # sleep 0.5 seconds
        
        # Printing fight results after a winner is determined
        # Below is the logic for eliminating the loser and finding a replacement
        # We just keep sliding the pointer indexes to the right, going through every character
        # If the index of the new fighter is >= the number of players, terminate program
        fightHistoryArea.insert(tk.END, str(P1Wins) + ' : ' + str(P2Wins) + '\n')
        if P1Wins == P2Wins:
            fightHistoryArea.insert(tk.END, 'Tie!' + '\n')
        elif P1Wins > P2Wins: 
            fightHistoryArea.insert(tk.END, p1Name + ' wins' + '\n')
        else:
            fightHistoryArea.insert(tk.END, p2Name + ' wins' + '\n')
        fightHistoryArea.insert(tk.END, '--------------\n\n\n') # a spacer to make things more readable between fights, we now loop back to start a new fight
        fightHistoryArea.see(tk.END)