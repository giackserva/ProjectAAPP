from random import random

class _Node:

    #Height start counting by 1
    def __init__(self, key, value = 0, height = 0):
        print ("Creating node with height ", str(height))
        self.key = key
        self.value = value
        self.forward = [0] * height
        print("Printing forward", str(self.forward))
                                    
    def printNode(n):               
        if isinstance(n, _Node):
            print("Node --- k:", str(n.key), ", v:", str(n.value))
        else:
            print(str(n))

    def printNodeWithAdjacent(self):
        self.printNode()
        print("Adjacent element, level 0 to (excluded): " + str(len(self.forward)))
        for n in self.forward:
            n.printNode()
        print("---End adjacent nodes")


class SkipList:

    #Note: level assumes counting notation starts from 0, maxLevel from 1
    def __init__(self, p, maxLevel):
        print("Initializing skip list")
        self.INT_MIN = -1000
        self.INT_MAX = 1000
        self.p = p
        self.maxLevel = maxLevel
        self.level = 0
        self.HEADER = _Node(self.INT_MIN, 0, 0)
        self.NIL = _Node(self.INT_MAX, 100, 0)
        # Note: we start from level 0 (not 1 as in the paper)
        for i in range(maxLevel):
            self.HEADER.forward.append(self.NIL)
        self.printList()

    def printList(self):
        print("SKIPLIST\n" + "Max level = " + str(self.maxLevel) + ", Level = " + str(self.level) + "\n")
        for i in range(self.maxLevel): 
            self.printLevel(i)

    def printLevel(self, l):
        if l >= self.maxLevel:
            raise ValueError("Level greater than MaxValue")

        print("Printing Level = " + str(l))
        y = self.HEADER
        y.printNode()
        while y.forward[l] != self.NIL:
            y.forward[l].printNode()
            y = y.forward[l]
        y.forward[l].printNode()
        print("---End of Level---")
         
    def randomLevel(self):
        level = 0
        while random() < self.p and level < self.maxLevel - 1:
            level += 1
        return level
             
    def updateList(self, key):
        update = [None] * (self.level + 1)
        x = self.HEADER
        for i in range(self.level, -1, -1):
            while x.forward[i].key < key:
                print("Inside while")
                x = x.forward[i]
            update[i] = x
        print("***Printing update list")
        for n in update:
            n.printNodeWithAdjacent()
        print("***End update list")
        return update
         
    def insert(self, key, value):
        if key <= self.INT_MIN or key >= self.INT_MAX:
            raise ValueError("Illegal key value")
        
        update = self.updateList(key)
        # if update[0].forward[0].key != self.NIL.key:
        #     x = update[0].forward[0]
        # else:
        #     print("Inserting first node")
        #     x = self.HEADER
        x = update[0].forward[0]
             
        print("Level 0 predecessor: ")
        x.printNode()
         
        if x.key == key:
            print("Key already present, updating value")
            x.value = value
        else:
            lvl = self.randomLevel()
            print("Random level selected " + str(lvl))
            x = _Node(key, value, lvl + 1)
    
            if lvl > self.level:
                for i in range(self.level + 1, lvl + 1):
                    update.append(self.HEADER)
                self.level = lvl
                print("***Printing update list")
                for n in update:
                    n.printNodeWithAdjacent()
                print("***End update list")
             
            for i in range (self.level + 1):
                print("Iteration " + str(i))
                # print("update[i].forward[i] node before append")
                # update[i].forward[i].printNodeWithAdjacent()
                x.forward[i] = update[i].forward[i]
                print("Node appended")
                # x.printNodeWithAdjacent()
                 
                # print("update[i].forward[i] node after append, before update")
                # update[i].forward[i].printNodeWithAdjacent()
                update[i].forward[i] = x
                print("Forward node updated")
            
            x.printNodeWithAdjacent()

            # print("printing update list")
            # for n in update:
            #     n.printNodeWithAdjacent()
                 
