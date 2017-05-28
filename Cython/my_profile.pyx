import skiplist
import random
import  numpy as np
cimport numpy as np
import time
import skiplist
import cProfile, pstats
import logging
import io
import os

cdef int MAX_LEVEL      = 10
cdef int MIN_N_OF_NODES = 50
cdef int MAX_N_OF_NODES = 2**MAX_LEVEL
DTYPE = np.int
ctypedef np.int_t DTYPE_t

cdef vectorized_insert(skiplist, n_of_nodes, nodes_keys):
    #n_of_nodes = random.randint(MIN_N_OF_NODES, MAX_N_OF_NODES)
    t0 = time.clock()
    for k in np.nditer(nodes_keys):
        skiplist.insert(k, 0)
    t1 = time.clock()
    logging.info('CPU time for Cython insert: %d', t1-t0)

cdef search_list(skiplist, keys):
    t0 = time.clock()
    for k in np.nditer(keys):
        skiplist.search(k)
    t1 = time.clock()
    logging.info('CPU time for Cython search: %d', t1-t0)

    
cpdef start():
    logging.basicConfig(filename='profile.log', filemode='w', level=logging.INFO)
    sl = skiplist.SkipList(0.5, 16)
    n_of_nodes = 350
    logging.debug("Trying insert with n of nodes = %d ", n_of_nodes)
    cdef np.ndarray[DTYPE_t, ndim=1, negative_indices=False, mode='c'] nodes_keys = np.random.random_integers(sl.MIN_KEY_VALUE, sl.MAX_KEY_VALUE, n_of_nodes)
    vectorized_insert(sl, n_of_nodes, nodes_keys)
    
    # we want to search for 10% of all keys in the ndarray of keys
    step = n_of_nodes / 10
    search_list(sl, nodes_keys[0:n_of_nodes:int(step)])


cpdef deep_profile():
    stream = io.open('profile.log', 'w')
    # cProfile.run('start()')
    cProfile.runctx('start()', globals(), locals(), '.prof')
    s = pstats.Stats('.prof', stream=stream)
    s.strip_dirs().sort_stats('time').print_stats(30)
    os.system('espeak "your program has finished"')
