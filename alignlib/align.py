
# Given two string lists of same number of entries, this function returns an array of
# concatenated strings, but padded whitespaces in the middle.
def alignList(strList1, strList2, padding=10):
    lengths = [len(strList1[i]) + len(strList2[i]) for i in range(len(strList1))]
    lenWithoutPadding = max(lengths)

    retList = []
    for i in range(len(strList1)):
        retList.append(strList1[i] + " " * (lenWithoutPadding - len(strList1[i]) - len(strList2[i]) + padding) + strList2[i])
    
    return retList