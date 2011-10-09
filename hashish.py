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
    def __init__(self, size=30):
        self._values = [None] * size
        self._size = size
        self._used = 0
        self._rehash = rehash_funs.Add11
        self._buildhash = buildhash_funs.SID
        self._count = 0

    def __getitem__(self, index):  # change index to item
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
        self._size *= 2
        for x in range(self._size - len(self._values)):
            self._values.append(None)
        # REHASH!

    def _at(self, hsh):
        return hsh % self._size

    def table_size(self):
        return '{} bytes'.format(self.__sizeof__())

    def get(self, key):
        sig = self._buildhash(key)
        newsig = sig
        while self._buildhash(self._values[self._at(newsig)]) != sig:
            count += 1
            newsig = self._rehash(sig)
        return self._values[self._at(newsig)]

    def insert(self, item):
        if self._saturation > 0.75:
            self._grow()
        sig = self._buildhash(item)
        while self._values[self._at(sig)] != None:
            self._count += 1
            sig = self.rehash(sig)
        self._values[self._at(sig)] = item
        self._used += 1

def parse_records(txt, table):
    with open(txt) as records:
        for record in records:
            if not record.startswith('//'):
                (fname, lname, sid, phone, height, bday, prog_pts, exam_pts,
                 part_pts) = record.split()
                table.insert(Record(fname, lname, sid, phone, height, bday, 
                                      prog_pts, exam_pts, part_pts))

def manual_insert(table, index, **kwargs):
    table[index] = Record(**kwargs)

def dump_table(table):
    for num, item in enumerate(table):
        if item != None:
            print('{}: {}'.format(num, item))

def dump_stats(table):
    # Gather use/performance statistics from table and return them. Placeholder
    return '{}'.format(table.stats)

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
        parse_records(txt, test)
        print("Using initial hashing algorithm: {} and rehashing \
              algorithm: {}".format(*algos))
        print(dump_stats(test))

if __name__ == '__main__':
    print(sys.argv)
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
