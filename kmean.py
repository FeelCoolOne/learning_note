#!/usr/bin/env python

import numpy as np
import random


def k_mean(X, k=3):
    [n_sample, n_col] = X.shape
    # pick random k means points
    curr_means = X[random.sample(np.arange(n_sample), k), :]

    old_means = np.random.random_integers(low=0, high=1, size=(k, n_col))
    new_means = np.random.random_integers(low=0, high=1, size=(k, n_col))

    while not ((curr_means - old_means) < 10e-3).all():
        # Assign each point to cluster with closest mean points.
        clusters = assign_points_to_clusters(curr_means, X)

        # Update cluster medoids to be lowest mean points.
        for cluster_id in range(k):
            cluster = np.where(cluster_id == clusters)[0]
            new_means[cluster_id, :] = np.mean(X[cluster, :], axis=0)

        old_means = curr_means
        curr_means = new_means


    return clusters, curr_means


def assign_points_to_clusters(points, X):
    k = len(points)
    all_distance = np.zeros(shape=(X.shape[0], k))
    for i in range(k):
        all_distance[:, i] = np.sqrt(np.sum(np.square(X - points[i]), axis=1))
    return np.argmin(all_distance, axis=1)

if __name__ == '__main__':
    X = np.random.random_integers(low=1, high=10, size=(10, 3))
    clusters, means = k_mean(X)
    print 'all data :'
    print X
    print 'assigment id for data :'
    print clusters
    print 'all mean points :'
    print means
