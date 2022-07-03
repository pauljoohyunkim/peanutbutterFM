from pbPlugin.plugin import Plugin
import random as rd
import string
import global_var
import os

def tmpfsCopyRead():
    N = 10
    assignedName = ''.join(rd.choices(string.ascii_uppercase + string.digits, k=N))
    fileName = global_var.currentListingEngine.inveval(global_var.fileListBox.selection_get())
    ext = os.path.splitext()[-1]

    pass

tempfsReadPlugin = Plugin("Copy to tempfs with obscured name, and read from it.", "tmpfs_read.py", tmpfsCopyRead, comment="Copies a file to tmpfs with obscured name and any record of that file being accessed will be erased in the next reboot.")