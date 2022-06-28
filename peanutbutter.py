#!/bin/python3
import os
import re
import configparser
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from filelib.images import imageCanvas, supported_img_types
import subprocess

currentPathString = os.getcwd()

def currentTime():
    now = datetime.now()
    return now.strftime("%Y.%m.%d %H:%M:%S")    

def updateFileList():
    global currentPathString
    
    # Clear fileListBox
    fileListBox.delete(0, tk.END)

    fileList = os.listdir()

    # Directories first
    for file in fileList:
        if os.path.isdir(file):
            fileListBox.insert(tk.END, file)
            fileListBox.itemconfig(tk.END, {"fg": folderColor})
    
    # Then files
    for file in fileList:
        if os.path.isfile(file):
            fileListBox.insert(tk.END, file)


def navigateDirectory(pathString=None):
    global currentPathString
    if not pathString:
        pathString = pathEntry.get()

    # If Directory
    if os.path.isdir(pathString):
        try:
            os.chdir(pathString)
            currentPathString = pathString
            print(f"[{currentTime()}] Changing directory to: {pathString}")

            # Refresh content list
            #fileListBox.delete(0, tk.END)
            updateFileList()
            pathEntry.delete(0, tk.END)
            pathEntry.insert(0, currentPathString)
        except:
            print(f"[{currentTime()}] Changing directory to: {pathString} failed.")

            # Rewrite the path
            pathEntry.delete(0, tk.END)
            pathEntry.insert(0, currentPathString)
    # If file
    elif os.path.isfile(pathString):
        try:
            subprocess.run([openFileMethod, pathString])
            print(f"[{currentTime()}] Opened {pathString} with default application.")
        except:
            print(f"[{currentTime()}] Opening {pathString} with default application failed.")
    
    else:
        print(f"[{currentTime()}] Changing directory to: {pathString} failed.")
        # Rewrite the path
        pathEntry.delete(0, tk.END)
        pathEntry.insert(0, currentPathString)
    
    fileListBox.selection_set(0)
def upDirectory():
    global currentPathString
    pathString = os.path.dirname(currentPathString)
    os.chdir(pathString)
    currentPathString = pathString
    print(f"[{currentTime()}] Changing directory tg: {pathString}")

    # Refresh content list
    fileListBox.delete(0, tk.END)
    updateFileList()
    pathEntry.delete(0, tk.END)
    pathEntry.insert(0, currentPathString)

def property_summary(currentPathString, fileListBox,sizeStringVar, modifiedStringVar, createdStringVar, osStatStringVar, imagePreviewCanvas):
    global previewImage
    cs = fileListBox.curselection()
    if len(cs) == 1:
        filename = fileListBox.get(cs[0])
        fullFilename = os.path.join(currentPathString, filename)
        size = os.path.getsize(fullFilename)
        modifiedTime = os.path.getmtime(fullFilename)
        creationTime = os.path.getctime(fullFilename)
        stat_result = os.stat(fullFilename)
        sizeStringVar.set(f"Size: {size} bytes")
        modifiedStringVar.set(f"Last Modified: {modifiedTime}")
        createdStringVar.set(f"Created: {creationTime}")
        osStatStringVar.set(f"Raw File Stat: {stat_result}")
        if fullFilename.endswith(supported_img_types):
            imagePreviewFrame.pack()
            imagePreviewCanvas.delete("all")
            previewImage = imageCanvas(fullFilename, (imagePreviewHeight, imagePreviewWidth))
            imagePreviewCanvas.create_image(imagePreviewWidth / 2, imagePreviewHeight / 2,anchor=tk.CENTER,image = previewImage)
        else:
            imagePreviewFrame.forget()
            imagePreviewCanvas.delete("all")

def autoCompletePath():
    global currentPathString
    folders = [folder for folder in os.listdir() if os.path.isdir(os.path.join(currentPathString,folder))]
    possibilities = [folder for folder in folders if re.search("^" + os.path.basename(pathEntry.get()), folder)]
    if len(possibilities) == 1:
        pathEntry.delete(0, tk.END)
        pathEntry.insert(0, os.path.join(currentPathString, possibilities[0]))
        print(f"[{currentTime()}] Autocompletion")
    return "break"      # For disabling highlight of pathEntry




def fileActionDelete():
    global currentPathString
    fileName = os.path.join(currentPathString, fileListBox.get(fileListBox.curselection()))
    deleteQ = messagebox.askyesno("Deletion Warning", f"Delete {fileName}?")

    if deleteQ == True:
        os.remove(fileName)
        print(f"Removed file")
        updateFileList()

if __name__ == "__main__":

    # Configuration & Initialization
    config = configparser.ConfigParser()
    config.read("pb.conf")
    windowSize = config["DEFAULT"]["WindowSize"]
    pathEntryWidth = int(config["DEFAULT"]["PathEntryWidth"])
    imagePreviewWidth = int(config["DEFAULT"]["ImagePreviewWidth"])
    imagePreviewHeight = int(config["DEFAULT"]["ImagePreviewHeight"])
    fgColor = config["THEME"]["fg"]
    bgColor = config["THEME"]["bg"]
    folderColor = config["THEME"]["folder"]
    openFileMethod = config["ACTION"]["open"]

    # Main Window
    mainWin = tk.Tk()
    mainWin.title("Peanut Butter FM")
    mainWin.geometry(windowSize)
    mainWin.configure(bg=bgColor)
    
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


    # Navigator Frame: Folder navigation
    navigatorFrame = tk.Frame(master=mainWin, bg=bgColor)
    locationLabel = tk.Label(master=navigatorFrame, text="Path: ", fg=fgColor, bg=bgColor)
    pathEntry = tk.Entry(master=navigatorFrame, width=pathEntryWidth, fg=fgColor, bg = bgColor)
    goButton = tk.Button(master=navigatorFrame, text="Navigate", fg=fgColor, bg=bgColor, command=lambda: navigateDirectory(), takefocus=False)
    upFolderButton = tk.Button(master=navigatorFrame, text="Up Folder", fg=fgColor, bg=bgColor, command=lambda: navigateDirectory(os.path.dirname(currentPathString)), takefocus=False)

    locationLabel.grid(row=0,column=0)
    pathEntry.grid(row=0,column=1)
    pathEntry.insert(0, os.getcwd())
    pathEntry.focus()
    goButton.grid(row=0,column=2)
    upFolderButton.grid(row=0, column=3)
    #navigatorFrame.place(x=20, y=20)
    navigatorFrame.pack(fill = tk.X)
    
    # Content Frame: Shows the files.
    contentFrame = tk.Frame(master=mainWin)
    fileListBox = tk.Listbox(master=contentFrame, width=pathEntryWidth, fg=fgColor, bg=bgColor, takefocus=False)
    updateFileList()
    fileListScrollbar = tk.Scrollbar(master=contentFrame, takefocus=False)
    fileListBox.config(yscrollcommand = fileListScrollbar.set)
    fileListScrollbar.config(command = fileListBox.yview)
    fileListScrollbar.pack()


    fileListBox.pack(fill = tk.X)
    fileListScrollbar.pack(side = tk.RIGHT)
    #fileListBox.grid(row=0,column=0)
    #contentFrame.place(x=20, y=60)
    contentFrame.pack(fill = tk.X)

    # Properties Frame: Shows properties of the file
    fileSizeStringVar = tk.StringVar()
    fileSizeStringVar.set("Size: ")
    fileLastModifiedStringVar = tk.StringVar()
    fileLastModifiedStringVar.set("Last Modified: ")
    fileCreationStringVar = tk.StringVar()
    fileCreationStringVar.set("Created: ")
    osStatStringVar = tk.StringVar()
    osStatStringVar.set("Raw File Stat:")

    propertiesFrame = tk.Frame(master=mainWin, bg=bgColor)
    propertiesLabel = tk.Label(master=propertiesFrame, text="Properties: ", fg=fgColor, bg=bgColor)
    propertiesLabel["font"] = "bold"
    fileSizeLabel = tk.Label(master=propertiesFrame, textvariable=fileSizeStringVar, fg=fgColor, bg=bgColor)
    fileLastModifiedLabel = tk.Label(master=propertiesFrame, textvariable=fileLastModifiedStringVar, fg=fgColor, bg=bgColor)
    fileCreationLabel = tk.Label(master=propertiesFrame, textvariable=fileCreationStringVar, fg=fgColor, bg=bgColor)
    osStatLabel = tk.Label(master=propertiesFrame, textvariable=osStatStringVar, fg=fgColor, bg=bgColor)

    #propertiesLabel.grid(row=0,column=0)
    #fileSizeLabel.grid(row=1, column=0)
    #fileLastModifiedLabel.grid(row=2, column=0)
    #fileCreationLabel.grid(row=3, column=0)
    #osStatLabel.grid(row=4, column=0)
    
    propertiesLabel.pack(anchor="w")
    fileSizeLabel.pack(anchor="w")
    fileLastModifiedLabel.pack(anchor="w")
    fileCreationLabel.pack(anchor="w")
    osStatLabel.pack(anchor="w")
    propertiesFrame.pack(fill = tk.X, expand=False)

    # Image Preview Frame
    imagePreviewFrame = tk.Frame(master=mainWin, bg=bgColor)
    imagePreviewLabel = tk.Label(master=imagePreviewFrame, text="Image Preview", fg=fgColor, bg=bgColor)
    imagePreviewLabel["font"] = "bold"
    imagePreviewLabel.pack()
    imagePreviewCanvas = tk.Canvas(master=imagePreviewFrame, width=imagePreviewWidth, height=imagePreviewHeight, bg=bgColor)
    imagePreviewCanvas.pack()

    #previewImage = imageCanvas("PNG_Test.png", (imagePreviewHeight, imagePreviewWidth))
    #imageContainer = imagePreviewCanvas.create_image(imagePreviewWidth / 2, imagePreviewHeight / 2,anchor=tk.CENTER,image = previewImage)
    #imagePreviewFrame.pack()

    # Bindings

    # Property Update
    # At every selection, the property summary gets updated.
    fileListBox.bind("<<ListboxSelect>>", lambda event: property_summary(currentPathString, fileListBox,fileSizeStringVar, fileLastModifiedStringVar, fileCreationStringVar, osStatStringVar, imagePreviewCanvas))
    # Navigate directory / Open file
    # Double click and Enter for navigation
    # Escape for upper folder
    fileListBox.bind("<Double-1>", lambda event: navigateDirectory(os.path.join(currentPathString, fileListBox.get(fileListBox.curselection()))))
    fileListBox.bind("<Return>", lambda event: navigateDirectory(os.path.join(currentPathString, fileListBox.get(fileListBox.curselection()))))
    fileListBox.bind("<Escape>", lambda event: navigateDirectory(os.path.dirname(currentPathString)))
    pathEntry.bind("<Return>", lambda event: navigateDirectory(pathEntry.get()))
    pathEntry.bind("<Escape>", lambda event: navigateDirectory(os.path.dirname(currentPathString)))
    # Autocompletion for Folders
    pathEntry.bind("<Tab>", lambda event: autoCompletePath())
    # Listbox Cursor Movement
    # HOME for the first item
    # END for the last item
    fileListBox.bind("<Home>", lambda event: [fileListBox.select_clear(0, tk.END), fileListBox.selection_set(0)])
    fileListBox.bind("<End>", lambda event: [fileListBox.select_clear(0, tk.END), fileListBox.selection_set(tk.END)])
    # File Actions
    fileListBox.bind("<Delete>", lambda event: fileActionDelete())


    mainWin.mainloop()

