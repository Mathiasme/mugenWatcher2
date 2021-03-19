import mysql.connector
import fightHistoryArea as fha
import tkinter as tk

def dropTable(debugOutputArea):
    mydb = mysql.connector.connect(
        host="localhost",
        user="mugenmaster",
        password="mastermugenpassword",
        database="mugen"
    )

    mycursor = mydb.cursor()
    mycursor.execute("DROP TABLE chars;")
    mydb.commit()
    debugOutputArea.insert(tk.END, "Dropped Table `chars`\n")

def createTable(debugOutputArea):
    mydb = mysql.connector.connect(
        host="localhost",
        user="mugenmaster",
        password="mastermugenpassword",
        database="mugen"
    )

    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE chars(name varchar(255), elo int);")
    mydb.commit()
    debugOutputArea.insert(tk.END, "Created Table `chars`\n")

def addNewChar(charName, debugOutputArea):
    mydb = mysql.connector.connect(
        host="localhost",
        user="mugenmaster",
        password="mastermugenpassword",
        database="mugen"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM chars WHERE name = '" + charName + "';")
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
        mycursor.execute("INSERT INTO chars (name, elo) VALUES ('" + charName + "', 1500);")
        mydb.commit()
        debugOutputArea.insert(tk.END, 'Added New Character: ' + charName + '\n')
    return myresult

def getRandChar(debugOutputArea):
    mydb = mysql.connector.connect(
        host="localhost",
        user="mugenmaster",
        password="mastermugenpassword",
        database="mugen"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM chars ORDER BY RAND() LIMIT 1;")
    char = mycursor.fetchall()
    debugOutputArea.insert(tk.END, 'Randomly Picked: ' + char[0][0] + '\n')
    debugOutputArea.see(tk.END)
    return char[0][0]

def getContender(charName, debugOutputArea):
    mydb = mysql.connector.connect(
        host="localhost",
        user="mugenmaster",
        password="mastermugenpassword",
        database="mugen"
    )

    score = getCharScore(charName, debugOutputArea)

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM chars WHERE elo <= " + str(score + 200) + " AND elo >= " + str(score - 200) + " AND name != '" + charName + "' ORDER BY RAND() LIMIT 1;")
    char = mycursor.fetchall()
    debugOutputArea.insert(tk.END, 'Randomly Picked: ' + char[0][0] + ' with bounds of ' + str(score + 200) + "," + str(score - 200) + '\n')
    debugOutputArea.see(tk.END)
    return char[0][0]

def getCharScore(charName, debugOutputArea):
    mydb = mysql.connector.connect(
        host="localhost",
        user="mugenmaster",
        password="mastermugenpassword",
        database="mugen"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT elo FROM chars WHERE name = '" + charName + "';")
    myresult = mycursor.fetchall()
    numResults = len(myresult)
    debugOutputArea.insert(tk.END, 'Searched for score for ' + charName + ', numResults: ' + str(numResults) + '\n')
    debugOutputArea.see(tk.END)

    if numResults == 0:
        addNewChar(charName, debugOutputArea)
        return 1500
    else:
        return myresult[0][0]

def updateCharScore(winner, loser, debugOutputArea, fightHistoryArea):
    mydb = mysql.connector.connect(
        host="localhost",
        user="mugenmaster",
        password="mastermugenpassword",
        database="mugen"
    )

    K = 32
    mycursor = mydb.cursor()
    winnerScore = getCharScore(winner, debugOutputArea)
    loserScore = getCharScore(loser, debugOutputArea)
    winnerNewScore = winnerScore + K*(1 - 0)
    loserNewScore = loserScore + K*(0 - 1)

    mycursor.execute("UPDATE chars SET elo = " + str(winnerNewScore) + " WHERE name = '" + winner  + "';")
    mydb.commit()
    mycursor.execute("UPDATE chars SET elo = " + str(loserNewScore) + " WHERE name = '" + loser  + "';")
    mydb.commit()

    fightHistoryArea.insert(tk.END, winner + ' +' + str((winnerNewScore - winnerScore)) + '\n')
    fightHistoryArea.insert(tk.END, loser + ' ' + str((loserNewScore - loserScore)) + '\n')
    fightHistoryArea.see(tk.END)

    debugOutputArea.insert(tk.END, 'Updating Scores\n')
    debugOutputArea.insert(tk.END, winner + " oldScore:newScore" + str(winnerScore) + ":" + str(winnerNewScore) + '\n')
    debugOutputArea.insert(tk.END, loser + " oldScore:newScore" + str(loserScore) + ":" + str(loserNewScore) + '\n')
    debugOutputArea.see(tk.END)

    return True