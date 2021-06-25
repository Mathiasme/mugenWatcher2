import os
import glob
import time

import infoWindowFrame as iwf
import fightHistoryArea as fha
import gameLoop as gl
import debugOutputArea as doa
import dbAccess as db

baseDir = os.getcwd()
#baseDir = r'C:\\Users\Owner\Downloads\TC'
os.chdir(baseDir) # simply setting our working directory explicitly. Unsure if this is needed.
charsDir = baseDir + r'\chars' # folder that holds all the fighter files
list = os.listdir(charsDir) # an array of all fighter names
#Allow for an access to characters .def files in folder (which was my default mugen configuration) 
#Avoid adding none-folder filenames to the list (such as the readme.txt)
players=[]
for i in list:
    if os.path.isdir(baseDir + r'\chars' + '\\' + i):
        players.append(i)  
numPlayers = len(players)

stagesDir = baseDir + r'\stages' # stages folder
os.chdir(stagesDir) # change our working directory temporarily to use glob
stages=[]
stagesList = glob.glob('*.def') # this gets all ".def" files in the stages folder
for stage in stagesList: #Take off ".def" extension to avoid "stage.def.def" output
    stages.append(os.path.splitext(stage)[0])
os.chdir(baseDir) # revert our working directory

p1i = 0 # player 1's array index
p2i = 1 # player 2's array index

base_address = 0x00400000 # mugen.exe
win_address_offset = 0x001040E8 # offset for above, points to actual win address
red_offset = 0x0000871C # offset for win_address (not win_address_offset), points to P1 wins
blue_offset = 0x00008728 # offset for win_address (not win_address_offset), points to P2 wins

# set our 1st two fighters
p1Name = players[p1i]
p2Name = players[p2i]

if __name__ == '__main__':
    infoWindowFrame = iwf.createFrame()
    fightHistoryArea = fha.create(infoWindowFrame)
    debugOutputArea = doa.create(infoWindowFrame)
    #db.dropTable(debugOutputArea)
    #db.createTable(debugOutputArea)
    for p in players:
        db.addNewChar(p, debugOutputArea)
    gl.start(stages, infoWindowFrame, fightHistoryArea, base_address, win_address_offset, red_offset, blue_offset, numPlayers, debugOutputArea)
