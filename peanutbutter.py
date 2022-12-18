#!/bin/python3
import sys
import global_var
# Location of the program
scriptLocation = sys.path[0]
global_var.scriptLocation = scriptLocation

import os
import re
import configparser
import textwrap
import time
import tkinter as tk
from tkinter import TclError, messagebox, simpledialog
from datetime import datetime
from filelib.hasher import sha256sum, md5sum
from filelib.images import imageCanvas, supported_img_types, simpleTkImage
# Listing Engine: Dictionary/Map of aliases of names of folders and files. This might be useful for encryption.
# By default, this will simply be an identity map, but this can be changed depending on the need.
# In simple term, essentially, listingEngine(realName) = alias
from listingenginelib.listingengine import ListingMap, defaultListingEngine
# Import Plugins
from pbPlugin.plugin import Plugin, pluginDictionary
with open(os.path.join(scriptLocation,"plugin.conf")) as file:
    pluginLib = file.readline().strip()
    while pluginLib:
        exec(f"from pbPlugin.{pluginLib} import *")
        pluginLib = file.readline().strip()
import subprocess
import shutil
import platform

# global_var.currentPathString, global_var.clipboardPathString are in real name
global_var.currentPathString = os.getcwd()
global_var.clipboardPathString = ""
global_var.currentListingEngine = defaultListingEngine
# global_var.currentFileList is in real name
# global_var.favoritesList and global_var.customScripts are in alias
global_var.currentFileList = []
global_var.favoritesList = []
global_var.customScripts = []
global_var.cutInsteadOfCopy = False
global_var.extensionLaunchDict = {}

def currentTime():
    now = datetime.now()
    return now.strftime("%Y.%m.%d %H:%M:%S")    

def debugMessage(string):
    msg = f"[{currentTime()}] {string}"
    print(msg)
    global_var.debugStringVar.set(textwrap.fill(f"Debug: {msg}",80))

def updateFileList():
    #global global_var.currentPathString
    #global global_var.currentFileList    
    # Clear fileListBox
    fileListBox.delete(0, tk.END)

    filelist = [global_var.currentListingEngine.eval(file) for file in os.listdir()]
    filelist.sort()

    global_var.currentFileList = []
    # Directories first
    for file in filelist:
        realFile = global_var.currentListingEngine.inveval(file)
        if os.path.isdir(realFile):
            fileListBox.insert(tk.END, file)
            fileListBox.itemconfig(tk.END, {"fg": folderColor})
            global_var.currentFileList.append(realFile)
    
    # Then files
    for file in filelist:
        realFile = global_var.currentListingEngine.inveval(file)
        if os.path.isfile(global_var.currentListingEngine.inveval(file)):
            fileListBox.insert(tk.END, file)
            global_var.currentFileList.append(realFile)

# Input real filename
def navigateDirectory(pathString=None):
    #global global_var.currentPathString
    if not pathString:
        pathString = pathEntry.get()
    
    if pathString == ".":
        pathString = global_var.currentPathString

    # If Directory
    if os.path.isdir(pathString):
        try:
            os.chdir(pathString)
            global_var.currentPathString = pathString
            debugMessage(f"Changing directory to: {pathString}")

            # Refresh content list
            #fileListBox.delete(0, tk.END)
            updateFileList()
            pathEntry.delete(0, tk.END)
            pathEntry.insert(0, global_var.currentListingEngine.eval(global_var.currentPathString))
        except:
            debugMessage(f"Changing directory to: {pathString} failed.")

            # Rewrite the path
            pathEntry.delete(0, tk.END)
            pathEntry.insert(0, global_var.currentListingEngine.eval(global_var.currentPathString))
    # If file
    elif os.path.isfile(pathString):
        try:
            ext = os.path.splitext(pathString)[-1]
            if ext in global_var.extensionLaunchDict.keys():
                os.system(global_var.extensionLaunchDict[ext].replace("`fileName`", pathString))
                debugMessage(f"Opening {pathString} by {global_var.extensionLaunchDict[ext]} {pathString}")
            else:

                if platform.system().lower() == "windows":
                    os.startfile(pathString)
                elif platform.system().lower() == "linux":
                    subprocess.Popen(["xdg-open", pathString], start_new_session=True)
                elif platform.system().lower() == "darwin":
                    subprocess.run(["open", pathString])
                debugMessage(f"Opened {pathString} with default application.")
        except:
            debugMessage(f"Opening {pathString} failed.")
    
    else:
        debugMessage(f"Changing directory to: {pathString} failed.")
        # Rewrite the path
        pathEntry.delete(0, tk.END)
        pathEntry.insert(0, global_var.currentListingEngine.eval(global_var.currentPathString))
    
    try:
        fileListBox.selection_get()
    except:
        try:
            fileListBox.select_clear(0, tk.END)
            fileListBox.selection_set(0)
            property_summary()
        except:
            pass
        
def property_summary():
    global previewImage
    cs = fileListBox.curselection()
    if len(cs) == 1:
        filename = global_var.currentListingEngine.inveval(fileListBox.get(cs[0]))
        fullFilename = os.path.join(global_var.currentPathString, filename)
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

# Need to check if listing engine is correct here.
def autoCompletePath():
    currentEntryDir = os.path.dirname(global_var.currentListingEngine.inveval(pathEntry.get()))
    folders = [folder for folder in os.listdir(currentEntryDir) if os.path.isdir(os.path.join(currentEntryDir,folder))]
    possibilities = [folder for folder in folders if re.search("^" + os.path.basename(global_var.currentListingEngine.inveval(pathEntry.get())), folder)]
    if len(possibilities) == 1:
        pathEntry.delete(0, tk.END)
        pathEntry.insert(0, os.path.join(currentEntryDir, possibilities[0],""))
        debugMessage(f"Autocompletion: {os.path.join(currentEntryDir, possibilities[0])}")
    elif len(possibilities) > 2:
        debugMessage(f"Autocompletion: {possibilities}")
    return "break"      # For disabling highlight of pathEntry

def newFolder():
    try:
        folderName = simpledialog.askstring("Create New Directory", "Directory Name: ", parent=mainWin)
        if folderName:
            realFolderName = global_var.currentListingEngine.inveval(folderName)
            os.mkdir(realFolderName)
            debugMessage(f"Created {realFolderName} directory.")
    except FileExistsError:
        debugMessage(f"Error while creating {realFolderName} directory.")
        messagebox.showerror("Create New Directory", "Folder already exists.")
    updateFileList()


def addFileToClipboard():
    #global global_var.clipboardPathString
    #global global_var.currentPathString
    try:
        fileName = global_var.currentListingEngine.inveval(fileListBox.selection_get())
        global_var.clipboardPathString = os.path.join(global_var.currentPathString, fileName)
        debugMessage(f"Clipboard: {global_var.clipboardPathString}")
        return 0
    except:
        return 1

def cutAddFileToClipboard():
    if addFileToClipboard() == 0:
        global_var.cutInsteadOfCopy = True

def pasteFile():
    if global_var.clipboardPathString:
        if os.path.isfile(global_var.clipboardPathString) or os.path.isdir(global_var.clipboardPathString):
            # Check if the file or folder does not exist
            if not (os.path.isfile(os.path.join(global_var.currentPathString, os.path.basename(global_var.clipboardPathString))) or os.path.isdir(os.path.join(global_var.currentPathString, os.path.basename(global_var.clipboardPathString)))):
                if os.path.isfile(global_var.clipboardPathString):
                    shutil.copy(global_var.clipboardPathString, global_var.currentPathString)
                    # Copy Operation
                    if global_var.cutInsteadOfCopy == False:
                        debugMessage(f"Copied file to {os.path.join(global_var.currentPathString)}")
                    # Cut Operation
                    else:
                        os.remove(global_var.clipboardPathString)
                        global_var.cutInsteadOfCopy = False
                        debugMessage(f"Cut file to {os.path.join(global_var.currentPathString)}")
                else:
                    shutil.copytree(global_var.clipboardPathString, os.path.join(global_var.currentPathString, os.path.basename(global_var.clipboardPathString)))
                    # Copy Operation
                    if global_var.cutInsteadOfCopy == False:
                        debugMessage(f"Copied folder to {os.path.join(global_var.currentPathString, os.path.basename(global_var.clipboardPathString))}")
                    # Cut Operation
                    else:
                        shutil.rmtree(global_var.clipboardPathString)
                        global_var.cutInsteadOfCopy = False
                        debugMessage(f"Cut folder to {os.path.join(global_var.currentPathString, os.path.basename(global_var.clipboardPathString))}")
                global_var.clipboardPathString = ""
            # Otherwise, ask for overwriting.
            else:
                confirmation = messagebox.askyesno("Overwrite?", f"Overwrite {os.path.join(global_var.currentPathString, os.path.basename(global_var.clipboardPathString))}?")
                if confirmation: 
                    # Delete first, then copy
                    if os.path.isfile(os.path.join(global_var.currentPathString, os.path.basename(global_var.clipboardPathString))):
                        os.remove(os.path.join(global_var.currentPathString, os.path.basename(global_var.clipboardPathString)))
                        shutil.copy(global_var.clipboardPathString, global_var.currentPathString)
                        # Copy Operation
                        if global_var.cutInsteadOfCopy == False:
                            debugMessage(f"Overwritten file to {os.path.join(global_var.currentPathString)}")
                        # Cut Operation
                        else:
                            os.remove(global_var.clipboardPathString)
                            debugMessage(f"Overwritten file to {os.path.join(global_var.currentPathString)}")

                    elif os.path.isdir(os.path.join(global_var.currentPathString, os.path.basename(global_var.clipboardPathString))):
                        shutil.rmtree(os.path.join(global_var.currentPathString, os.path.basename(global_var.clipboardPathString)))
                        shutil.copytree(global_var.clipboardPathString, os.path.join(global_var.currentPathString, os.path.basename(global_var.clipboardPathString)))
                        # Copy Operation
                        if global_var.cutInsteadOfCopy == False:
                            debugMessage(f"Overwritten folder to {os.path.join(global_var.currentPathString, os.path.basename(global_var.clipboardPathString))}")
                        # Cut Operation
                        else:
                            shutil.rmtree(global_var.clipboardPathString)
                            global_var.cutInsteadOfCopy = False
                            debugMessage(f"Overwritten folder to {os.path.join(global_var.currentPathString, os.path.basename(global_var.clipboardPathString))}")
                    global_var.clipboardPathString = ""
    updateFileList()


def fileActionDelete():
    fileName = os.path.join(global_var.currentPathString, global_var.currentListingEngine.inveval(fileListBox.selection_get()))
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
    try:
        fileName = os.path.join(global_var.currentPathString, global_var.currentListingEngine.inveval(fileListBox.selection_get()))
        
        if os.path.isfile(fileName) == False:
            messagebox.showerror(f"SHA256: {fileName}", f"{fileName} is not a file.")
            return 1
        
        if hashtype == "sha256":
            debugMessage(f"Viewed {hashtype} hash.")
            messagebox.showinfo(f"SHA256: {fileName}", f"{sha256sum(fileName)}")
        if hashtype == "md5":
            debugMessage(f"Viewed {hashtype} hash.")
            messagebox.showinfo(f"MD5: {fileName}", f"{md5sum(fileName)}")
    except TclError:
        messagebox.showerror("Hash", "Cannot show hash. Did you select a file?")

def onClosing():
    global restoreSession
    if restoreSession:
        prev["NAVIGATION"]["Folder"] = global_var.currentPathString
        for i in range(1,10):
            prev["FAVORITES"][f"folder{i}"] = global_var.currentListingEngine.eval(global_var.favoritesList[i-1])
        with open(os.path.join(scriptLocation, ".session.ini"), "w") as saveSession:
            prev.write(saveSession)
    mainWin.destroy()

def setFavorite(index):
    global_var.favoritesList[index] = global_var.currentListingEngine.eval(global_var.currentPathString)
    favoritesMenu.entryconfig(index, label=global_var.currentListingEngine.eval(global_var.currentPathString) + " " * 50 + f"Alt+{index + 1}")

    debugMessage(f"Set {global_var.currentListingEngine.eval(global_var.currentPathString)} to folder{index + 1}")

def focusOnPathEntry():
    pathEntry.focus()
    return "break"

def fileSelectByFirstChar(character):
    fileStartsWithCharList = [file for file in global_var.currentFileList if file.startswith(character)]
    currentSelectionIndex = global_var.currentFileList.index(fileListBox.selection_get())
    if fileStartsWithCharList:
        try:
            for index in range(currentSelectionIndex+1, len(global_var.currentFileList)):
                if global_var.currentFileList[index] in fileStartsWithCharList:
                    fileListBox.selection_clear(0, tk.END)
                    fileListBox.selection_set(index)
                    fileListBox.see(index)
                    fileListBox.activate(index)
                    break
                # Circular Loop
                for index in range(0, len(global_var.currentFileList)):
                    if global_var.currentFileList[index] in fileStartsWithCharList:
                        fileListBox.selection_clear(0, tk.END)
                        fileListBox.selection_set(index)
                        fileListBox.see(index)
                        fileListBox.activate(index)
                        break
        except:
            debugMessage("Error in fileSelectByFirstChar function.")

def setCustomScript(index):
    realScriptName = os.path.join(global_var.currentPathString, global_var.currentListingEngine.inveval(fileListBox.selection_get()))
    global_var.customScripts[index] = global_var.currentListingEngine.eval(realScriptName)
    customScriptMenu.entryconfig(index, label=global_var.currentListingEngine.eval(realScriptName) + " " * 50 + f"Ctrl+Numpad {index + 1}")
    debugMessage(f"Set {global_var.currentListingEngine.eval(realScriptName)} to script{index+1}")

def runCustomScript(index):
    subprocess.run([global_var.currentListingEngine.inveval(global_var.customScripts[index])])
    updateFileList()
    debugMessage(f"Running {global_var.customScripts[index]}")

if __name__ == "__main__":

    argc = len(sys.argv)

    # Configuration & Initialization
    config = configparser.ConfigParser()
    config.read(os.path.join(scriptLocation, "pb.conf"))
    windowSize = config["DEFAULT"]["WindowSize"]
    pathEntryWidth = int(config["DEFAULT"]["PathEntryWidth"])
    imagePreviewWidth = int(config["DEFAULT"]["ImagePreviewWidth"])
    imagePreviewHeight = int(config["DEFAULT"]["ImagePreviewHeight"])
    restoreSession = bool(config["DEFAULT"]["RestoreSession"])
    debugOnScreen = bool(config["DEFAULT"]["DebugOnScreen"])
    fgColor = config["THEME"]["fg"]
    bgColor = config["THEME"]["bg"]
    folderColor = config["THEME"]["folder"]
    global_var.extensionLaunchDict = config["ACTION"]

    #Restoring session if restoreSession = True
    if restoreSession:
        prev = configparser.ConfigParser()
        prev.read(os.path.join(scriptLocation, ".session.ini"))
        global_var.currentPathString = prev["NAVIGATION"]["Folder"]
        if not os.path.isdir(global_var.currentPathString):
            global_var.currentPathString = scriptLocation
        os.chdir(global_var.currentPathString)

    if argc > 1 and os.path.isdir(sys.argv[1]):
            global_var.currentPathString = os.path.realpath(sys.argv[1])
            os.chdir(global_var.currentPathString)

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
    upFolderButton = tk.Button(master=navigatorFrame, text="Up Folder", fg=fgColor, bg=bgColor, command=lambda: navigateDirectory(os.path.dirname(global_var.currentPathString)), takefocus=False)

    locationLabel.grid(row=0,column=0)
    pathEntry.grid(row=0,column=1)
    pathEntry.insert(0, global_var.currentListingEngine.eval(global_var.currentPathString))
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

    # Debug Frame
    debugFrame = tk.Frame(master=mainWin, bg=bgColor)
    debugStringVar = tk.StringVar()
    debugStringVar.set("Debug: ")
    debugLabel = tk.Label(textvariable=debugStringVar, justify="left", fg=fgColor, bg=bgColor)
    
    debugLabel.pack(side="left")
    debugFrame.pack(fill=tk.X, expand=False, side="bottom")
    if debugOnScreen == False:
        debugLabel.forget()
        debugFrame.forget()
    

    # Menu Bar
    menubar = tk.Menu(mainWin, fg=fgColor, bg=bgColor)
    # File Menu
    fileMenu = tk.Menu(menubar, tearoff=0)
    fileMenu.add_command(label="New folder" + " " * 50 + "Ctrl+N", command=lambda: newFolder())
    fileMenu.add_command(label="Open", command=lambda: navigateDirectory(global_var.currentListingEngine.inveval(os.path.join(global_var.currentPathString, fileListBox.selection_get()))))
    #fileMenu.add_command(label="Properties")
    #fileMenu.add_separator()
    #fileMenu.add_command(label="Recent Files")
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
            return lambda: navigateDirectory(global_var.currentListingEngine.inveval(global_var.favoritesList[x-1]))
        favoritesMenu.add_command(label=f"Folder {i}" + " " * 50 + f"Alt+Ctrl+{i} to set favorite.", command = lambdaNavigateFavorites(i))
    
    # Restore favorites
    if restoreSession:
        for i in range(9):
            if prev["FAVORITES"][f"folder{i+1}"] != ".":
                favoritesMenu.entryconfig(i, label=global_var.currentListingEngine.eval(prev["FAVORITES"][f"folder{i+1}"]) + " " * 50 + f"Alt+{i+1}")
                global_var.favoritesList.append(global_var.currentListingEngine.eval(prev["FAVORITES"][f"folder{i+1}"]))
            else:
                global_var.favoritesList.append(".")
    menubar.add_cascade(label="Favorites", menu=favoritesMenu)
    # Custom Scripts Menu
    customScriptMenu = tk.Menu(menubar, tearoff=0)
    #customScriptMenu.add_command(label="Script 1")
    for i in range(1,10):
        def lambdaRunCustomScript(x):
            return lambda: runCustomScript(global_var.customScripts[x-1])
        customScriptMenu.add_command(label=f"Script {i}" + " " * 50 + f"Alt+Ctrl+Numpad {i} to set custom script.", command = lambdaRunCustomScript(i))
    menubar.add_cascade(label="Custom Scripts", menu=customScriptMenu)

    # Restore Custom Scripts
    if restoreSession:
        for i in range(9):
            if prev["CUSTOMSCRIPTS"][f"script{i+1}"] != ".":
                global_var.customScripts.append(global_var.currentListingEngine(prev["CUSTOMSCRIPTS"][f"folder{i+1}"]))
            else:
                global_var.customScripts.append(".")

    # Plugin Menu
    pluginMenu = tk.Menu(menubar, tearoff=0)
    for pluginName in pluginDictionary.keys():
        def lambdaRunPlugin(name):
            return lambda: pluginDictionary[name][0].use()
        pluginMenu.add_command(label=pluginName, command = lambdaRunPlugin(pluginName))
    menubar.add_cascade(label="Plugins", menu=pluginMenu)

    mainWin.config(menu=menubar)
    # Bindings

    # Property Update
    # At every selection, the property summary gets updated.
    fileListBox.bind("<<ListboxSelect>>", lambda event: property_summary())
    # Create directory
    fileListBox.bind("<Control-KeyPress-n>", lambda event: newFolder())
    # Navigate directory / Open file
    # Double click and Enter for navigation
    fileListBox.bind("<Double-1>", lambda event: navigateDirectory(global_var.currentListingEngine.inveval(os.path.join(global_var.currentPathString, fileListBox.selection_get()))))
    fileListBox.bind("<Return>", lambda event: navigateDirectory(global_var.currentListingEngine.inveval(os.path.join(global_var.currentPathString, fileListBox.selection_get()))))
    pathEntry.bind("<Return>", lambda event: navigateDirectory(global_var.currentListingEngine.inveval(pathEntry.get())))
    # Refresh fileListBox
    mainWin.bind("<F5>", lambda event: [updateFileList(), debugMessage("fileListBox refreshed.")])
    # Escape for upper folder
    fileListBox.bind("<Escape>", lambda event: navigateDirectory(os.path.dirname(global_var.currentPathString)))
    pathEntry.bind("<Escape>", lambda event: navigateDirectory(os.path.dirname(global_var.currentPathString)))
    # Autocompletion for Folders
    pathEntry.bind("<Tab>", lambda event: autoCompletePath())
    # Listbox Cursor Movement
    # HOME for the first item
    fileListBox.bind("<Home>", lambda event: [fileListBox.select_clear(0, tk.END), fileListBox.selection_set(0), fileListBox.see(0), fileListBox.activate(0)])
    # END for the last item
    fileListBox.bind("<End>", lambda event: [fileListBox.select_clear(0, tk.END), fileListBox.selection_set(tk.END), fileListBox.see(tk.END), fileListBox.activate(tk.END)])
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
    # Delete file
    fileListBox.bind("<Delete>", lambda event: fileActionDelete())
    # Copy file
    fileListBox.bind("<Control-KeyPress-c>", lambda event: addFileToClipboard())
    # Cut file
    fileListBox.bind("<Control-KeyPress-x>", lambda event: cutAddFileToClipboard())
    # Paste file
    fileListBox.bind("<Control-KeyPress-v>", lambda event: pasteFile())
    # Favorites (Adding to Favorite and navigation) & Custom Scripts
    for i in range(9):
        def lambdaSetFavorite(x):
            return lambda event: setFavorite(x-1)
        def lambdaNavigateFavorite(x):
            return lambda event: navigateDirectory(global_var.currentListingEngine.inveval(global_var.favoritesList[x-1]))
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
    
    # WIDGET VARIABLES
    # Expose widget variables to global_var for easing plugin development
    # (Add this part as needed in a similar fashion, while declaring the variables in global_var.py file.)
    global_var.fileListBox = fileListBox
    global_var.debugStringVar = debugStringVar



    mainWin.mainloop()

