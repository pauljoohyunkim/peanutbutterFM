#!/bin/python3
import os
import configparser
import tkinter as tk
from turtle import bgcolor

currentPathString = os.getcwd()

def changeDirectory():
    global currentPathString
    pathString = pathEntry.get()
    try:
        os.chdir(pathString)
        currentPathString = pathString
        print(f"Changing directory to: {pathString}")
    except:
        print(f"Changing directory to: {pathString} failed.")

        # Rewrite the path
        pathEntry.delete(0, tk.END)
        pathEntry.insert(0, currentPathString)



if __name__ == "__main__":

    # Configuration & Initialization
    config = configparser.ConfigParser()
    config.read("pb.conf")
    windowSize = config["DEFAULT"]["WindowSize"]
    fgColor = config["THEME"]["fg"]
    bgColor = config["THEME"]["bg"]

    # Main Window
    mainWin = tk.Tk()
    mainWin.title("Peanut Butter FM")
    mainWin.geometry(windowSize)
    # Menu Bar
    menubar = tk.Menu(mainWin)
    # File Menu
    fileMenu = tk.Menu(menubar, tearoff=0)
    fileMenu.add_command(label="New")
    fileMenu.add_command(label="Open")
    fileMenu.add_command(label="Properties")
    fileMenu.add_separator()
    fileMenu.add_command(label="Recent Files")
    fileMenu.add_separator()
    fileMenu.add_command(label="Quit", command=mainWin.quit)
    menubar.add_cascade(label="File", menu=fileMenu)
    # Hash Menu
    hashMenu = tk.Menu(menubar, tearoff=0)
    hashMenu.add_command(label="MD5")
    hashMenu.add_command(label="SHA-256")
    menubar.add_cascade(label="Hash", menu=hashMenu)
    mainWin.config(menu=menubar)


    # Navigator Frame
    navigatorFrame = tk.Frame(master=mainWin)
    locationLabel = tk.Label(master=navigatorFrame, text="Path: ", fg=fgColor, bg=bgColor)
    pathEntry = tk.Entry(master=navigatorFrame, width=100, fg=fgColor, bg = bgColor)
    goButton = tk.Button(master=navigatorFrame, text="Navigate", fg=fgColor, bg=bgColor, command=changeDirectory)

    locationLabel.grid(row=0,column=0)
    pathEntry.grid(row=0,column=1)
    pathEntry.insert(0, os.getcwd())
    goButton.grid(row=0,column=2)
    navigatorFrame.grid(row=0,column=0)
    # Labels
    







    mainWin.mainloop()

