# This is a dictionary of the form {PluginName: PluginObject} to keep track of which plugins there are.
pluginDictionary = {}

# Example:
# Suppose there is a file pbPlugin/plugin1.py containing a function pluginfunction1, and you wish to call it
# Plugin 1. You can define the plugin by:
# plugin1 = Plugin("Plugin 1", "plugin1.py", "pluginfunction1", comment="This is a plugin that does something.")
class Plugin():
    def __init__(self, name, pluginFile, pluginFunction, comment=""):
        global pluginDictionary
        self.name = name
        self.pluginFile = pluginFile
        self.pluginFunction = pluginFunction
        self.comment = comment
        pluginDictionary[name] = [self, name, pluginFile, pluginFunction, comment]

# Consult the sample plugin local_dupe_check.py that is included.