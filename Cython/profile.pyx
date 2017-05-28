import logging
import skiplist
import random
import  numpy as np
cimport numpy as np
import time
import skiplist

cdef int MAX_LEVEL      = 10
cdef int MIN_N_OF_NODES = 50
cdef int MAX_N_OF_NODES = 2**MAX_LEVEL
DTYPE = np.int
ctypedef np.int_t DTYPE_t

cdef vectorized_insert():
    sl = skiplist.SkipList(0.5, 8)
    #n_of_nodes = random.randint(MIN_N_OF_NODES, MAX_N_OF_NODES)
    n_of_nodes = 50000
    print("Trying insert with n of nodes = " + str(n_of_nodes))

    cdef np.ndarray[DTYPE_t, ndim=1, negative_indices=False, mode='c'] nodes_keys = np.random.random_integers(sl.MIN_KEY_VALUE, sl.MAX_KEY_VALUE, n_of_nodes)

    t0 = time.clock()
    for k in np.nditer(nodes_keys):
        sl.insert(k, 0)
    t1 = time.clock()
    print('CPU time for loops in Python:' + str(t1-t0))

    
if __name__ == '__main__':
    vectorized_insert()
    
cpdef start():
    vectorized_insert()
