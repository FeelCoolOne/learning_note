# encoding=utf-8


class BernuliNaiveBayes(object):

    def __init__(self):
        pass

    def fit(self, X, y):
        from numpy import unique, ndarray
        from numpy import mean, sum, zeros
        if not isinstance(X, ndarray):
            raise TypeError('X must be numpy.array')
        self.n_samples_, self.n_features_ = X.shape
        self.classes_ = unique(y)
        self.n_class = self.classes_.size
        if not 2 == self.n_class:
            raise ValueError('y must be 2-class, but {0} given'.format(self.n_class))
        if not self.n_samples_ == len(y):
            raise ValueError('X can not match with y')
        self.class_map = {self.classes_[i]: i for i in range(self.n_class)}
        y_vec = zeros((self.n_samples_, self.n_class))
        for i in range(self.n_samples_):
            y_vec[i, self.class_map.get(y[i])] = 1
        print y_vec
        self.priors = sum(y, axis=0) / self.n_samples_
        self.prob = zeros((self.n_class, self.n_features_))
        for i in range(self.n_class):
            self.prob[i, :] = mean(X[y_vec[:, i] == 1, :], axis=0)

    def predict(self, X):
        from numpy import log, dot, argmax
        neg_prob = 1 - self.prob
        neg_log_prob = log(neg_prob)
        pos_log_prob = log(self.prob)
        log_likelihood_numerator = dot(X, pos_log_prob.T) + dot(X, neg_log_prob.T) + self.priors
        tmp = argmax(log_likelihood_numerator, axis=1)
        return self.classes_[tmp]


if __name__ == '__main__':
    from numpy import random, arange
    X = random.rand(50, 60)
    X[X > 0.5] = 0
    X[X <= 0.5] = 1
    y = arange(40)
    y[:30] = 0
    y[30:] = 1
    model = BernuliNaiveBayes()
    model.fit(X[:40], y)
    print model.predict(X[40:])
