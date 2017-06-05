from libc.limits cimport UINT_MAX
from libc.stdlib cimport srand, rand, RAND_MAX
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
# To generate a random seed for the rand c function
from random import randint

srand(randint(0, RAND_MAX))

cdef struct node:
    unsigned int key
    unsigned int value
    node *forward [200]

cdef node* newNode(key, value):
    n = <node *>PyMem_Malloc(sizeof(node))
    n.key = key
    n.value = value
    return n

cdef class SkipList:
    cdef public unsigned short maxLevel, level
    cdef readonly float p
    cdef node *HEADER
    cdef node *NIL
    cpdef readonly unsigned int MIN_KEY_VALUE
    cpdef readonly unsigned MAX_KEY_VALUE

    def __cinit__(self, float p, unsigned short maxLevel = 1):
        if maxLevel < 1 or p < 0:
            raise ValueError("Illegal constructor value")

        self.p        = p
        self.maxLevel = maxLevel
        self.level    = 0
        self.MIN_KEY_VALUE = 1
        self.MAX_KEY_VALUE = UINT_MAX - 2
        self.HEADER   = newNode(self.MIN_KEY_VALUE, 0)
        self.NIL      = newNode(self.MAX_KEY_VALUE, 0)

        cdef unsigned short i
        for i in range(self.maxLevel):
            self.HEADER.forward[i] = self.NIL
            self.NIL.forward[i] = NULL

    cpdef print_level(self, int lvl):
        cdef node *toPrint = self.HEADER
        print("--- Level {} ---".format(lvl))
        while toPrint != NULL:
            print("\t--- Node ---  k: {}, v: {}".format(toPrint.key, toPrint.value))
            toPrint = toPrint.forward[lvl]

    cpdef print_list(self):
        for i in range(self.level + 1):
            self.print_level(i)

    cdef unsigned short _random_level(self):
        cdef unsigned short level = 0
        cdef float random = int(rand()) / int(RAND_MAX)

        while random < self.p and level < self.maxLevel - 1:
            level += 1
            random = int(rand()) / int(RAND_MAX)
        return level

    cpdef bint insert(self, unsigned int key, int value):
        if key < self.MIN_KEY_VALUE  or key > self.MAX_KEY_VALUE:
            raise ValueError("Illegal key value")

        cdef node *update[200]
        cdef unsigned short i
        
        for i in range(self.level):
            update[i]=self.NIL

        cdef node *x = self.HEADER

        for i in range(self.level, -1, -1):
            while x.forward[i].key < key:
                x = x.forward[i]
            update[i] = x

        cdef unsigned short lvl = self._random_level()

        if x.key == key:
            x.value = value
            return False
        else:
            x = newNode(key, value)
            if lvl > self.level:
                i = 0
                for i in range(self.level + 1, lvl + 1):
                    update[i]=self.HEADER
                self.level = lvl
            i = 0
            for i in range (lvl + 1):
                    x.forward[i] = update[i].forward[i]
                    update[i].forward[i] = x
            return True

    cpdef unsigned int search(self, unsigned int key):
        if key < self.MIN_KEY_VALUE  or key > self.MAX_KEY_VALUE:
            raise ValueError("Illegal key value")

        cdef node *x = self.HEADER

        cdef unsigned short i = self.level
        for i in range(self.level, -1, -1):
            while x.forward[i].key < key:
                x = x.forward[i]
        x = x.forward[0]
        if x.key == key:
            return x.value
        else:
            return -1

    cpdef bint delete(self, unsigned int key):
        if key < self.MIN_KEY_VALUE  or key > self.MAX_KEY_VALUE:
            raise ValueError("Illegal key value")

        cdef node *update[200]
        cdef unsigned short i
        
        for i in range(self.level):
            update[i]=self.NIL

        cdef node *x = self.HEADER

        for i in range(self.level, -1, -1):
            while x.forward[i].key < key:
                x = x.forward[i]
            update[i] = x

        if x.key == key:
            for i in range(0, self.level):
                if update[i].forward[i] != x: break
                update[i].forward[i] = x.forward[i]
            while self.level > 0 and self.HEADER.forward[self.level] == self.NIL:
                self.level -=1
            PyMem_Free(x)
            return True
        else:
            return False
