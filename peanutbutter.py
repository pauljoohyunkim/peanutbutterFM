#!/bin/python3
import sys
import os
import re
import configparser
import textwrap
import time
import tkinter as tk
from tkinter import TclError, messagebox
from datetime import datetime
from filelib.hasher import sha256sum, md5sum
from filelib.images import imageCanvas, supported_img_types, simpleTkImage
# Listing Engine: Dictionary/Map of aliases of names of folders and files. This might be useful for encryption.
# By default, this will simply be an identity map, but this can be changed depending on the need.
# In simple term, essentially, listingEngine(realName) = alias
from listingenginelib.listingengine import ListingMap, defaultListingEngine
import subprocess
import shutil

currentPathString = os.getcwd()
currentListingEngine = defaultListingEngine
currentFileList = []
favoritesList = []
customScripts = []

def currentTime():
    now = datetime.now()
    return now.strftime("%Y.%m.%d %H:%M:%S")    

def debugMessage(string):
    print(f"[{currentTime()}] {string}")

def updateFileList():
    global currentPathString
    global currentFileList    
    # Clear fileListBox
    fileListBox.delete(0, tk.END)

    filelist = [currentListingEngine.eval(file) for file in os.listdir()]

    currentFileList = []
    # Directories first
    for file in filelist:
        if os.path.isdir(currentListingEngine.inveval(file)):
            fileListBox.insert(tk.END, file)
            fileListBox.itemconfig(tk.END, {"fg": folderColor})
            currentFileList.append(file)
    
    # Then files
    for file in filelist:
        if os.path.isfile(currentListingEngine.inveval(file)):
            fileListBox.insert(tk.END, file)
            currentFileList.append(file)


def navigateDirectory(pathString=None):
    global currentPathString
    if not pathString:
        pathString = pathEntry.get()
    
    if pathString == ".":
        pathString = currentPathString

    # If Directory
    if os.path.isdir(pathString):
        try:
            os.chdir(pathString)
            currentPathString = pathString
            debugMessage(f"Changing directory to: {pathString}")

            # Refresh content list
            #fileListBox.delete(0, tk.END)
            updateFileList()
            pathEntry.delete(0, tk.END)
            pathEntry.insert(0, currentPathString)
        except:
            debugMessage(f"Changing directory to: {pathString} failed.")

            # Rewrite the path
            pathEntry.delete(0, tk.END)
            pathEntry.insert(0, currentPathString)
    # If file
    elif os.path.isfile(pathString):
        try:
            subprocess.run([openFileMethod, pathString])
            debugMessage(f"Opened {pathString} with default application.")
        except:
            debugMessage(f"Opening {pathString} with default application failed.")
    
    else:
        debugMessage(f"Changing directory to: {pathString} failed.")
        # Rewrite the path
        pathEntry.delete(0, tk.END)
        pathEntry.insert(0, currentPathString)
    
    # If a file is already selected, keep the selection.
    # Otherwise, force the selection onto the first item.

    # If a file does not exist in a folder, do nothing.
    #try:
    #    imagePreview(os.path.join(currentPathString, fileListBox.selection_get()))
    #except:
    #    try:
    #        fileListBox.select_clear(0, tk.END)
    #        fileListBox.selection_set(0)
    #        imagePreview(os.path.join(currentPathString, fileListBox.selection_get()))
    #    except:
    #        pass

    try:
        fileListBox.selection_get()
    except:
        try:
            fileListBox.select_clear(0, tk.END)
            fileListBox.selection_set(0)
            property_summary()
            #imagePreview(os.path.join(currentPathString, fileListBox.selection_get()))
        except:
            pass
        
def property_summary():
    global previewImage
    cs = fileListBox.curselection()
    if len(cs) == 1:
        filename = currentListingEngine.inveval(fileListBox.get(cs[0]))
        fullFilename = os.path.join(currentPathString, filename)
        size = f"Size: {os.path.getsize(fullFilename)} bytes" if os.path.isfile(fullFilename) else "Size: REDACTED (Folder)"
        modifiedTime = time.ctime(os.path.getmtime(fullFilename))
        creationTime = time.ctime(os.path.getctime(fullFilename))
        stat_result = os.stat(fullFilename)
        fileSizeStringVar.set(size)
        fileLastModifiedStringVar.set(f"Last Modified: {modifiedTime}")
        fileCreationStringVar.set(f"Created: {creationTime}")
        osStatStringVar.set(f"Raw File Stat: {stat_result}")
        imagePreview(fullFilename)

def imagePreview(fullFilename):
    global previewImage
    if fullFilename.lower().endswith(supported_img_types):
        imagePreviewFrame.pack()
        imagePreviewCanvas.delete("all")
        previewImage = imageCanvas(fullFilename, (imagePreviewHeight, imagePreviewWidth))
        imagePreviewCanvas.create_image(imagePreviewWidth / 2, imagePreviewHeight / 2,anchor=tk.CENTER,image = previewImage)
    else:
        imagePreviewFrame.forget()
        imagePreviewCanvas.delete("all")

def autoCompletePath():
    currentEntryDir = os.path.dirname(pathEntry.get())
    folders = [folder for folder in os.listdir(currentEntryDir) if os.path.isdir(os.path.join(currentEntryDir,folder))]
    possibilities = [folder for folder in folders if re.search("^" + os.path.basename(currentListingEngine.inveval(pathEntry.get())), folder)]
    if len(possibilities) == 1:
        pathEntry.delete(0, tk.END)
        pathEntry.insert(0, os.path.join(currentEntryDir, possibilities[0],""))
        debugMessage(f"Autocompletion: {os.path.join(currentEntryDir, possibilities[0])}")
    return "break"      # For disabling highlight of pathEntry




def fileActionDelete():
    global currentPathString
    fileName = os.path.join(currentPathString, currentListingEngine.inveval(fileListBox.selection_get()))
    deleteQ = messagebox.askyesno("Deletion Warning", f"Delete {fileName}?")

    if deleteQ == True:
        if os.path.isdir(fileName):
            shutil.rmtree(fileName)
            debugMessage(f"Deleted folder {fileName}")
        elif os.path.isfile(fileName):
            os.remove(fileName)
            debugMessage(f"Deleted file {fileName}")
        updateFileList()

def showHash(hashtype):
    global currentPathString
    try:
        fileName = os.path.join(currentPathString, currentListingEngine.inveval(fileListBox.selection_get()))
        
        if os.path.isfile(fileName) == False:
            messagebox.showerror(f"SHA256: {fileName}", f"{fileName} is not a file.")
            return 1
        
        if hashtype == "sha256":
            messagebox.showinfo(f"SHA256: {fileName}", f"{sha256sum(fileName)}")
        if hashtype == "md5":
            messagebox.showinfo(f"MD5: {fileName}", f"{md5sum(fileName)}")
    except TclError:
        messagebox.showerror("Hash", "Cannot show hash. Did you select a file?")

def onClosing():
    global restoreSession
    if restoreSession:
        prev["NAVIGATION"]["Folder"] = currentPathString
        for i in range(1,10):
            prev["FAVORITES"][f"folder{i}"] = favoritesList[i-1]
        with open(os.path.join(scriptLocation, ".session.ini"), "w") as saveSession:
            prev.write(saveSession)
    mainWin.destroy()

def setFavorite(index):
    favoritesList[index] = currentListingEngine.eval(currentPathString)
    favoritesMenu.entryconfig(index, label=currentListingEngine.eval(currentPathString) + " " * 50 + f"Alt+{index + 1}")

    debugMessage(f"Set {currentListingEngine.eval(currentPathString)} to folder{index + 1}")

def focusOnPathEntry():
    pathEntry.focus()
    return "break"

def fileSelectByFirstChar(character):
    fileStartsWithCharList = [file for file in currentFileList if file.startswith(character)]
    currentSelectionIndex = currentFileList.index(fileListBox.selection_get())
    if fileStartsWithCharList:
        try:
            for index in range(currentSelectionIndex+1, len(currentFileList)):
                if currentFileList[index] in fileStartsWithCharList:
                    fileListBox.selection_clear(0, tk.END)
                    fileListBox.selection_set(index)
                    fileListBox.see(index)
                    break
        except:
            debugMessage("Error in fileSelectByFirstChar function.")

def setCustomScript(index):
    scriptName = os.path.join(currentPathString, fileListBox.selection_get())
    customScripts[index] = currentListingEngine.eval(scriptName)
    customScriptMenu.entryconfig(index, label=currentListingEngine.eval(scriptName) + " " * 50 + f"Ctrl+Numpad {index + 1}")
    debugMessage(f"Set {currentListingEngine.eval(scriptName)} to script{index+1}")

def runCustomScript(index):
    subprocess.run([currentListingEngine.inveval(customScripts[index])])
    updateFileList()
    debugMessage(f"Running {customScripts[index]}")

if __name__ == "__main__":

    # Location of the program
    scriptLocation = sys.path[0]

    # Configuration & Initialization
    config = configparser.ConfigParser()
    config.read(os.path.join(scriptLocation, "pb.conf"))
    windowSize = config["DEFAULT"]["WindowSize"]
    pathEntryWidth = int(config["DEFAULT"]["PathEntryWidth"])
    imagePreviewWidth = int(config["DEFAULT"]["ImagePreviewWidth"])
    imagePreviewHeight = int(config["DEFAULT"]["ImagePreviewHeight"])
    restoreSession = bool(config["DEFAULT"]["RestoreSession"])
    fgColor = config["THEME"]["fg"]
    bgColor = config["THEME"]["bg"]
    folderColor = config["THEME"]["folder"]
    openFileMethod = config["ACTION"]["open"]
    #Restoring session if restoreSession = True
    if restoreSession:
        prev = configparser.ConfigParser()
        prev.read(os.path.join(scriptLocation, ".session.ini"))
        currentPathString = prev["NAVIGATION"]["Folder"]
        os.chdir(currentPathString)

    # Main Window
    mainWin = tk.Tk()
    mainWin.title("Peanut Butter FM")
    mainWin.geometry(windowSize)
    mainWin.configure(bg=bgColor)
    icon = simpleTkImage(os.path.join(scriptLocation, "peanutbutter.jpg"))
    mainWin.wm_iconphoto(False, icon)
    mainWin.protocol("WM_DELETE_WINDOW", onClosing)
    
    # Navigator Frame: Folder navigation
    navigatorFrame = tk.Frame(master=mainWin, bg=bgColor)
    locationLabel = tk.Label(master=navigatorFrame, text="Path: ", fg=fgColor, bg=bgColor)
    pathEntry = tk.Entry(master=navigatorFrame, width=pathEntryWidth, fg=fgColor, bg = bgColor)
    goButton = tk.Button(master=navigatorFrame, text="Navigate", fg=fgColor, bg=bgColor, command=lambda: navigateDirectory(), takefocus=False)
    upFolderButton = tk.Button(master=navigatorFrame, text="Up Folder", fg=fgColor, bg=bgColor, command=lambda: navigateDirectory(os.path.dirname(currentPathString)), takefocus=False)

    locationLabel.grid(row=0,column=0)
    pathEntry.grid(row=0,column=1)
    pathEntry.insert(0, currentPathString)
    pathEntry.focus()
    goButton.grid(row=0,column=2)
    upFolderButton.grid(row=0, column=3)
    #navigatorFrame.place(x=20, y=20)
    navigatorFrame.pack(fill = tk.X)
    
    # Content Frame: Shows the files.
    contentFrame = tk.Frame(master=mainWin)
    fileListBox = tk.Listbox(master=contentFrame, width=pathEntryWidth, fg=fgColor, bg=bgColor, takefocus=True)
    updateFileList()
    fileListScrollbar = tk.Scrollbar(master=contentFrame, takefocus=False)
    fileListBox.config(yscrollcommand = fileListScrollbar.set)
    fileListScrollbar.config(command = fileListBox.yview)
    fileListScrollbar.pack(side="right", fill="y", expand=False)


    fileListBox.pack(fill = tk.X)
    fileListScrollbar.pack(side = tk.RIGHT)
    #fileListBox.grid(row=0,column=0)
    #contentFrame.place(x=20, y=60)
    contentFrame.pack(fill = tk.X)

    # By default, select the first entry, unless it is not possible.
    try:
        fileListBox.selection_set(0)
    except:
        pass

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
    
    propertiesLabel.pack(anchor="w")
    fileSizeLabel.pack(anchor="w")
    fileLastModifiedLabel.pack(anchor="w")
    fileCreationLabel.pack(anchor="w")
    osStatLabel.pack(anchor="w")
    propertiesFrame.pack(fill = tk.X, expand=False)

    # By default, show property of the selected item if possible.
    try:
        property_summary()
    except:
        pass

    # Image Preview Frame
    imagePreviewFrame = tk.Frame(master=mainWin, bg=bgColor)
    imagePreviewLabel = tk.Label(master=imagePreviewFrame, text="Image Preview", fg=fgColor, bg=bgColor)
    imagePreviewLabel["font"] = "bold"
    imagePreviewLabel.pack()
    imagePreviewCanvas = tk.Canvas(master=imagePreviewFrame, width=imagePreviewWidth, height=imagePreviewHeight, bg=bgColor)
    imagePreviewCanvas.pack()

    

    # Menu Bar
    menubar = tk.Menu(mainWin, fg=fgColor, bg=bgColor)
    # File Menu
    fileMenu = tk.Menu(menubar, tearoff=0)
    fileMenu.add_command(label="New")
    fileMenu.add_command(label="Open", command=lambda: navigateDirectory(os.path.join(currentPathString, fileListBox.selection_get())))
    fileMenu.add_command(label="Properties")
    fileMenu.add_separator()
    fileMenu.add_command(label="Recent Files")
    fileMenu.add_separator()
    fileMenu.add_command(label="Quit", command=mainWin.quit)
    menubar.add_cascade(label="File", menu=fileMenu)
    # Hash Menu
    hashMenu = tk.Menu(menubar, tearoff=0)
    hashMenu.add_command(label="MD5", command=lambda: showHash("md5"))
    hashMenu.add_command(label="SHA-256", command=lambda: showHash("sha256"))
    menubar.add_cascade(label="Hash", menu=hashMenu)
    # Favorites Menu
    favoritesMenu = tk.Menu(menubar, tearoff=0)
    #favoritesMenu.add_command(label="Folder 1", command=lambda: navigateDirectory("/"))
    for i in range(1,10):
        def lambdaNavigateFavorites(x):
            return lambda: navigateDirectory(favoritesList[x-1])
        favoritesMenu.add_command(label=f"Folder {i}" + " " * 50 + f"Alt+Ctrl+{i} to set favorite.", command = lambdaNavigateFavorites(i))
    
    # Restore favorites
    if restoreSession:
        for i in range(9):
            if prev["FAVORITES"][f"folder{i+1}"] != ".":
                favoritesMenu.entryconfig(i, label=prev["FAVORITES"][f"folder{i+1}"] + " " * 50 + f"Alt+{i+1}")
                favoritesList.append(prev["FAVORITES"][f"folder{i+1}"])
            else:
                favoritesList.append(".")
    menubar.add_cascade(label="Favorites", menu=favoritesMenu)
    # Custom Scripts
    customScriptMenu = tk.Menu(menubar, tearoff=0)
    #customScriptMenu.add_command(label="Script 1")
    for i in range(1,10):
        def lambdaRunCustomScript(x):
            return lambda: runCustomScript(customScripts[x-1])
        customScriptMenu.add_command(label=f"Script {i}" + " " * 50 + f"Alt+Ctrl+Numpad {i} to set custom script.", command = lambdaRunCustomScript(i))
    menubar.add_cascade(label="Custom Scripts", menu=customScriptMenu)
    mainWin.config(menu=menubar)

    # Restore Custom Scripts
    if restoreSession:
        for i in range(9):
            if prev["CUSTOMSCRIPTS"][f"script{i+1}"] != ".":
                customScripts.append(prev["CUSTOMSCRIPTS"][f"folder{i+1}"])
            else:
                customScripts.append(".")


    # Bindings

    # Property Update
    # At every selection, the property summary gets updated.
    fileListBox.bind("<<ListboxSelect>>", lambda event: property_summary())
    # Navigate directory / Open file
    # Double click and Enter for navigation
    fileListBox.bind("<Double-1>", lambda event: navigateDirectory(os.path.join(currentPathString, currentListingEngine.inveval(fileListBox.selection_get()))))
    fileListBox.bind("<Return>", lambda event: navigateDirectory(os.path.join(currentPathString, currentListingEngine.inveval(fileListBox.selection_get()))))
    pathEntry.bind("<Return>", lambda event: navigateDirectory(pathEntry.get()))
    # Refresh fileListBox
    mainWin.bind("<F5>", lambda event: [updateFileList(), debugMessage("fileListBox refreshed.")])
    # Escape for upper folder
    fileListBox.bind("<Escape>", lambda event: navigateDirectory(os.path.dirname(currentPathString)))
    pathEntry.bind("<Escape>", lambda event: navigateDirectory(os.path.dirname(currentPathString)))
    # Autocompletion for Folders
    pathEntry.bind("<Tab>", lambda event: autoCompletePath())
    # Listbox Cursor Movement
    # HOME for the first item
    fileListBox.bind("<Home>", lambda event: [fileListBox.select_clear(0, tk.END), fileListBox.selection_set(0), fileListBox.see(0)])
    # END for the last item
    fileListBox.bind("<End>", lambda event: [fileListBox.select_clear(0, tk.END), fileListBox.selection_set(tk.END), fileListBox.see(tk.END)])
    # fileListBox focused when pressing down arrow key.
    mainWin.bind("<Down>", lambda event: fileListBox.focus())
    # fileListBox select file that starts with certain characters
    for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
        def lambdaFileSelectByFirstChar(character):
            return lambda event: fileSelectByFirstChar(character)
        fileListBox.bind(f"<KeyPress-{char}>", lambdaFileSelectByFirstChar(char))
    # pathEntry focused when tabbed from fileListBox
    fileListBox.bind("<Tab>", lambda event: focusOnPathEntry())
    # File Actions
    fileListBox.bind("<Delete>", lambda event: fileActionDelete())
    # Favorites (Adding to Favorite and navigation) & Custom Scripts
    symbol_to_num = {}
    for i in range(9):
        def lambdaSetFavorite(x):
            return lambda event: setFavorite(x-1)
        def lambdaNavigateFavorite(x):
            return lambda event: navigateDirectory(favoritesList[x-1])
        def lambdaSetCustomScript(x):
            return lambda event: setCustomScript(x-1)
        def lambdaRunCustomScript(x):
            return lambda event: runCustomScript(x-1)
        fileListBox.bind(f"<Alt-Control-KeyPress-{i}>", lambdaSetFavorite(i))
        pathEntry.bind(f"<Alt-Control-KeyPress-{i}>", lambdaSetFavorite(i))
        fileListBox.bind(f"<Alt-KeyPress-{i}>", lambdaNavigateFavorite(i))
        pathEntry.bind(f"<Alt-KeyPress-{i}>", lambdaNavigateFavorite(i))
        fileListBox.bind(f"<Alt-Control-KeyPress-KP_{i}>", lambdaSetCustomScript(i))
        fileListBox.bind(f"<Control-KeyPress-KP_{i}>", lambdaRunCustomScript(i))
        fileListBox.bind(f"<Control-KeyPress-{i}>", lambdaRunCustomScript(i))
    

    mainWin.mainloop()

