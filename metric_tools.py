# Utility methods
import random

from pony.orm import db_session
from scipy.spatial import distance

__author__ = "Matúš Sedlák"


def jaccard_similarity(v1, v2):
    return distance.jaccard(v1, v2)


def hamming_distance(v1, v2):
    return distance.hamming(v1, v2)


def cossine_distance(v1, v2):
    return distance.cosine(v1, v2)


def corr(vector_1, vector_2):
    return distance.correlation(vector_1, vector_2)


def kulsinski_distance(vector_1, vector_2):
    return distance.kulsinski(vector_1, vector_2)


def manhattan_distance(vector_1, vector_2):
    return distance.cityblock(vector_1, vector_2)


def russel_rao_distance(vector_1, vector_2):
    return distance.russellrao(vector_1, vector_2)


def random_data(x, y):
    return random.uniform(0, 1)


metric_dic = {'Jaccard': jaccard_similarity,
              'Hamming': hamming_distance,
              'Cossine': cossine_distance,
              'Correl': corr,
              'Kulsinski': kulsinski_distance,
              'Manhattan': manhattan_distance,
              'Russel R': russel_rao_distance,
              'Random': random_data
              }
