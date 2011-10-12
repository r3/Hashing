import rehash_funs
import buildhash_funs
import sys

class Record():
    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def __str__(self):
        return '{fname} {lname}\t{sid}\t{phone}'.format(**self.__dict__)

class RDict():
    def __init__(self, size=42):
        self._values = [None] * size
        self._size = size
        self._used = 0
        self._rehash = rehash_funs.Add11
        self._buildhash = buildhash_funs.SID
        self._cost = 0

    def __getitem__(self, index):
        return self._values[index]
        
    def __setitem__(self, index, item):
        self._values[index] = item

    def __delitem__(self, index):
        self._values[index] = None
        self._used -= 1

    def __iter__(self):
        return iter(self._values)

    @property
    def _saturation(self):
        return self._used / self._size

    def _grow(self):
        contains = [x for x in self._values if x != None]
        cost = 0

        self._size *= 2
        self._values = [None] * self._size

        for item in contains:
            cost = self.insert(item)
        #print("Growing, cost of {} incurred.".format(cost))

    def _at(self, hsh):
        return hsh % self._size

    def table_size(self):
        return '{} bytes'.format(self.__sizeof__())

    def insert(self, item):
        cost = 0  # Per insertion cost
        if self._saturation > 0.75:
            self._grow()
        hsh = self._buildhash(item)
        sig = self._at(hsh)
        tries = [sig]
        while self._values[sig] != None:
            self._cost += 1
            cost += 1
            sig = self._at(self._rehash(sig))
            if sig in tries:
                self._cost += 100  # Record could not be inserted.
                cost += 100
                break
            else:
                tries.append(sig)
        self._values[self._at(sig)] = item
        self._used += 1
        return cost

def parse_records(txt, table):
    with open(txt) as records:
        for record in records:
            if not record.isspace() and not record.startswith('//'):
                (fname, lname, sid, phone, height, bday, prog_pts, exam_pts,
                 part_pts) = record.split()
                table.insert(Record(fname=fname, lname=lname, sid=sid,
                                    phone=phone, height=height, bday=bday, 
                                    prog_pts=prog_pts, exam_pts=exam_pts,
                                    part_pts=part_pts))
        print("The cost of building table was {}.\n".format(table._cost))

def manual_insert(table, index, **kwargs):
    table[index] = Record(**kwargs)

def dump_table(table):
    for num, item in enumerate(table):
        if item != None:
            print('{}: {}'.format(num, item))

def test_methods(txt, output=None):
    def build_instance():
        for buildhash in buildhash_funs.methods:
            for rehash in rehash_funs.methods:
                instance = RDict()
                setattr(instance, '_buildhash', buildhash)
                setattr(instance, '_rehash', rehash)
                yield (buildhash.__name__, rehash.__name__), instance

    if output != None:
        sys.stdout = output

    for algos, test in build_instance():
        print(("Using initial hashing algorithm: {} and rehashing" +
              " algorithm: {}").format(*algos))
        parse_records(txt, test)

if __name__ == '__main__':
    if len(sys.argv) < 1:
        table = RDict()
        dump_table(table)
        manual_insert(table, 13, fname='Tom', lname='Mix', sid=12345678,
                      phone='360-360-3603', height=185, bday=277, prog_pts=0,
                      exam_pts=0, part_pts=0)
        manual_insert(table, 29, fname='Tom', lname='Thumb', sid=54352671,
                      phone='360-123-4567', height=83, bday=177, prog_pts=0,
                      exam_pts=0, part_pts=0)
        dump_table(table)
    else:
        test_methods(sys.argv[1])
