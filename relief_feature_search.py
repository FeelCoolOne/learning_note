# encoding=utf=8
from numpy.random import randint
from numpy import shape, zeros, ma, logical_not, float32, array
import numpy as np


def calculate_distance(data, kind):
    '''calculate distance between samples from data'''

    from numpy.linalg import norm
    if kind not in ['cosine', 'euclidean']:
        raise ValueError("'kind' should be one of ['cosine', 'euclidean']"
                         "got kind: {0}".format(kind))
    if kind == 'cosine':
        norms = norm(data, axis=1)
        XX = data.dot(data.T)
        XX_norm = norms.reshape(norms.size, 1) * norms
        distances = XX / XX_norm
        return distances
    elif kind == 'euclidean':
        pass


def relief(data, y, threshold):
    '''
        feature selection using relief algorithm

        Parameter
        ---------
            data: numpy.array
            y: list_like of 1 dimension for sample label
            threshold: float, (0, 1)

        Return
        ------
            valid_feature: bool of list
        caution: only for binary classification and discreat
    '''

    if isinstance(y, list):
        y = array(y)
    distances = calculate_distance(data, kind='cosine')
    n_sample, n_feature = shape(data)
    weight = zeros(n_feature, dtype=float32)
    diff_nominal = lambda x, y: 0 if x == y else 1
    tmp = np.max(data, axis=0) - np.min(data, axis=0)
    tmp = np.where(tmp == 0, 1, tmp)
    diff_numerical = lambda x, y, id: abs(x - y)/tmp[id]
    n_iter = int(n_sample * 0.8)
    for i in range(n_iter):
        index = randint(n_sample)
        sample = data[index]
        same_label_mask = y != y[index]
        non_same_label_mask = logical_not(same_label_mask)
        same_label_mask[index] = True
        same_label_data = ma.array(distances[index],
                                   mask=same_label_mask)
        non_same_label_data = ma.array(distances[index],
                                       mask=non_same_label_mask)
        hit_id = ma.argmax(same_label_data)
        miss_id = ma.argmax(non_same_label_data)
        # print index, hit_id, miss_id
        for id_attr, (sample_attr,
                      miss_attr,
                      hit_attr) in enumerate(zip(sample,
                                                 data[miss_id],
                                                 data[hit_id])):
            if isinstance(sample_attr, (str, bool)):
                delta_w = diff_nominal(sample_attr,
                                       miss_attr) - diff_nominal(sample_attr,
                                                                 hit_attr)
            else:
                delta_w = diff_numerical(sample_attr,
                                         miss_attr,
                                         id_attr) - diff_numerical(sample_attr,
                                                                   hit_attr, id_attr)

            weight[id_attr] += delta_w
    weight /= n_iter

    # filter the feature of lower weight than threshold
    valid_feature = weight >= threshold
    return valid_feature


def reliefF(data, y, threshold):
    '''
        feature selection using reliefF algorithm

        Parameter
        ---------
            data: numpy.array
            y: list_like of 1 dimension for sample label
            threshold: float, (0, 1)

        Return
        ------
            valid_feature: bool of list
    '''
    if isinstance(y, list):
        y = array(y)
    distances = calculate_distance(data, kind='cosine')
    n_sample, n_feature = shape(data)
    weight = zeros(n_feature, dtype=float32)
    n_iter = int(n_sample * 0.8)
    pass


if __name__ == '__main__':
    # from numpy.random import randint
    from numpy import array
    # y = randint(2, size=20)
    # data = randint(5, size=[20, 40])
    data = array([[1, 2, 3, 0, 5, 3],
                  [1, 2, 2, 0, 5, 3],
                  [1, 3, 2, 4, 5, 6],
                  [1, 3, 2, 4, 5, 6],
                  [1, 3, 2, 4, 5, 6]])
    y = [0, 0, 1, 1, 1]
    mask = relief(data, y, 0.01)
    print mask
