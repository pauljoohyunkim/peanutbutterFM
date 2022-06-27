import os
import tkinter as tk

def property_summary(currentPathString, fileListBox,sizeStringVar, modifiedStringVar, createdStringVar, osStatStringVar):
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