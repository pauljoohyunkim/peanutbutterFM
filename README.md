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