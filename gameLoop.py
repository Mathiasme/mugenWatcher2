from pymem import Pymem
from tkinter import *

import time
import subprocess
import pymem.process
import random
import logging
import sys

import infoWindowFrame as iwf
import fightHistoryArea as fha

def start(p1Name, p2Name, stages, p1i, p2i, infoWindowFrame, fightHistoryArea, base_address, win_address_offset, red_offset, blue_offset, numPlayers, players):

    # This loop advances only when the fighters change pairings
    # It picks a random stage, 
    # starts the fight, 
    # monitors the fight for the winner in an inner loop,
    # loser is eliminated, 
    # replacement fighter is chosen, 
    # loop advances
    while True:

        stage = random.choice(stages)

        # open our target process with the fight parameters
        subprocess.Popen("mugen.exe -p1 \"" + p1Name + "\" -p2 \"" + p2Name +"\"" + "-rounds 2 -p1.life 1200 -p2.life 1200 -p1.ai 9 -p2.ai 9 -s \"" + stage + "\"")

        time.sleep(1) # sleep for a second after opening the process before hooking in
        pm = pymem.Pymem("mugen.exe")

        logging.debug(p1Name + ' - vs - ' + p2Name)
        fightHistoryArea.insert(END, p1Name + ' - vs - ' + p2Name)

        # calculating our addresses
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
                    logging.debug(p1Name + ' wins round')                
                    P1Wins = temp
                if temp2 != P2Wins and temp2 <= 2 and temp2 != 0:
                    logging.debug(p2Name + ' wins round')                
                    P2Wins = temp2
            except:
                logging.debug(sys.exc_info()[0])
                break
            infoWindowFrame.update()
            time.sleep(0.5) # sleep 0.5 seconds
        
        # Printing fight results after a winner is determined
        # Below is the logic for eliminating the loser and finding a replacement
        # We just keep sliding the pointer indexes to the right, going through every character
        # If the index of the new fighter is >= the number of players, terminate program
        logging.debug(str(P1Wins) + ' : ' + str(P2Wins))
        if P1Wins == P2Wins:
            logging.debug('Tie! Rematch!')        
        elif P1Wins > P2Wins: 
            logging.debug(p1Name + ' wins')
            fightHistoryArea.insert(END, ' --- ' + str(P1Wins) + ':' + str(P2Wins) + '\n')
            if p1i < p2i:
                p2i += 1
                if p2i >= numPlayers:
                    logging.debug('Done!')                
                    exit
                p2Name = players[p2i]
            elif p2i < p1i:
                p2i = p1i + 1
                if p2i >= numPlayers:
                    logging.debug('Done!')                
                    exit
                p2Name = players[p2i]
        else:
            logging.debug(p2Name + ' wins')
            fightHistoryArea.insert(END, ' - ' + str(P1Wins) + ':' + str(P2Wins) + '\n')
            if p1i < p2i:
                p1i = p2i + 1
                if p1i >= numPlayers:
                    logging.debug('Done!')                
                    exit
                p1Name = players[p1i]
            elif p2i < p1i:
                p1i += 1
                if p1i >= numPlayers:
                    logging.debug('Done!')                
                    exit
                p1Name = players[p1i]
        logging.debug('--------------') # a spacer to make things more readable between fights, we now loop back to start a new fight