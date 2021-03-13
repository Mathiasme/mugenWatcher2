from pymem import Pymem
import pymem.process
import os
import time
import subprocess
import random
import psutil
import glob

baseDir = os.getcwd()
#baseDir = r'C:\Users\Owner\Downloads\TC'
charsDir = baseDir + r'\chars'
players = os.listdir(charsDir)

stagesDir = baseDir + r'\stages'
os.chdir(stagesDir)
stages = glob.glob('*.def')
os.chdir(baseDir)

p1p = 0
p2p = 1

p1 = players[p1p]
p2 = players[p2p]

base_address = 0x00400000 # mugen.exe
win_address_offset = 0x001040E8 # offset for above, points to actual win address
red_offset = 0x0000871C # offset for win_address (not win_address_offset), points to P1 wins
blue_offset = 0x00008728 # offset for win_address (not win_address_offset), points to P2 wins

while True:

    stage = random.choice(stages)
    stageCharacterLength = len(stage)
    stage = stage[0:stageCharacterLength - 4] # removes 4 char file extension

    #os.chdir("C:\\Users\\Owner\\Downloads\\TC\\")
    subprocess.Popen("TC.exe -p1 \"" + p1 + "\" -p2 \"" + p2 +"\"" + "-rounds 2 -p1.life 1200 -p2.life 1200 -p1.ai 9 -p2.ai 9 -s \"" + stage + "\"")

    time.sleep(1)
    pm = pymem.Pymem("TC.exe")
    print(p1 + ' - vs - ' + p2)
    pid = pm.process_id

    win_address = pm.read_int(base_address + win_address_offset)
    p1_win_address = win_address + red_offset
    p2_win_address = win_address + blue_offset

    P1Wins = 0
    P2Wins = 0

    while psutil.pid_exists(pid):
        time.sleep(0.5)
        try:
            temp = pm.read_int(p1_win_address)
            temp2 = pm.read_int(p2_win_address)
            if temp != P1Wins and temp <= 2:
                print('p1 wins round')
                P1Wins = temp
            if temp2 != P2Wins and temp2 <= 2:
                print('p2 wins round')
                P2Wins = temp2
        except:
            continue
    
    print(str(P1Wins) + ' : ' + str(P2Wins))
    if P1Wins == P2Wins:
        print('Tie! Rematch!')
    elif P1Wins > P2Wins:
        print(p1 + ' wins')
        if p1p < p2p:
            p2p += 1
            p2 = players[p2p]
        elif p2p < p1p:
            p2p = p1p + 1
            p2 = players[p2p]
    else:
        print(p2 + ' wins')
        if p1p < p2p:
            p1p = p2p + 1
            p1 = players[p1p]
        elif p2p < p1p:
            p1p += 1
            p1 = players[p1p]
    print('')

