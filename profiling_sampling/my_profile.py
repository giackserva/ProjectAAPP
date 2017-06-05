import numpy as np

def vectorized_insert(skiplist, nodes_keys):
    for k in np.nditer(nodes_keys):
        skiplist.insert(k, 0)

def search_list(skiplist, keys):
    for k in np.nditer(keys):
        skiplist.search(k)

def delete_list(skiplist, keys):
    for k in np.nditer(keys):
        skiplist.delete(k)


