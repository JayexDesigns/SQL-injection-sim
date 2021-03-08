#imports
from string import ascii_lowercase, digits
from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from time import sleep
import threading
import sqlite3
import os

#file path
path=os.path.realpath(__file__)
path = path.split("\\")
folder = ""
file = ""
for i in range(len(path)):
    if i == len(path) - 1:
        file = path[i]
    else:
        folder += path[i] + "\\"
os.chdir(folder)

#connect with the SQL database
dbconn = sqlite3.connect("database.db")
db = dbconn.cursor()



#<===FUNCTIONING===>

#create the database
def createDatabase():
    db.execute("""CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
        );""")
    db.execute(f"""INSERT INTO users VALUES (
        1, 'Admin', '1234'
        );""")
    db.execute(f"""INSERT INTO users VALUES (
        2, 'Joe Doe', 'abcd'
        );""")
    db.execute(f"""INSERT INTO users VALUES (
        3, 'Jane Doe', 'hola'
        );""")
    dbconn.commit()

#get the username from the database
def getUser():
    username = usernameEntry.get()
    password = passwordEntry.get()
    db.execute(f"SELECT username FROM users WHERE username='{username}' and password='{password}';")
    name = db.fetchone()
    if name == None:
        outputVar.set("Username or Password not valid")
    else:
        outputVar.set(f"Welcome {name[0]}")

#changes the output label color, don't look at this I'm stupid and this is inefficient
def changeColor():
    color = ""
    while True:
        for i in range(60, 510-60):
            if i > 255:
                i = 510 - i

            color = "{:0>2s}".format(str(hex(i))[2:])*3

            sleep(0.003)
            outputLabel.config(fg=f"#{color}", activeforeground=f"#{color}")

colorThread = threading.Thread(target=changeColor)



#<===GUI===>

#color variables
black = "#101010"
gray = "#1a1a1a"
lightgray = "#999999"
white = "#ffffff"
pink = "#ff0066"
green = "#00ffaa"
purple = "#7b00ff"
back = gray
secondary = black
main = white
accent = pink

#create tkinter
root = Tk()

#change title, icon and background of the gui
root.title("SQL Injection Simulator")
root.iconbitmap("assets/icon.ico")
root.resizable(False, False)
root.configure(bg=back)

#center the window on the screen
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
root.geometry(f"302x289+{(screenWidth//2)-(302//2)}+{(screenHeight//2)-(289//2)}")

#convert units to pixels
pixelVirtual = PhotoImage(width=1, height=1)

#add the nexa font
nexaBold = Font(family="Nexa-Bold", size=15)
nexaRegular = Font(family="Nexa-Regular", size=12)

#username
usernameLabel = Label(root, text="Username:", bg=back, fg=accent, font=nexaRegular).grid(row=0, column=0, padx=(40, 10), pady=(40, 10))

usernameEntry = Entry(root, width=10, bg=secondary, fg=main, borderwidth=0, insertbackground=main, font=nexaRegular)
usernameEntry.insert(END, "'or '' = '")
usernameEntry.grid(row=0, column=1, padx=(10, 40), pady=(40, 10))

#password
passwordLabel = Label(root, text="Password:", bg=back, fg=accent, font=nexaRegular).grid(row=1, column=0, padx=(40, 10), pady=(10, 15))

passwordEntry = Entry(root, width=10, bg=secondary, fg=main, borderwidth=0, insertbackground=main, font=nexaRegular)
passwordEntry.insert(END, "'or '' = '")
passwordEntry.grid(row=1, column=1, padx=(10, 40), pady=(10, 15))

#submit
submit = Button(root, text="Submit", command=getUser, image=pixelVirtual, compound="c", width=100, height=50, bg=secondary, fg=main, activebackground=back, activeforeground=main, borderwidth=0, font=nexaBold).grid(row=2, column=0, columnspan=2, pady=15)

#output text
outputVar = StringVar()
outputVar.set("Input a username and a password")
outputLabel = Label(root, textvariable=outputVar, bg=back, fg=main, font=nexaRegular)
outputLabel.grid(row=3, column=0, columnspan=2, pady=(15, 40))

#start threads
colorThread.start()

#execute tkinter window
root.mainloop()
