from libc.limits cimport INT_MAX, INT_MIN
from random import random

cdef class _node:
    cdef public int key
    cdef public int value
    forward = []

    def __init__(self, int key, int value):
        self.key = key
        self.value = value
         
    def printNode(n):
        print "k:" + str(n.key) + ", v:" + str(n.value)

    def printNodeWithList(self):
        self.printNode()
        for n in self.forward:
            n.printNode()

cdef class skipList:
    cdef double p
    cdef int level
    cdef int nodes
    cdef public _node HEADER, NIL
    cdef int maxLevel

    #Note: level assumes counting notation starts from 0, maxLevel from 1
    def __init__(self, double p, int maxLevel):
        self.p = p
        self.maxLevel = maxLevel
        self.nodes = 0 
        self.HEADER = _node(INT_MIN, 0)
        self.NIL = _node(INT_MAX, 0)
        self.level = 0
        # Note: we start from level 0 (not 1 as in the paper)
        cdef int i
        for i in range(maxLevel):
            self.HEADER.forward.append(self.NIL)

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
            level += 2 #Just a test, must be 1
        return level
             
    def insert(self, int key, int value):
        update = []
        x = self.HEADER
        for i in range(self.level, -1, -1):
            while x.forward[i].key < key:
                print "Inside while"
                x = x.forward[i]
            update.append(x)
        update.reverse()
        
        if self.nodes != 0:
            x = x.forward[0]
        else:
            print "Inserting first node"
             
        print "Level 0 predecessor: "
        x.printNode()
         
        if x.key == key:
            print "Key already present, updating value"
            x.value = value
        else:
            lvl = self.randomLevel()
            print "Random level selected: " + str(lvl)
            if lvl > self.level:
                for i in range(self.level + 1, lvl + 1):
                    update.append(x)
                self.level = lvl
            print "printing update list"
            for n in update:
                print "k: " + str(n.key) + ", v: " + str(n.value)
                 
            x = _node(key, value)
            print "Node created"
            x.printNode()

            for i in range (self.level + 1):
                print "i = " + str(i)
                print "update[i].forward[i]"
                update[i].forward[i].printNode()
                x.forward.append(update[i].forward[i])
                print "x.forward[i]"
                x.forward[i].printNode()
                print "Node appended"
                 
                update[i].forward[i] = x
                print "update[i].forward[i]"
                update[i].forward[i].printNode()
                print "update[i].forward[i].forward[i]"
                update[i].forward[i].forward[i].printNode()
                print "x.forward[i]"
                x.forward[i].printNode()
                print "Forward node updated"

                x.forward[i].printNode()
                print "Node appended"
            self.nodes += 1

            # print "printing update list"
            # for n in update:
            #     n.printNodeWithList()
                 
