# Utility methods
from scipy.spatial import distance
from sklearn.metrics import jaccard_score


def get_ingredient_ids(ingredient_ids_string):
    stripped_brackets = ingredient_ids_string.strip('[]')
    return list(map(int, stripped_brackets.split(',')))

#def get_recipes(input)


def jaccard_similarity(v1, v2):
    return jaccard_score(v1, v2)


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
    return abs(distance.euclidean(vector_1, vector_2))

