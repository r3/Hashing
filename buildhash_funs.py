def FirstLetter(record):
    return ord(record.fname[0])

def CountLetters(record):
    return len(record.fname)

def SumName(record):
    return sum(map(ord, list(record.fname)))

def SumNames(record):
    return sum(map(ord, list(record.fname + record.lname)))

def SID(record):
    return record.sid

def Phone(record):
    return sum([str(x) for x in list(record.phone) if x.isnumeric()])

methods = (FirstLetter, CountLetters, SumName, SumNames, SID, Phone)
