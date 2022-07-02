# This is a dictionary of the form {PluginName: PluginObject} to keep track of which plugins there are.
pluginDictionary = {}

class Plugin():
    def __init__(self, name):
        global pluginDictionary
        self.name = name
        pluginDictionary[name] = self