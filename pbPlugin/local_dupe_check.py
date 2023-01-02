from pbPlugin.plugin import Plugin
from filelib.hasher import sha256sum
from collections import defaultdict
from tkinter import messagebox
import tkinter as tk
import global_var
import os

# More extensive version of revdict, allowing nonunique mapping
# Consider this a "preimage" instead of inverse.
def revdict2(dictionary):
    invdict = defaultdict(list)
    for key,value in dictionary.items():
        invdict[value].append(key)
    return dict(invdict)


def dupe_check():
    # All the files (not directories) in folder
    files = []
    for root, dirs, names in os.walk(global_var.currentPathString):
        for name in names:
            if os.path.isfile(os.path.join(root,name)):
                files.append(os.path.join(root,name))
    #files = [file for file in os.listdir(global_var.currentPathString) if os.path.isfile(os.path.join(global_var.currentPathString,file))]
    hashdict={}
    for file in files:
        hashdict[file] = sha256sum(os.path.join(global_var.currentPathString,file))
    
    invhashdict = revdict2(hashdict)
    # Only consider entries with more than one hashes
    # Returns a dictionary of the form clashes[hash] = list of files
    clashes = {key:value for key,value in invhashdict.items() if len(value) >= 2}
    if clashes:
        clashInfo = "Following files are duplicate tuples:\n"
        for clashFileList in clashes.values():
            clashInfo += str(clashFileList) + "\n"
        
        messagebox.showinfo(f"Duplicate File Checker: {global_var.currentPathString}", f"{clashInfo}")
    else:
        messagebox.showinfo(f"Duplicate File Checker: {global_var.currentPathString}", "No exact duplicates found!")
    return clashes

localDupeCheckPlugin = Plugin("Check duplicate files in current directory", "local_dupe_check.py", dupe_check, comment="Checks for duplicate files in current directory by comparing SHA256 hashes.")
