@classmethod
def FirstLetter(name):
    return ord(name[0])

@classmethod
def CountLetters(name):
    return len(name)

@classmethod
def SumName(name):
    return sum(map(ord, list(name)))

@classmethod
def SumNames(fname, lname):
    return sum(map(ord, list(fname + lname)))

@classmethod
def SID(sid):
    return sid

@classmethod
def Phone(phone):
    return sum([str(x) for x in list(phone) if x.isnumeric()])

methods = (FirstLetter, CountLetters, SumName, SumNames, SID, Phone)
