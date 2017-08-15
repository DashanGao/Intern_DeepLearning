import numpy as np
from scipy.spatial.distance import pdist
import math
import time

'''
By Gao Dashan 
@ 2017/8/6
What is required: 
    FEATURE : feature gallery
    ranking(g): given query original feature g, return the ranking index list 
    distance(a, b): given two original features, return the Mahalanobis distance between a and b.

How to use: 
    Invoke calculate_jaccard_distance(a, b), given original feature of a and b, 
    return the modified Jaccard diatance. 
'''

k1 = 20  # 20
k2 = 6  # 10
R_star_ratio = 2/3.  # 2/3. * |R(q, 0.5*k)|
R_star_k_ratio = 0.5  # R(q, 0.5*k)
FEATURE = np.load("feature.npy")
# FEATURE = np.load("feature_final.npy")
TOTAL_NUM = FEATURE.shape[0]


def ranking(query_list):
    '''
    Given original feature g, return the ranking of all items
    :param g: original feature
    :return: ranking of all items, by index
    '''

    global FEATURE
    query_list = query_list.reshape(query_list.shape[0], FEATURE.shape[1])
    # num_query = query_list.shape[0]
    # num_set = FEATURE.shape[0]
    # dists = np.zeros((num_query, num_set))
    M = np.dot(query_list, FEATURE.T)
    te = np.square(query_list).sum(axis = 1 )
    tr = np.square(FEATURE).sum(axis = 1 )
    dists = np.sqrt( np.abs( -2*M + tr + np.matrix(te).T ) )
    g = np.argsort( dists )
    return g


def distance(a, b):
    return pdist(np.array([a,b]), 'euclidean', VI=None)


def find_nearest_neighbors(g, k=k1):
    '''
    N(p,k) = {g1, g2, g3 ...., gk}, |N(p,k)| = k
    Find the index of nearest neighbors.

    :param g: feature for query
    :param k: top k items to handle, by defult k = k1 = 20
    :return: index of the top k ranked images  N(p,k)
    '''
    ranking_list = ranking(FEATURE[int(g)].reshape(1, -1))
    nearest_neighbors = ranking_list[:, 0:k + 1]
    res = [value for value in nearest_neighbors.tolist()[0] if value != g][:k]
    return np.array(res, dtype=np.uint32)  # from the second image because the feature of the query is in the FEATURE.


def find_nearest_neighbors_multi(g, k=k1):
    '''
    N(p,k) = {g1, g2, g3 ...., gk}, |N(p,k)| = k
    Find the index of nearest neighbors.

    :param g: feature for query
    :param k: top k items to handle, by defult k = k1 = 20
    :return: index of the top k ranked images  N(p,k)
    '''

    ranking_list = ranking(FEATURE[g].reshape(len(g), -1))
    res = []
    nearest_neighbors = ranking_list[:, 0:k + 1]
    for i in range(len(nearest_neighbors)):
        tmp = [value for value in nearest_neighbors[i].tolist() if value != g[i]][0]
        res.append(tmp[:k])
        # print len(res[i]), "Neighbor's neighbor"
    return np.array(res, dtype=np.uint32)  # from the second image because the feature of the query is in the FEATURE.


def reciprocal(p, k=k1):
    '''
    R(p, k) = {gi | (gi <- N(p,k)) /\ (p <- N(gi, k))}

    :param p: feature of the query
    :param k: top k items
    :param N_p:
    :return: R(p, k)
    '''

    N_p = find_nearest_neighbors(p, k)
    reciprocal_items = None
    for g in np.nditer(N_p):
        N_g = find_nearest_neighbors(g, k)
        if p in N_g:
            if reciprocal_items is None:
                reciprocal_items = np.array(g, dtype=np.uint32, ndmin=1)
            else:
                reciprocal_items = np.append(reciprocal_items, g)
    if reciprocal_items is None:
        reciprocal_items = np.array([])
    return reciprocal_items


def reciprocal_modi(p, k=k1, flag=True):
    '''
    R(p, k) = {gi | (gi <- N(p,k)) /\ (p <- N(gi, k))}

    :param p: feature of the query
    :param k: top k items
    :param N_p:
    :return: R(p, k)
    '''

    N_p = find_nearest_neighbors(p, k)
    reciprocal_items = None
    N_gs = find_nearest_neighbors_multi(N_p.astype(int).tolist(), k)
    for g_index in range(len(N_p)):
        N_g = N_gs[g_index]
        if (flag and g_index < 3) or p in N_g:
            if reciprocal_items is None:
                reciprocal_items = np.array(N_p[g_index], dtype=np.uint32, ndmin=1)
            else:
                reciprocal_items = np.append(reciprocal_items, N_p[g_index])
    if reciprocal_items is None:
        reciprocal_items = np.array([])
    return reciprocal_items


def reciprocal_star(p, k=k1):
    '''
    R*(p, k)

    :param p: query image index
    :param k: top k items to process, by defult k = k1 = 20
    :param N_p: well ranked list by index of each image.
    :return:   R*(p, k)
    '''
    reciprocal_neighbors = reciprocal_modi(p, k)  # reciprocal_neighbors = R(p, k)
    # print reciprocal_neighbors, 'R(p)'
    reciprocal_star_items = reciprocal_neighbors
    for index in range(len(reciprocal_neighbors)):
        item_reciprocal = reciprocal_modi(reciprocal_neighbors[index], int(R_star_k_ratio * k), flag=False)
        diff = list(set(item_reciprocal) - set(reciprocal_neighbors))
        if float(len(diff)) < (1-R_star_ratio)*len(item_reciprocal):
            reciprocal_star_items = np.append(reciprocal_star_items, diff)
    resu = reciprocal_star_items.astype(int)  # index of neighbors
    return list(set(resu.tolist()))

