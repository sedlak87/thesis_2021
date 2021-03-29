import pickle
import sqlite3 as sl
import csv
import sys
import pandas as pandas
import random
import re
from itertools import chain

INGR_COUNT = 8022

def standardize(vector):
    result = []
    for x in range(INGR_COUNT):
        result[x] = vector[x]
    return result


class Recipe:
  def __init__(self, name, ingr_vector):
      self.name = name
      self.ingr_vector = ingr_vector

  def get_vector(self):
    return self.ingr_vector


class User:
    def __init__(self):
        pass

    def get_vector(self):
        print("Hello my name is " + self.name)



def user_vector(recipes):
    print('test')


def jaccard_index(vector_1, vector_2):
    print('test')

def jaccard_get5(user_recipes, db_recipes):
    pass

def hamming_distance(vector_1, vector_2):
    print('test')


def cossine_distance(vector_1, vector_2):
    print('test')


def pearson_cor(vector_1, vector_2):
    print('test')


def kulczynski(vector_1, vector_2):
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


def get_recipe_ids_from_db(con):
    cur = con.cursor()
    ids = cur.execute(f"SELECT id FROM PP_RECIPES").fetchall()
    return list(chain.from_iterable(ids))


def get_all_recipes(con):
    recipe_ids = get_recipe_ids_from_db(con)
    all_recipes = []
    c = 0
    for r_id in recipe_ids:
        ingrs = string_to_ingredient_ids(get_recipe_ingr_from_db(con, r_id)[0])
        all_recipes.append(Recipe(f'Recipe number: {r_id}', ingrs))
        c += 1
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
    user_recipe_choice = random.sample(list(recipe_ids), 5)  # random recipes
    ingr_vectors = []
    for x in user_recipe_choice:
        ingr_vectors.append(get_recipe_ingr_from_db(con, x))
    ingr_vectors = [x[0] for x in ingr_vectors]

    user_vector = merge_to1_vector(ingr_vectors)
    recipes_list = get_all_recipes(con)

    jaccard_top5 = jaccard_get5(user_vector, 0)
    pearson_top5 = []
    hamming_top5 = []

    print('Jaccard top 5: ')
    print(f'  1){jaccard_top5[0]}\n  2){jaccard_top5[1]}\n  3){jaccard_top5[2]}\n  4){jaccard_top5[3]}\n  5){jaccard_top5[4]}\n')
    print('Pearson top 5: ')
    print(f'  1){pearson_top5[0]}\n  2){pearson_top5[1]}\n  3){pearson_top5[2]}\n  4){pearson_top5[3]}\n  5){pearson_top5[4]}\n')
    print('Hamming top 5: ')
    print(f'  1){hamming_top5[0]}\n  2){hamming_top5[1]}\n  3){hamming_top5[2]}\n  4){hamming_top5[3]}\n  5){hamming_top5[4]}\n')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/