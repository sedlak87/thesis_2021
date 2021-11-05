import json
import pickle

from numpy import genfromtxt, array
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from flask import Flask, render_template, request, redirect, url_for, jsonify
from dto.recipe_ingredients_dao import Recipe
from dto.Similarity import Similarity
from utils import *
from flask_paginate import Pagination, get_page_parameter
import os
import csv
from pony.orm import *
import numpy as np


db = Database(provider='sqlite', filename='../archive/backup/test.db')
app = Flask(__name__, static_url_path='')
app.static_folder = 'static'
INGR_COUNT = 8023
POPULAR_INGR = {6270, 840, 6906, 5006, 7655, 5319, 800, 6276, 590, 4987}


class RECIPE_INGREDIENTS(db.Entity):
    id = PrimaryKey(int)
    ingredient_ids = Required(str)

class PP_RECIPES(db.Entity):
    id = PrimaryKey(int, auto=True)
    ingredient_ids = Required(str)


class RAW_RECIPES(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    ingredients = Required(str)


@db_session
def get_user_vector(choose_recipe_ids):
    data = list(select(p.ingredient_ids for p in PP_RECIPES if p.id in choose_recipe_ids))
    zero_vector = [0] * INGR_COUNT
    for a in data:
        recipe = get_ingredient_ids(a)
        for ingredient_id in recipe:
            zero_vector[ingredient_id] = 1
    return zero_vector


db.generate_mapping(create_tables=True)


def create_recipe_vectors_file(input_recipes):
    d = {}
    for r in input_recipes:
        r_int = get_ingredient_ids(r[1])
        zero_vector = [0] * INGR_COUNT
        for ingr_id in r_int:
            if ingr_id not in POPULAR_INGR:
                zero_vector[ingr_id] = 1
        if len(r_int) > 9:
            d[r[0]] = zero_vector
    try:
        file = "/test/Names.json"
        with open(os.getcwd() + file, 'w', ) as f:
            json.dump(d, f)
    except IOError:
        print("I/O error")


def get5_by_method(user_vector, db_recipes, method, reverse=False):
    top5list = []
    try:
        for db in db_recipes:
            obj = Similarity(db.id, db.name, db.ingredients, method(db.ingr_vector, user_vector))
            top5list.append(obj)
        top5list.sort(key=lambda v: v.value, reverse=reverse)
    except Error:
        print(Error)
    return top5list[:15]


def read_recipe_file(file, user_vector, rec_list):
    all = []
    with open(file) as json_file:
        recipe_data = json.load(json_file)
        for k, v in recipe_data.items():
            recipe_name = list(select(p.name for p in RAW_RECIPES if p.id == int(k)))
            recipe_obj = Recipe(k, recipe_name, None, v)
            all.append(recipe_obj)
    jacc = get5_by_method(user_vector, all, jaccard_similarity)
    hamm = get5_by_method(user_vector, all, hamming_distance)
    coss = get5_by_method(user_vector, all, cossine_distance)
    kuzl = get5_by_method(user_vector, all, kulzinsky_distance)
    dice = get5_by_method(user_vector, all, dice_distance)
    roger = get5_by_method(user_vector, all, rogers_tan_distance)
    russr = get5_by_method(user_vector, all, russel_rao_distance)
    eucl = get5_by_method(user_vector, all, euclidean_distance)
    sm = get5_by_method(user_vector, all, sm_distance)
    correl = get5_by_method(user_vector, all, corr)
    bray_c = get5_by_method(user_vector, all, bray_c_distance)
    yule = get5_by_method(user_vector, all, yule_distance)
    manhattan = get5_by_method(user_vector, all, manhattan_distance)
    sokal_d = get5_by_method(user_vector, all, sokal)

    list_of_top5s = [jacc, hamm, coss, kuzl, dice, roger, russr, eucl, sm, correl,
                     bray_c, yule, manhattan, sokal_d]
    sims = []
    sims.extend(['Jaccard', 'Hamming', 'Cossine', 'Kulzinsky', 'Dice', 'Rogers', 'Russ R', 'Euclid.',
                 'Sokel M.', 'Correlation', 'Bray C.', 'Yule', 'Manhattan', 'Sokal'])
    return render_template("user_recipes.html", rec_list=rec_list, sims=sims, list_of_top5s=list_of_top5s)


@app.route("/test")
def index():
    with db_session:
        all_recipes = set(select(p.id for p in PP_RECIPES))
        pick_ids = random.sample(all_recipes, k=10)
        u_v = get_user_vector(pick_ids)
        recipes = set(select((p.id, p.ingredient_ids) for p in PP_RECIPES)[:1000])
        create_recipe_vectors_file(recipes)
        user_p = []
        for xxx in pick_ids:
            x = Recipe(None, list(select(p.name for p in RAW_RECIPES if p.id == xxx))[0], None)
            user_p.append(x)
        return read_recipe_file(os.getcwd() + "/test/Names.json", u_v, user_p)


# @app.route('/')
# @db_session
# def test():
#     search = False
#     q = request.args.get('q')
#     if q:
#         search = True
#     page = request.args.get(get_page_parameter(), type=int, default=1)
#     total = len(select(p.id for p in RAW_RECIPES))
#     recipes = list(select(p for p in RAW_RECIPES).page(page))
#     pagination = Pagination( page=page, total=total, search=search, record_name='recipes')
#     return render_template('recipes.html', recipes=recipes, pagination=pagination)

# if __name__ == '__main__':
#     # app.run(host="127.0.0.1", port=8080, debug=True)
#     with db_session:
#         data = list(select(p.id for p in RECIPE_INGREDIENTS))
#         print(data)


# if __name__ == '__main__':
#     db.generate_mapping(create_tables=True)
#     with db_session:
#         data = RAW_RECIPES.select(lambda p: p.id < 500)
#         for i in data:
#             print("[ID] = " + str(i.id) + "| [name] = " + i.name)


# if __name__ == '__main__':
#     x = [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0
#          , 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0]
#     y = [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1
#          , 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]
#
#     a = [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1,
#          1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1]
#     b = [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0,
#          0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0]
#
#     print ("Jaccard Viac: " + str(jaccard_similarity(x, y)))
#     print ("Jaccard Menej: " + str(jaccard_similarity(a, b)))
#
#     print("hamming Viac: " + str(hamming_distance(x, y)))
#     print("hamming Menej: " + str(hamming_distance(a, b)))
#
#     print("cossine Viac: " + str(cossine_distance(x, y)))
#     print("cossine Menej: " + str(cossine_distance(a, b)))
#
#     print("kulzinsky Viac: " + str(kulzinsky_distance(x, y)))
#     print("kulzinsky Menej: " + str(kulzinsky_distance(a, b)))
#
#     print("dice Viac: " + str(dice_distance(x, y)))
#     print("dice Menej: " + str(dice_distance(a, b)))
#
#     print("R&T Viac: " + str(rogers_tan_distance(x, y)))
#     print("R&T Menej: " + str(rogers_tan_distance(a, b)))
#
#     print("R&R Viac: " + str(russel_rao_distance(x, y)))
#     print("R&R Menej: " + str(russel_rao_distance(a, b)))
#
#     print("sm_distance Viac: " + str(sm_distance(x, y)))
#     print("sm_distance Menej: " + str(sm_distance(a, b)))
#
#     print("corr Viac: " + str(corr(x, y)))
#     print("corr Menej: " + str(corr(a, b)))
#
#     print("bray_c_distance Viac: " + str(bray_c_distance(x, y)))
#     print("bray_c_distance Menej: " + str(bray_c_distance(a, b)))
#
#     print("yule_distance Viac: " + str(yule_distance(x, y)))
#     print("yule_distance Menej: " + str(yule_distance(a, b)))
#
#     print("kulsinski_distance Viac: " + str(kulsinski_distance(x, y)))
#     print("kulsinski_distance Menej: " + str(kulsinski_distance(a, b)))
#
#     print("manhattan_distance Viac: " + str(manhattan_distance(x, y)))
#     print("manhattan_distance Menej: " + str(manhattan_distance(a, b)))
#
#     print("sokal Viac: " + str(sokal(x, y)))
#     print("sokal Menej: " + str(sokal(a, b)))

# if __name__ == '__main__':
#    engine = create_engine('sqlite:///archive/csv_test.db')
#   Base.metadata.create_all(engine)
#
# Create the session
#    session = sessionmaker()
#    session.configure(bind=engine)
#    s = session()
