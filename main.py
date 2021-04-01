import pickle
import sqlite3 as sl
import csv
import sys
import pandas as pandas
import random
import numpy as np
import re
from scipy.spatial import distance
from sklearn.metrics import jaccard_score
from itertools import chain

INGR_COUNT = 8023

def standardize(vector):
    result = []
    for x in range(INGR_COUNT):
        result[x] = vector[x]
    return result


class Similarity:
    def __init__(self, recipe_id, value):
        self.recipe_id = recipe_id
        self.value = value


class Recipe:
  def __init__(self, id, ingr_vector):
      self.id = id
      self.ingr_vector = ingr_vector

  def get_vector(self):
    return self.ingr_vector


class User:
    def __init__(self):
        pass

    def get_vector(self):
        print("Hello my name is " + self.name)



def jaccard_similarity(v1, v2):
    return jaccard_score(v1, v2)


def hamming_distance(v1, v2):
    return distance.hamming(v1, v2)


def get5_by_method(user_vector, db_recipes, method):
    jaccard_list = []
    c = 0
    for db in db_recipes:
        obj = Similarity(db.id, method(db.ingr_vector, user_vector))
        jaccard_list.append(obj)
        print(c)
        c += 1
    jaccard_list.sort(key=lambda v: v.value, reverse=True)
    return jaccard_list


def cossine_distance(v1, v2):
    return distance.cosine(v1, v2)


def kulzinsky(vector_1, vector_2):
    print('test')


def dice_sim(vector_1, vector_2):
    print('test')


def manhattan_sim(vector_1, vector_2):
    print('test')


def russel_rao_sim(vector_1, vector_2):
    print('test')

def string_to_ingredient_ids(string):
    result = string.strip("[]")
    return list(map(int, result.split(',')))

def get_recipe_ingr_from_db(con, id):
    cur = con.cursor()
    ingredients_ids = cur.execute(f"SELECT ingredient_ids FROM PP_RECIPES WHERE id={id}").fetchone()
    return ingredients_ids


def select_all_recipe_ingr_ids(con):
    cur = con.cursor()
    #  fixme momentalne vyberam mensiu vzorku receptov kvoli debugu
    ingredients_ids = cur.execute(f"SELECT id, ingredient_ids FROM PP_RECIPES").fetchmany(5000)
    return ingredients_ids


def get_recipe_ids_from_db(con):
    cur = con.cursor()
    ids = cur.execute(f"SELECT id FROM PP_RECIPES").fetchall()
    return list(chain.from_iterable(ids))


def get_all_recipes(con):
    all_recipes = []
    recipe_ingrs_coll = select_all_recipe_ingr_ids(con)
    for rec in recipe_ingrs_coll:
        ingr_ids = string_to_ingredient_ids(rec[1])
        recipe_vector = [0] * INGR_COUNT
        for i in ingr_ids:
            try:
                recipe_vector[i] = 1
            except IndexError:
                print(f"{i}")
        all_recipes.append(Recipe(rec[0], recipe_vector))
    return all_recipes


def merge_to1_vector(input_vectors):
    result = [0] * INGR_COUNT
    c = 0
    for i in input_vectors:
        ing_array = string_to_ingredient_ids(input_vectors[c])
        for y in ing_array:
            result[y] = 1
        c += 1
    return result

if __name__ == '__main__':
    con = sl.connect('test.db')
    print('Opening file: ' + sys.argv[1])

    #df = pandas.read_csv(sys.argv[1])
    #df.to_sql('PP_RECIPES', con, if_exists='append', index=False)
    #con.close()

    with open(sys.argv[1], 'rb') as p_f:
        ingredient_ids = pickle.load(p_f).id.unique()

    recipe_ids = get_recipe_ids_from_db(con)
    user_recipes = random.sample(list(recipe_ids), 5)  # random recipes

    ingr_vectors = []
    for x in user_recipes:
        ingr_vectors.append(get_recipe_ingr_from_db(con, x))
    user_recipes_ingrs = [x[0] for x in ingr_vectors]
    user_vector = merge_to1_vector(user_recipes_ingrs)

    recipes_list = get_all_recipes(con)

    jaccard_top5 = get5_by_method(user_vector, recipes_list, jaccard_similarity)
    hamming_top5 = get5_by_method(user_vector, recipes_list, hamming_distance)
    cossine_top5 = get5_by_method(user_vector, recipes_list, cossine_distance)

    print('Jaccard top 5: ')
    print(f'  1){jaccard_top5[0].recipe_id}\n  2){jaccard_top5[1].recipe_id}\n  3){jaccard_top5[2].recipe_id}\n  4){jaccard_top5[3].recipe_id}\n  5){jaccard_top5[4].recipe_id}\n')
    print('Pearson top 5: ')
    print(f'  1){cossine_top5[0].recipe_id}\n  2){cossine_top5[1].recipe_id}\n  3){cossine_top5[2].recipe_id}\n  4){cossine_top5[3].recipe_id}\n  5){cossine_top5[4].recipe_id}\n')
    print('Hamming top 5: ')
    print(f'  1){hamming_top5[0].recipe_id}\n  2){hamming_top5[1].recipe_id}\n  3){hamming_top5[2].recipe_id}\n  4){hamming_top5[3].recipe_id}\n  5){hamming_top5[4].recipe_id}\n')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/