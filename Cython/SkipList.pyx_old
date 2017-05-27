from libc.limits cimport INT_MAX, INT_MIN
from random import random

cdef class _node:
    cdef public int key
    cdef public int value

    #Height start counting by 1
    def __init__(self, int key, int value = 0, int height = 0):
        print "Creating node with height " + str(height)
        self.key = key
        self.value = value
        self.forward = []
        #self.forward = [0] * height
        print "Printing forward" + str(self.forward)
                                    
    def printNode(_node n):               
        print "k:" + str(n.key)     + ", v:" + str(n.value)

    def printNodeWithAdjacent(self):
        self.printNode()
        print "Adjacent element, level 0 to (excluded): " + str(len(self.forward))
        for n in self.forward:
            n.printNode()

cdef class skipList:
    cdef readonly double p
    cdef readonly _node HEADER, NIL
    cdef int level
    cdef int maxLevel

    #Note: level assumes counting notation starts from 0, maxLevel from 1
    def __init__(self, double p, int maxLevel):
        print "Initializing skip list"
        self.p = p
        self.maxLevel = maxLevel
        self.level = 0
        self.HEADER = _node(INT_MIN, 0, 0)
        self.NIL = _node(INT_MAX, 100, 0)
        # Note: we start from level 0 (not 1 as in the paper)
        cdef int i
        for i in range(maxLevel):
            self.HEADER.forward.append(self.NIL)
        self.printList()

    def printList(self):
        print "SKIPLIST\n" + "Max level = " + str(self.maxLevel) + ", Level = " + str(self.level) + "\n"
        for i in range(self.maxLevel): 
            self.printLevel(i)

    def printLevel(self, l):
        if l >= self.maxLevel:
            raise ValueError("Level greater than MaxValue")

        print  "Printing Level = " + str(l)
        y = self.HEADER
        y.printNode()
        while y.forward[l] != self.NIL:
            y.forward[l].printNode()
            y = y.forward[l]
        y.forward[l].printNode()
        print ""
         
    def randomLevel(self):
        cdef int level = 0
        while random() < self.p and level < self.maxLevel:
            level += 1
        return level
             
    def updateList(self, int key):
        update = [None] * (self.level + 1)
        x = self.HEADER
        for i in range(self.level, -1, -1):
            while x.forward[i].key < key:
                print "Inside while"
                x = x.forward[i]
            update[i] = x
        print "***Printing update list"
        for n in update:
            n.printNodeWithAdjacent()
        print "***End update list"
        return update
         
    def insert(self, int key, int value):
        if key <= INT_MIN or key >= INT_MAX:
            raise ValueError("Illegal key value")
        
        update = self.updateList(key)
        if update[0].forward[0].key != self.NIL.key:
            x = update[0].forward[0]
        else:
            print "Inserting first node"
            x = self.HEADER
             
        print "Level 0 predecessor: "
        x.printNode()
         
        if x.key == key:
            print "Key already present, updating value"
            x.value = value
        else:
            lvl = self.randomLevel()
            print "Random level selected " + str(lvl)
            node = _node(key, value, lvl + 1)
    
            if lvl > self.level:
                for i in range(self.level + 1, lvl + 1):
                    update.append(self.HEADER)
                self.level = lvl
                 
            print "***Printing update list"
            for n in update:
                n.printNodeWithAdjacent()
            print "***End update list"
             
            for i in range (self.level + 1):
                print "Iteration " + str(i)
                print "update[i].forward[i] node before append"
                update[i].forward[i].printNodeWithAdjacent()
                x.forward[i] = update[i].forward[i]
                print "Node appended, printing node"
                x.printNodeWithAdjacent()
                 
                print "update[i].forward[i] node after append, before update"
                update[i].forward[i].printNodeWithAdjacent()
                update[i].forward[i] = x
                print "Forward node updated, printing node"
                 
                x.printNodeWithAdjacent()

            # print "printing update list"
            # for n in update:
            #     n.printNodeWithAdjacent()
                 
