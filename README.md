# peatnutbutterFM
File manager that is highly customizable.

![Peanut Butter Icon](peanutbutter.jpg)

## Requirements
* PIL
* tkinter

![Screenshot with DARK MODE](docs/images/Screenshot%20from%202022-06-29%2020-45-26.png)

## To Get Started
Getting started is as easy as simply cloning the repository and running the program.

```
git clone https://github.com/pauljoohyunkim/peanutbutterFM.git

python peanutbutter.py
# Try python3 instead if you have legacy Python.
# If you are given an error that you do not have PIL module, try:
# pip install Pillow
# or
# pip3 install Pillow


```

### Configuration
If you open pb.conf, you will various configurations. Try tweaking them to see how it affects the program at launch.

#### Launch Configuration by File Extension
It is possible to configure what program to run the file with, or even run a script before a file with certain file extension is to be run. Add your own configuration by opening up pb.conf and adding lines under [ACTION]. Use `fileName` as a macro for your file name (which will be replaced every time you run a corresponding file.)

For example, on my Linux machine using Gnome, I added the following to open txt files with vim.
```
[ACTION]
txt = gnome-terminal -- bash -c "vim `fileName`; exec bash"
```

When opening file.txt, file manager will run the command: gnome-terminal -- bash -c "vim file.txt; exec bash" instead.

(Currently the repository is still under construction.)

### Some Shortcuts So Far
* [F5] to manually refresh the file list.
* [Esc] to go up a folder.
* While focused on the file list, [Tab] will change your focus back to the path input bar.
* [Home] to go to the first entry in the list. [End] to go to the last entry in the list.
* [Down] key when focused on the path input bar to change your focus to file list.
* Alphabet key to highlight the file or folder that starts with that letter (case sensitive).
* [Ctrl+n] for creating directory.
* [Delete] key to delete a file or a folder.
* [Ctrl+c], [Ctrl+x] and [Ctrl+v] for copy, cut, and paste respectively.
* [Alt+Ctrl+{0123456789}] for setting the current folder as a favorite. [Alt+{0123456789}] for navigating to the assigned favorite folder.
* [Alt+Ctrl+Numpad{0123456789}] for setting the highlighted file as a script that you wish to run by [Ctrl+Numpad{0123456789}].

### Plugin
You can add custom plugins to Peanut Butter FM. In fact, it is extremely easy! (You can look at pbPlugin/local_dupe_check.py for inspiration. Notice that most of the code is just pure Python code without any obscure library or module!)

Basic template that I might start with for writing a plugin is:
```
# This is what pbPlugin/template.py might look like.
from pbPlugin.plugin import Plugin                          #This defines the class Plugin
import global_var                                           #It is likely that you would want
                                                            #to use some of the global variables...

# What you want your plugin to do.
# Note that your function should not take any arguments,
# as you are trying to make a plugin on a GUI...
def someFunction():
    pass


# This part should help Peanut Butter recognize a new plugin easily.
pluginObj = Plugin("How you want it to show up in the FM", "template.py", someFunction, comment="Description of your plugin")
```

If you ever need to access reference to one of the widgets, see the comment near the bottom of peanutbutter.py on how to do so. (You will be adding one line to each peanutbutter.py and global_var.py for each widget you wish to access.)

