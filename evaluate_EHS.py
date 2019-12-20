import numpy as np


def get_histogram_vector(array, bins=50, range=(0, 1)):
    '''
    Get the probability histogram vector of a numpy array.
    '''
    histogram_vec = np.histogram(array, bins=bins, range=range, density=True)
    prob_vec = histogram_vec / np.sum(histogram_vec)
    return prob_vec
