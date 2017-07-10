# encoding=utf-8
'''
simhash
'''
import numpy as np


def make_phrase(data, type_=64):
    # 64 bit phrase
    if isinstance(type_, int) and type > 0:
        num_bit = type_
    phrase = np.zeros(num_bit)
    bit_map = np.array([2**(i - 1) for i in range(num_bit, 0, -1)])
    for word, weight in data:
        t = (hash(word) & (1 << num_bit - 1))
        bit_phrase = [t & (1 << (num_bit - 1 - i)) for i in range(0, num_bit)]
        bit_phrase = map(lambda x: x if x == 1 else -x, bit_phrase)
        phrase += bit_phrase * weight
    phrase[phrase > 0] = 1
    phrase[phrase < 0] = 0
    phrase = phrase.astype(int)
    return np.sum(phrase * bit_map)


def hamming_distance(phrase1, phrase2):
    tmp = phrase1 ^ phrase2
    distance = 0
    while tmp > 0:
        distance += 1
        tmp &= (tmp - 1)
    return distance


if __name__ == '__main__':
    '''
    hamming distance of 3 in 64 bit be better
    '''
    data = [('hehe', 0.45), ('xiaoxi', 0.69)]
    phrase = make_phrase(data)
    print phrase
