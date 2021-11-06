# Utility methods
import random

from pony.orm import db_session, select
from scipy.spatial import distance

from database.db_helper import Ingredients_VectorI


@db_session
def get_user_vector_mock():
    random_ingredients = random.sample(list(select(p.Vector_I for p in Ingredients_VectorI)), 40)
    zero_vector = [0] * select(r.Vector_I for r in Ingredients_VectorI).count()
    for a in random_ingredients:
        zero_vector[a] = 1
    return zero_vector


def jaccard_similarity(v1, v2):
    return distance.jaccard(v1, v2)


def hamming_distance(v1, v2):
    return distance.hamming(v1, v2)


def cossine_distance(v1, v2):
    return distance.cosine(v1, v2)


def kulsinski_distance(vector_1, vector_2):
    return distance.kulsinski(vector_1, vector_2)


def dice_distance(vector_1, vector_2):
    return distance.dice(vector_1, vector_2)


def rogers_tan_distance(vector_1, vector_2):
    return distance.rogerstanimoto(vector_1, vector_2)


def russel_rao_distance(vector_1, vector_2):
    return distance.russellrao(vector_1, vector_2)


def euclidean_distance(vector_1, vector_2):
    return distance.euclidean(vector_1, vector_2)


def sm_distance(vector_1, vector_2):
    return distance.sokalmichener(vector_1, vector_2)


def corr(vector_1, vector_2):
    return distance.correlation(vector_1, vector_2)


def bray_c_distance(vector_1, vector_2):
    return distance.braycurtis(vector_1, vector_2)


def yule_distance(vector_1, vector_2):
    return distance.yule(vector_1, vector_2)


def manhattan_distance(vector_1, vector_2):
    return distance.cityblock(vector_1, vector_2)


def sokal(vector_1, vector_2):
    return distance.sokalsneath(vector_1, vector_2)


metric_dic = {'Jaccard': jaccard_similarity,
              'Hamming': hamming_distance,
              'Cossine': cossine_distance,
              'Kulsinski': kulsinski_distance,
              'Dice': dice_distance,
              'Rogers T': rogers_tan_distance,
              'Russel R': russel_rao_distance,
              'Euclidean': euclidean_distance,
              'SM': sm_distance,
              'Correl': corr,
              'Bray c': bray_c_distance,
              'Yule': yule_distance,
              'Manhattan': manhattan_distance,
              'Sokal': sokal}
