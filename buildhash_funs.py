def fix_inpt(func):
    def decorator(*args, **kwargs):
        if type(args[0]) != str:
            pass
        return fucn(*args, **kwargs)
    return decorator

def FirstLetter(record):
    return ord(record.fname[0])

def CountLetters(record):
    return len(record.fname)

def SumName(record):
    return sum(map(ord, list(record.fname)))

def SumNames(record):
    return sum(map(ord, list(record.fname + record.lname)))

def SID(record):
    return int(record.sid)

def Phone(record):
    return sum([int(x) for x in list(record.phone) if x.isnumeric()])

methods = (FirstLetter, CountLetters, SumName, SumNames, SID, Phone)
