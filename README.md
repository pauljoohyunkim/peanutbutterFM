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

python peanutbutter.py      # Try python3 instead if you have legacy Python.

```

If you are on Windows, currently a minor tweak is needed. This will be fixed at a later time.

### Configuration
If you open pb.conf, you will various configurations. Try tweaking them to see how it affects the program at launch.

(Currently the repository is still under construction.)

### Some Shortcuts So Far
* [F5] to manually refresh the file list.
* [Esc] to go up a folder.
* While focused on the file list, [Tab] will change your focus back to the path input bar.
* [Home] to go to the first entry in the list. [End] to go to the last entry in the list.
* [Down] key when focused on the path input bar to change your focus to file list.
* Alphabet key to highlight the file or folder that starts with that letter (case sensitive).
* [Delete] key to delete a file or a folder.
* [Ctrl+C] and [Ctrl+V] for copy and paste respectively.
* [Alt+Ctrl+{0123456789}] for setting the current folder as a favorite. [Alt+{0123456789}] for navigating to the assigned favorite folder.
* [Alt+Ctrl+Numpad{0123456789}] for setting the highlighted file as a script that you wish to run by [Ctrl+Numpad{0123456789}].

### Plugin
You can add custom plugins to Peanut Butter FM. In fact, it is extremely easy! (You can look at pbPlugin/local_dupe_check.py for inspiration.)

Basic template that I might start with for writing a plug is:
```
# This is what pbPlugin/template.py might look like.
from pbPlugin.plugin import Plugin  #This defines the class Plugin
import global_var                   #It is likely that you would want
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