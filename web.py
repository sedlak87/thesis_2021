import pickle
import sqlite3 as sl
import csv
import sys
import pandas as pandas
import random
import numpy as np
import re
from flask import Flask, render_template
from scipy.spatial import distance
from sklearn.metrics import jaccard_score
from itertools import chain

from dto.recipe_ingredients_dao import Recipe
from dto.Similarity import Similarity
from utils import get_ingredient_ids

app = Flask(__name__, static_url_path='')
app.static_folder = 'static'
INGR_COUNT = 8023

class Similarity_method:
    def __init__(self, name):
        self.name = name


def get_recipe_ids_from_db(con):
    cur = con.cursor()
    ids = cur.execute(f"SELECT id FROM PP_RECIPES").fetchall()
    return list(chain.from_iterable(ids))


def get_recipe_by_id(con, id):
    cur = con.cursor()
    recipe = cur.execute(f"SELECT name, ingredients FROM RAW_RECIPES WHERE id={id}").fetchall()
    return recipe


def get_recipe_ingr_from_db(con, id):
    cur = con.cursor()
    ingredients_ids = cur.execute(f"SELECT ingredient_ids FROM PP_RECIPES WHERE id={id}").fetchone()
    return ingredients_ids


def merge_to1_vector(input_vectors):
    result = [0] * INGR_COUNT
    c = 0
    for i in input_vectors:
        ing_array = get_ingredient_ids(input_vectors[c])
        for y in ing_array:
            result[y] = 1
        c += 1
    return result


def select_all_recipe_ingr_ids(con):
    cur = con.cursor()
    #  fixme momentalne vyberam mensiu vzorku receptov kvoli debugu
    statement = f"SELECT rr.name, rr.id, rr.ingredients, pr.ingredient_ids from RAW_RECIPES rr " \
                f"JOIN PP_RECIPES pr ON rr.id = pr.id"
    ingredients_ids = cur.execute(statement).fetchmany(500)
    return ingredients_ids


def get_all_recipes(con):
    all_recipes = []
    recipe_ingrs_coll = select_all_recipe_ingr_ids(con)
    for rec in recipe_ingrs_coll:
        ingr_ids = get_ingredient_ids(rec[3])
        recipe_vector = [0] * INGR_COUNT
        for i in ingr_ids:
            try:
                recipe_vector[i] = 1
            except IndexError:
                print(f"{i}")
        all_recipes.append(Recipe(rec[1], rec[0], rec[2], recipe_vector))
    return all_recipes


def jaccard_similarity(v1, v2):
    return 1 - distance.jaccard(v1, v2)


def hamming_distance(v1, v2):
    return distance.hamming(v1, v2)


def cossine_distance(v1, v2):
    return 1 - distance.cosine(v1, v2)


def get5_by_method(user_vector, db_recipes, method, reverse=True):
    list = []
    for db in db_recipes:
        obj = Similarity(db.id, db.name, db.ingredients, method(db.ingr_vector, user_vector))
        list.append(obj)
    list.sort(key=lambda v: v.value, reverse=reverse)
    return list[:5]


@app.route("/")
def index():
    con = sl.connect('test.db')
    print('Opening file: ' + sys.argv[1])
    with open(sys.argv[1], 'rb') as p_f:
        ingredient_ids = pickle.load(p_f).id.unique()
    recipe_ids = get_recipe_ids_from_db(con)
    user_recipes = random.sample(list(recipe_ids), 5)  # random recipes
    rec_list = []
    for ur in user_recipes:
        recipe = get_recipe_by_id(con, ur)  # name, ingredients
        rec_list.append(Recipe(ur, recipe[0][0], recipe[0][1]))

    ingr_vectors = []
    for x in user_recipes:
        ingr_vectors.append(get_recipe_ingr_from_db(con, x))
    user_recipes_ingrs = [x[0] for x in ingr_vectors]
    user_vector = merge_to1_vector(user_recipes_ingrs)

    recipes_list = get_all_recipes(con)

    jaccard_top5 = get5_by_method(user_vector, recipes_list, jaccard_similarity, True)
    hamming_top5 = get5_by_method(user_vector, recipes_list, hamming_distance, False)
    cossine_top5 = get5_by_method(user_vector, recipes_list, cossine_distance, True)

    list_of_top5s = [jaccard_top5, hamming_top5, cossine_top5]
    sims = []
    sims.extend(['Jaccard', 'Hamming', 'Cossine'])
    return render_template("user_recipes.html", rec_list=rec_list, sims=sims, list_of_top5s=list_of_top5s)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
