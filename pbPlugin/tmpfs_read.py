import shutil
from tkinter import messagebox
from pbPlugin.plugin import Plugin
import random as rd
import string
import global_var
import os
import subprocess
import configparser

from peanutbutter import debugMessage

def tmpfsCopyRead():

    # Configurations
    config = configparser.ConfigParser()
    config.read(os.path.join(global_var.scriptLocation,"pbPlugin/tmpfs_read.conf"))
    N = int(config["OPTION"]["len"])
    tmpfs = config["OPTION"]["tmpfs"]
    extDict = {extension:prog for extension,prog in config["EXTENSION"].items()}


    assignedName = ''.join(rd.choices(string.ascii_uppercase + string.digits, k=N))
    fileName = global_var.currentListingEngine.inveval(global_var.fileListBox.selection_get())
    if os.path.isfile(fileName):
        fileNameWithoutExt, ext = os.path.splitext(fileName)
        shutil.copy(fileName,os.path.join(tmpfs, assignedName) + f"{ext}")
        debugMessage(f"Copied {fileName} to {tmpfs}.")
        
        if ext in config["EXTENSION"].keys():
            subprocess.run([config["EXTENSION"][ext], os.path.join(tmpfs, assignedName) + f"{ext}"])
            debugMessage(f"Running from {tmpfs}")
            os.remove(os.path.join(tmpfs, assignedName) + f"{ext}")
            debugMessage(f"{os.path.join(tmpfs, assignedName) + ext} removed.")
        else:
            subprocess.call(["xdg-open", os.path.join(tmpfs, assignedName) + f"{ext}"])
            debugMessage(f"Warning: Because {ext} is not a pre-defined extension, this plugin could not get a blocking signal. Instead, click OK on the info message when you are done with the file.")
            if messagebox.showinfo(f"tmpfs_read", f"Because {ext} is not a pre-defined extension, this plugin could not get a blocking signal. Instead, click OK on the info message when you are done with the file."):
                os.remove(os.path.join(tmpfs, assignedName) + f"{ext}")
                messagebox.showinfo(f"tmpfs_read", f"{os.path.join(tmpfs, assignedName) + ext} removed.")
    else:
        messagebox.showerror(f"tmpfs_read",f"{fileName} is not a file")

tempfsReadPlugin = Plugin("Copy to tempfs with obscured name, and read from it.", "tmpfs_read.py", tmpfsCopyRead, comment="Copies a file to tmpfs with obscured name and any record of that file being accessed will be erased in the next reboot.")
