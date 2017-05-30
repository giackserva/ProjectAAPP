import random
import  numpy as np
import time
import skiplist_no_log as skiplist
import cProfile, pstats
import io
#import os

MAX_LEVEL      = 10
MIN_N_OF_NODES = 50
MAX_N_OF_NODES = 2**MAX_LEVEL

def vectorized_insert(skiplist, n_of_nodes, nodes_keys):
    for k in np.nditer(nodes_keys):
        skiplist.insert(k, 0)

def search_list(skiplist, keys):
    for k in np.nditer(keys):
        skiplist.search(k)

def delete_list(skiplist, keys):
    for k in np.nditer(keys):
        skiplist.delete(k)


def basic_profile(number_of_nodes, max_level, p):
    path = './basic_profile/ml_{:0>2}_n_{:0>8}_p_{}.log'.format(max_level, number_of_nodes, p)
    f = open(path, 'w')

    sl = skiplist.SkipList(p, max_level)
    nodes_keys = np.random.randint(sl.MIN_KEY_VALUE,
            sl.MAX_KEY_VALUE,
            size=number_of_nodes)
    t0 = time.perf_counter()
    vectorized_insert(sl, number_of_nodes, nodes_keys)
    t1 = time.perf_counter()
    f.write('CPU time for Python insert {:4.10f}\n'.format(t1-t0))

    t0 = time.perf_counter()
    search_list(sl, np.random.permutation(nodes_keys))
    t1 = time.perf_counter()
    f.write('CPU time for Python search {:4.10f}\n'.format(t1-t0))

    t0 = time.perf_counter()
    delete_list(sl, np.random.permutation(nodes_keys))
    t1 = time.perf_counter()
    f.write('CPU time for Python delete {:4.10f}\n'.format(t1-t0))
    f.close()

    # we want to search for 10% of all keys in the ndarray of keys
    #step = n_of_nodes / 10
    #search_list(sl, nodes_keys[0:n_of_nodes:int(step)])


def deep_profile(number_of_nodes, max_level, p):
    path = 'deep_profile/ml_{:0>2}_n_{:0>8}_p_{}.log'.format(max_level, number_of_nodes, p)
    stream = io.open(path, 'w')
    # cProfile.run('basic_profile()')
    cProfile.runctx('basic_profile(number_of_nodes, max_level, p)', globals(), locals(), '.prof')
    s = pstats.Stats('.prof', stream=stream)
    s.strip_dirs().sort_stats('time').print_stats(30)
    #os.system('espeak "your program has finished"')

def sampling(number_of_nodes, max_level, p):
    path_for_insert_samples = 'samples/insert.csv'
    path_for_search_samples = 'samples/search.csv'
    path_for_delete_samples = 'samples/delete.csv'
    sl = skiplist.SkipList(p, max_level)
    nodes_keys = np.random.randint(sl.MIN_KEY_VALUE,
            sl.MAX_KEY_VALUE,
            size=number_of_nodes)

    f1 = open(path_for_insert_samples, 'a')
    t0 = time.perf_counter()
    vectorized_insert(sl, number_of_nodes, nodes_keys)
    t1 = time.perf_counter()
    f1.write('{}, {}, {:4.10f}\n'.format(number_of_nodes, max_level, t1-t0))
    f1.close()

    f2 = open(path_for_search_samples, 'a')
    perm = np.random.permutation(nodes_keys)
    t0 = time.perf_counter()
    search_list(sl, perm)
    t1 = time.perf_counter()
    f2.write('{}, {}, {:4.10f}\n'.format(number_of_nodes, max_level, t1-t0))
    f2.close()

    f3 = open(path_for_delete_samples, 'a')
    perm = np.random.permutation(nodes_keys)
    t0 = time.perf_counter()
    delete_list(sl, perm)
    t1 = time.perf_counter()
    f3.write('{}, {}, {:4.10f}\n'.format(number_of_nodes, max_level, t1-t0))
    f3.close()

# n = 0 for basic_profile, 1 for deep_profile
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
    elif n == 2:
        print('Sampling enabled')
        for i in range(max_max_level, 0, -1):
            #n of nodes
            #The idea is to have a sampling on 10% of the range
            for j in range(max_n_of_nodes, min_n_of_nodes - 1, int(max_n_of_nodes / -10)):
                sampling(j, i, p)
    else:
        print('error, illegal value {}'.format(n))
