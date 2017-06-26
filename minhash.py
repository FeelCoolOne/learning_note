# encoding=utf=8
"""
minhash
"""
import math
import numpy as np


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

r = 3
b = 100
n_hash = r * b
n_voca = 50000

# hash function: (a * x + b) % c


def create_hash_funcs():
    t = n_voca + 1
    result = list()
    while len(result) != n_hash:
        if is_prime(t) is True:
            result.append(t)
        t += 1
    abc = np.zeros((3, n_hash))
    abc[:, [0, 1]] = np.random.randint(low=0, high=n_voca, size=(n_hash, 2))
    abc[:, 2] = t
    hash_funcs = lambda x: (abc[:, 0] * x + abc[:, 1]) % abc[:, 2]
    return hash_funcs


def numerize_doc(docs_text, sep):
    """
      Parameter:
          doc_text: dict {doc0_name: content_string, doc0_name: content_string, ...}
      Return:
          vacabulary: list_str
          doc: array of int for words instead of str,  nan is null
    """
    if not isinstance(docs_text, dict):
        raise ValueError('error value')
    if all(map(lambda doc: isinstance(doc, str), docs_text)) is False:
        raise ValueError('error value')
    data = map(lambda doc: doc.strip().split(sep), docs_text)
    vacab = reduce(lambda x, y: set(x) | set(y), data)
    map_ = dict()
    for i, word in enumerate(vacab):
        map_[word] = i
    vacab = map_.keys()
    max_len_doc = max(map(lambda doc: len(doc), data))
    docs = np.zeros(len(data), max_len_doc)
    for i, doc in enumerate(data):
        doc = map(lambda x: map_.get(x, np.NaN), doc)
        diff_len = max_len_doc - len(doc)
        if diff_len > 0:
            doc = doc.extend([np.NaN] * diff_len)
        docs[i, :] = doc
    return vacab, docs


def doc_2_phrase(docs):
    """

    """
    global n_hash
    n_doc, _ = docs.shape
    hashs = create_hash_funcs()
    phrase = np.ones(n_hash, n_doc) * np.inf
    for word_vec in docs.T:
        phrase = np.minimum(hashs(word_vec), phrase)
    return phrase


def sim(phrase):
    global b
    global r
    global vacab
    n_hash, n_doc = phrase.shape
    tmp = np.ones((b, n_doc))
    for i in range(b):
        for j in range(n_doc):
            # need check
            t = map(lambda i: vacab[i], phrase[(i * r): (i * r + 2), j])
            tmp[i, j] = hash(''.join(t))
    # remain check sim
