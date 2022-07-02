from pbPlugin.plugin import Plugin, pluginDictionary
from filelib.hasher import sha256sum
from collections import defaultdict
#from listingenginelib.listingengine import revdict
import os

# More extensive version of revdict, allowing nonunique mapping
# Consider this a "preimage" instead of inverse.
def revdict2(dictionary):
    invdict = defaultdict(list)
    for key,value in dictionary.items():
        invdict[value].append(key)
    return dict(invdict)


def dupe_check(folder):
    # All the files (not directories) in folder
    files = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder,file))]
    hashdict={}
    for file in files:
        hashdict[file] = sha256sum(os.path.join(folder,file))
    
    invhashdict = revdict2(hashdict)
    # Only consider entries with more than one hashes
    # Returns a dictionary of the form clashes[hash] = list of files
    clashes = {key:value for key,value in invhashdict.items() if len(value) >= 2}
    return clashes


localDupeCheckPlugin = Plugin("Check duplicate files in current directory", "local_dupe_check.py", dupe_check, comment="Checks for duplicate files in current directory by comparing SHA256 hashes.")