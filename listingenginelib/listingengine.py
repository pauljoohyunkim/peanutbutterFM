revdict = lambda injectiveDictionary: {val:key for key,val in injectiveDictionary.items()}

class ListingMap():
    def __init__(self, listingDictionary={}):
        self.listingDictionary = listingDictionary
        self.inverseDictionary = revdict(self.listingDictionary)
    
    def aliases(self):
        return list(self.listingDictionary.values())
    
    def reals(self):
        return list(self.listingDictionary.keys())

    def eval(self, real):
        if real in self.listingDictionary.keys():
            return self.listingDictionary[real]
        else:
            return real
    
    def inveval(self, alias):
        if alias in self.inverseDictionary.keys():
            return self.inverseDictionary[alias]
        else:
            return alias

defaultListingEngine = ListingMap()