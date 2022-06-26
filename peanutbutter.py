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
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New")
    filemenu.add_command(label="Open")
    filemenu.add_command(label="Properties")
    filemenu.add_separator()
    filemenu.add_command(label="Recent Files")
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=mainWin.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    # Hash Menu
    hashmenu = tk.Menu(menubar, tearoff=0)
    hashmenu.add_command(label="MD5")
    hashmenu.add_command(label="SHA-256")
    menubar.add_cascade(label="Hash", menu=hashmenu)

    mainWin.config(menu=menubar)


    

    mainWin.mainloop()

