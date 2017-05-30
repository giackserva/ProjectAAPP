import random
import  numpy as np
cimport numpy as np
import time
import skiplist_no_log as skiplist
import cProfile, pstats
import io
#import os

cdef int MAX_LEVEL      = 10
cdef int MIN_N_OF_NODES = 50
cdef int MAX_N_OF_NODES = 2**MAX_LEVEL
DTYPE = np.int
ctypedef np.int_t DTYPE_t

cdef vectorized_insert(skiplist, n_of_nodes, nodes_keys):
    #n_of_nodes = random.randint(MIN_N_OF_NODES, MAX_N_OF_NODES)
    t0 = time.perf_counter()
    for k in np.nditer(nodes_keys):
        skiplist.insert(k, 0)
    t1 = time.perf_counter()
    return t1-t0

cdef search_list(skiplist, keys):
    t0 = time.perf_counter()
    for k in np.nditer(keys):
        skiplist.search(k)
    t1 = time.perf_counter()
    return t1-t0

cdef delete_list(skiplist, keys):
    t0 = time.perf_counter()
    for k in np.nditer(keys):
        skiplist.delete(k)
    t1 = time.perf_counter()
    return t1-t0
    
cpdef basic_profile(number_of_nodes, max_level, p):
    path = './basic_profile/ml_{:0>2}_n_{:0>8}_p_{}.log'.format(max_level, number_of_nodes, p)
    f = open(path, 'w')
    sl = skiplist.SkipList(p, max_level)
    nodes_keys = np.random.randint(sl.MIN_KEY_VALUE,
                                   sl.MAX_KEY_VALUE, 
                                   size=number_of_nodes)
    t = vectorized_insert(sl, number_of_nodes, nodes_keys)
    f.write('CPU time for Python insert {:4.10f}\n'.format(t))
    
    # we want to search for 10% of all keys in the ndarray of keys
    #step = n_of_nodes / 10
    #search_list(sl, nodes_keys[0:n_of_nodes:int(step)])
    t = search_list(sl, np.random.permutation(nodes_keys))
    f.write('CPU time for Python search {:4.10f}\n'.format(t))

    t = delete_list(sl, np.random.permutation(nodes_keys))
    f.write('CPU time for Python delete {:4.10f}\n'.format(t))

    f.close()

cpdef deep_profile(number_of_nodes, max_level, p):
    path = 'deep_profile/ml_{:0>2}_n_{:0>8}_p_{}.log'.format(max_level, number_of_nodes, p)
    stream = io.open(path, 'w')
    # cProfile.run('basic_profile()')
    cProfile.runctx('basic_profile(number_of_nodes, max_level, p)', globals(), locals(), '.prof')
    s = pstats.Stats('.prof', stream=stream)
    s.strip_dirs().sort_stats('time').print_stats(30)
    #os.system('espeak "your program has finished"')

def multiple_profiling(n, max_max_level):
    p = 0.5
    min_n_of_nodes = max_max_level
    max_n_of_nodes = 2**max_max_level

    if n == 0:
        print('Basic profile starting')
        for i in range(max_max_level, 0, -1):
            #n of nodes
            #The idea is to have a sampling on 10% of the range
            for j in range(max_n_of_nodes, min_n_of_nodes - 1, int(max_n_of_nodes / -10)):
                basic_profile(j, i, p)
    elif n == 1:
        print('Deep profile starting')
        for i in range(max_max_level, 0, -1):
            #n of nodes
            #The idea is to have a sampling on 10% of the range
            for j in range(max_n_of_nodes, min_n_of_nodes - 1, int(max_n_of_nodes / -10)):
                deep_profile(j, i, p)
    else:
        print('error, illegal value {}'.format(n))
