import sys
sys.path.insert(0, '../Python')
sys.path.insert(0, '../Cython')
sys.path.insert(0, '../Cython_malloc')
import skiplist_cython as slc
import skiplist as slp
import skiplist_malloc as slm
import random
import  numpy as np
import time
import cProfile, pstats
import io
import os

def vectorized_insert(skiplist, n_of_nodes, nodes_keys):
    for k in np.nditer(nodes_keys):
        skiplist.insert(k, 0)

def search_list(skiplist, keys):
    for k in np.nditer(keys):
        skiplist.search(k)

def delete_list(skiplist, keys):
    for k in np.nditer(keys):
        skiplist.delete(k)

# n is the type of skiplist implementation to use
# 0 for python, 1 for cython, 2 for cython_malloc
def _skiplist_implementation_type_build(n, p, max_level):
    if n == 0:
        sl = slp.SkipList(p, max_level)
    elif n == 1:
        sl = slc.SkipList(p, max_level)
    elif n == 2:
        sl = slm.SkipList(p, max_level)
    else:
        raise ValueError("Choice not valid {}".format(n))
    return sl


def basic_profile(number_of_nodes, max_level, p, n):
    sl = _skiplist_implementation_type_build(n, p, max_level)
    filename = 'basic_profile/{}/{:1.2f}/ml_{:0>2}_n_{:0>8}.log'.format(n, p, max_level, number_of_nodes)
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    nodes_keys = np.random.randint(sl.MIN_KEY_VALUE,
                sl.MAX_KEY_VALUE,
                size=number_of_nodes)
    f = open(filename, 'w')

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


def deep_profile(number_of_nodes, max_level, p, n):
    filename = 'deep_profile/{}/{:1.2f}/ml_{:0>2}_n_{:0>8}.log'.format(n, p, max_level, number_of_nodes)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    stream = io.open(filename, 'w')
    # cProfile.run('basic_profile()')
    cProfile.runctx('basic_profile(number_of_nodes, max_level, p, n)', globals(), locals(), '.prof')
    s = pstats.Stats('.prof', stream=stream)
    s.strip_dirs().sort_stats('time').print_stats(30)
    #os.system('espeak "your program has finished"')

def sampling(number_of_nodes, max_level, p, n):
    filename_for_insert_samples = 'samples/{}/{:1.2f}/insert.csv'.format(n, p)
    filename_for_search_samples = 'samples/{}/{:1.2f}/search.csv'.format(n, p)
    filename_for_delete_samples = 'samples/{}/{:1.2f}/delete.csv'.format(n, p)
    os.makedirs(os.path.dirname(filename_for_insert_samples), exist_ok=True)
    os.makedirs(os.path.dirname(filename_for_search_samples), exist_ok=True)
    os.makedirs(os.path.dirname(filename_for_delete_samples), exist_ok=True)
    
    sl = _skiplist_implementation_type_build(n, p, max_level)
    nodes_keys = np.random.randint(sl.MIN_KEY_VALUE,
                sl.MAX_KEY_VALUE,
                size=number_of_nodes)

    f1 = open(filename_for_insert_samples, 'a')
    t0 = time.perf_counter()
    vectorized_insert(sl, number_of_nodes, nodes_keys)
    t1 = time.perf_counter()
    f1.write('{}, {}, {:4.10f}\n'.format(number_of_nodes, max_level, t1-t0))
    f1.close()

    f2 = open(filename_for_search_samples, 'a')
    perm = np.random.permutation(nodes_keys)
    t0 = time.perf_counter()
    search_list(sl, perm)
    t1 = time.perf_counter()
    f2.write('{}, {}, {:4.10f}\n'.format(number_of_nodes, max_level, t1-t0))
    f2.close()

    f3 = open(filename_for_delete_samples, 'a')
    perm = np.random.permutation(nodes_keys)
    t0 = time.perf_counter()
    delete_list(sl, perm)
    t1 = time.perf_counter()
    f3.write('{}, {}, {:4.10f}\n'.format(number_of_nodes, max_level, t1-t0))
    f3.close()

# t = 0 for basic_profile, 1 for deep_profile
# n = 0, 1, 2 for python, cython, cython_malloc
def multiple_profiling(t, max_max_level, p, n):
    min_n_of_nodes = max_max_level
    max_n_of_nodes = 2**max_max_level

    if t == 0:
        print('Basic profile starting')
        for i in range(max_max_level, 0, -1):
            #n of nodes
            #The idea is to have a sampling on 10% of the range
            for j in range(max_n_of_nodes, min_n_of_nodes - 1, int(max_n_of_nodes / -10)):
                basic_profile(j, i, p, n)
    elif t == 1:
        print('Deep profile starting')
        for i in range(max_max_level, 0, -1):
            #n of nodes
            #The idea is to have a sampling on 10% of the range
            for j in range(max_n_of_nodes, min_n_of_nodes - 1, int(max_n_of_nodes / -10)):
                deep_profile(j, i, p, n)
    elif t == 2:
        print('Sampling enabled')
        for i in range(max_max_level, 0, -1):
            #n of nodes
            #The idea is to have a sampling on 10% of the range
            for j in range(max_n_of_nodes, min_n_of_nodes - 1, int(max_n_of_nodes / -10)):
                sampling(j, i, p, n)
    else:
        print('error, illegal value {}'.format(n))

def all_night_long(max_max_level):
    ps = np.linspace(0.2, 1.0, num=4, endpoint=False)
    for t in range(3):
        for n in range(3):
            for i in range(len(ps)):
                multiple_profiling(t, max_max_level, ps[i], n)

