#!/bin/python3
import os
import configparser
import tkinter as tk


if __name__ == "__main__":
    
    # Configuration
    config = configparser.ConfigParser()
    config.read("pb.conf")
    windowSize = config['DEFAULT']['WindowSize']

    # Main Window
    mainWin = tk.Tk()
    mainWin.title("Peanut Butter")
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




    # Labels
    locationLabel = tk.Label(mainWin, text="Path: ")
    

    mainWin.mainloop()

