# Utility methods
from scipy.spatial import distance


def get_user_vector_mock():
    random_ingredients = [1, 2, 3, 4, 5, 6, 7, 8]  # ziskam X oblubenych ingrediencii
    zero_vector = [0] * 6227
    # for a in random_ingredients:
    #     #recipe = get_ingredient_ids(a)
    #     for ingredient_id in []:
    #         zero_vector[ingredient_id] = 1
    return zero_vector


def jaccard_similarity(v1, v2):
    return distance.jaccard(v1, v2)


def hamming_distance(v1, v2):
    return distance.hamming(v1, v2)


def cossine_distance(v1, v2):
    return distance.cosine(v1, v2)


def kulzinsky_distance(vector_1, vector_2):
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
