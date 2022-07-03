import shutil
from pbPlugin.plugin import Plugin
import random as rd
import string
import global_var
import os
import subprocess

from peanutbutter import debugMessage

def tmpfsCopyRead():
    N = 10
    tmpfs = "/tmp"

    debugStringVar = global_var.debugStringVar


    assignedName = ''.join(rd.choices(string.ascii_uppercase + string.digits, k=N))
    fileName = global_var.currentListingEngine.inveval(global_var.fileListBox.selection_get())
    fileNameWithoutExt, ext = os.path.splitext(fileName)
    shutil.copy(fileName,os.path.join(tmpfs, assignedName) + f"{ext}")
    debugMessage(f"Copied {fileName} to {tmpfs}.")    
    subprocess.call(["xdg-open", os.path.join(tmpfs, assignedName) + f"{ext}"])


tempfsReadPlugin = Plugin("Copy to tempfs with obscured name, and read from it.", "tmpfs_read.py", tmpfsCopyRead, comment="Copies a file to tmpfs with obscured name and any record of that file being accessed will be erased in the next reboot.")