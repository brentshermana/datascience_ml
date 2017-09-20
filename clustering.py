import logging

# returns a list of lists. first dimension is the index of the center, the list
def _kmeans_assignments(centers, coords):
    # assign nodes to centers
    assignments = []
    for _ in range(len(centers)):
        assignments.append([])
    for coord in coords:
        mini = -1
        mindist = 100000000
        for ci, center in enumerate(centers):
            dist = _distance(coord, center)
            if dist < mindist:
                mindist = dist
                mini = ci
        assignments[mini].append(coord)
    return assignments

# k = len(starting_centers)
# assume members of 'coords' and 'starting_centers' are lists of size two
# returns new centers (list of 2d lists) and assignments (see _kmeans_assignments)
def kmeans(coords, starting_centers, iterations=100):
    logging.basicConfig()
    centers = starting_centers
    for _ in range(iterations):
        assignments = _kmeans_assignments(centers, coords)
        # get new centers by averaging
        for center_index, assigned_coords in enumerate(assignments):
            sum = [0] * 2
            for coord in assigned_coords:
                sum[0] += coord[0]
                sum[1] += coord[1]
            centers[center_index] = (sum[0] / len(assigned_coords), sum[1] / len(assigned_coords))
    # all done, return the new centers:
    assignments = _kmeans_assignments(centers, coords)
    return (centers, assignments)

def _distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

# returns a list of sets of coord indices. each set is a cluster
def singlelink(coords, k):
    logging.debug("== Single Link Begin ==")

    sorted_indexlist = []
    for x in range(len(coords)):
        for y in range(x): # not len(coords) to avoid building the whole square, which has duplicate info
            sorted_indexlist.append( (x, y) )
    sorted_indexlist = sorted(sorted_indexlist, key=lambda x: _distance(coords[x[0]], coords[x[1]]))

    clusterdict = {} # maps cluster indices to sets of coord indices
    # create disjoint clusters of size one
    assignments = [i for i in range(len(coords))]  # allows conversion from coord index to cluster index
    for i in range(len(coords)):
        ith_set = set()
        ith_set.add(i)
        clusterdict[i] = ith_set

    for closestpair in sorted_indexlist:
        if len(clusterdict.keys()) == k:
            break # have k distinct groups!

        a = closestpair[0]
        b = closestpair[1]
        a_cluster_i = assignments[a]
        if b in clusterdict[a_cluster_i]:
            continue # in same set, don't do anything
        else:
            #get rid of b's cluster, merge its cluster with a's cluster
            b_cluster_i = assignments[b]
            for bi in clusterdict[b_cluster_i]:
                clusterdict[a_cluster_i].add(bi)
                assignments[bi] = a_cluster_i
            del clusterdict[b_cluster_i]

    # return disjoint cluster sets in a list:
    ret = list(clusterdict.values())

    #log the coords for each set
    logging.debug("== Done. Clusters are as follows: ==")
    for s in ret:
        set_list = [coords[i] for i in s]
        logging.debug("== Set: {}".format(set_list))

    return ret