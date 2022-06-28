class ListingMap():
    def __init__(self, listingDictionary):
        self.listingDictionary = listingDictionary
    
    def aliases(self):
        return list(self.listingDictionary.keys())
    
    def reals(self):
        return list(self.listingDictionary.values())

    def eval(self, alias):
        return self.listingDictionary[alias]
    
