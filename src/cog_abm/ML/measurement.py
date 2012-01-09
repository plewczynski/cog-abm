import time

from statistics import correct

def timeit(fun, *args, **kwargs):
    start = time.time()
    ret = fun(*args, **kwargs)
    elapsed = time.time() - start
    return (ret, elapsed)
    

def analyse_classifier(classifier, d_train, d_test):
    train_t = timeit(classifier.train, d_train)[1]
    corr, test_t = timeit(correct, classifier, d_test)
    return corr, train_t, test_t
    