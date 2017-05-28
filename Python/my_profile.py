import time
import random
import numpy as np
import skiplist

MAX_LEVEL      = 10
MIN_N_OF_NODES = 50
MAX_N_OF_NODES = 2**MAX_LEVEL

def vectorized_insert():
    sl = skiplist.SkipList(0.5, 8)
    
    #n_of_nodes = random.randint(MIN_N_OF_NODES, MAX_N_OF_NODES)
    n_of_nodes = 50000
    print("Trying insert with n of nodes = " + str(n_of_nodes))
    nodes_keys = np.random.randint(sl.MIN_KEY_VALUE,
                                   sl.MAX_KEY_VALUE, 
                                   size=n_of_nodes)
    
    t0 = time.clock()
    for k in np.nditer(nodes_keys):
        sl.insert(k, 0)
    t1 = time.clock()
    print('CPU time for loops in Python:' + str(t1-t0))

def start():
    vectorized_insert()
