revdict = lambda injectiveDictionary: {val:key for key,val in injectiveDictionary.items()}

# funinvfun = (f, f^{-1})       (Function and its inverse)
class ListingMap():
    def __init__(self, listingDictionary={}, funinvfun=(None,None)):
        self.listingDictionary = listingDictionary
        self.inverseDictionary = revdict(self.listingDictionary)
        self.f, self.invf = funinvfun
    
    def aliases(self):
        return list(self.listingDictionary.values())
    
    def reals(self):
        return list(self.listingDictionary.keys())

    def eval(self, real):
        if self.f != None:
            return self.f(real)
        elif real in self.listingDictionary.keys():
            return self.listingDictionary[real]
        else:
            return real
    
    def inveval(self, alias):
        if self.invf != None:
            return self.invf(alias)
        elif alias in self.inverseDictionary.keys():
            return self.inverseDictionary[alias]
        else:
            return alias

defaultListingEngine = ListingMap()
