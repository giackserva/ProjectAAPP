import random
import  numpy as np
import time
import skiplist_no_log as skiplist
import cProfile, pstats
import logging
import io
#import os

MAX_LEVEL      = 10
MIN_N_OF_NODES = 50
MAX_N_OF_NODES = 2**MAX_LEVEL

def vectorized_insert(skiplist, n_of_nodes, nodes_keys):
    t0 = time.perf_counter()
    for k in np.nditer(nodes_keys):
        skiplist.insert(k, 0)
    t1 = time.perf_counter()
    return t1-t0

def search_list(skiplist, keys):
    t0 = time.perf_counter()
    for k in np.nditer(keys):
        skiplist.search(k)
    t1 = time.perf_counter()
    return t1-t0

def delete_list(skiplist, keys):
    t0 = time.perf_counter()
    for k in np.nditer(keys):
        skiplist.delete(k)
    t1 = time.perf_counter()
    return t1-t0
    
def basic_profile(number_of_nodes, max_level, p):
    path = './basic_profile/ml_{:0>2}_n_{:0>8}_p_{}.log'.format(max_level, number_of_nodes, p)
    logging.basicConfig(filename=path, filemode='w', level=logging.INFO)
    sl = skiplist.SkipList(p, max_level)
    n_of_nodes = number_of_nodes
    logging.debug("Trying insert with n of nodes = %d ", n_of_nodes)
    nodes_keys = np.random.randint(sl.MIN_KEY_VALUE,
                                   sl.MAX_KEY_VALUE, 
                                   size=n_of_nodes)
    t = vectorized_insert(sl, n_of_nodes, nodes_keys)
    logging.info('CPU time for Python insert: %.3fs', t)
    
    # we want to search for 10% of all keys in the ndarray of keys
    #step = n_of_nodes / 10
    #search_list(sl, nodes_keys[0:n_of_nodes:int(step)])
    t = search_list(sl, np.random.permutation(nodes_keys))
    logging.info('CPU time for Python search: %.3fs', t)

    t = delete_list(sl, np.random.permutation(nodes_keys))
    logging.info('CPU time for Python delete: %.3fs', t)

def deep_profile(number_of_nodes, max_level, p):
    path = 'deep_profile/ml_{:0>2}_n_{:0>8}_p_{}.log'.format(max_level, number_of_nodes, p)
    stream = io.open(path, 'w')
    # cProfile.run('basic_profile()')
    cProfile.runctx('basic_profile(number_of_nodes, max_level, p)', globals(), locals(), '.prof')
    s = pstats.Stats('.prof', stream=stream)
    s.strip_dirs().sort_stats('time').print_stats(30)
    #os.system('espeak "your program has finished"')

# n = 0 for basic_profile, 1 for deep_profile
def multiple_profiling(n):
    p = 0.5
    max_max_level = 16
    min_n_of_nodes = max_max_level
    max_n_of_nodes = 2**max_max_level

    if n == 0:
        print('Basic profile starting')
        for i in range(max_max_level, 0, -1):
            #n of nodes
            for j in range(max_n_of_nodes, min_n_of_nodes - 1, -1):
                basic_profile(j, i, p)
    elif n == 1:
        print('Deep profile starting')
        for i in range(max_max_level, 0, -1):
            #n of nodes
            for j in range(max_n_of_nodes, min_n_of_nodes - 1, -1):
                deep_profile(j, i, p)
    else:
        print('error, illegal value {}'.format(n))
