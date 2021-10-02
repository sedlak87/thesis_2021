import json
import pickle
import sys

from numpy import genfromtxt, array
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from flask import Flask, render_template
from dto.Recipe import Recipe
from dto.Similarity import Similarity
from utils import *
import os
import csv
from pony.orm import *
import numpy as np

db = Database(provider='sqlite', filename='../archive/backup/test.db')
app = Flask(__name__, static_url_path='')
app.static_folder = 'static'
INGR_COUNT = 8023
POPULAR_INGR = {6270, 840, 6906, 5006, 7655, 5319, 800, 6276, 590, 4987}


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
        if len(r_int) > 8:
            d[r[0]] = zero_vector
    try:
        file = "/test/Names.json"
        with open(os.getcwd() + file, 'w', ) as f:
            json.dump(d, f)
    except IOError:
        print("I/O error")


def get5_by_method(user_vector, db_recipes, method, reverse=True):
    top5list = []
    try:
        for db in db_recipes:
            obj = Similarity(db.id, db.name, db.ingredients, method(db.ingr_vector, user_vector))
            top5list.append(obj)
        top5list.sort(key=lambda v: v.value, reverse=reverse)
    except Error:
        print(Error)
    return top5list[:20]


def read_recipe_file(file, user_vector, rec_list):
    all = []
    with open(file) as json_file:
        recipe_data = json.load(json_file)
        for k, v in recipe_data.items():
            recipe_name = list(select(p.name for p in RAW_RECIPES if p.id == int(k)))
            recipe_obj = Recipe(k, recipe_name, None, v)
            all.append(recipe_obj)
    jacc = get5_by_method(user_vector, all, jaccard_similarity)
    hamm = get5_by_method(user_vector, all, hamming_distance, False)
    coss = get5_by_method(user_vector, all, cossine_distance, False)
    kuzl = get5_by_method(user_vector, all, kulzinsky_distance, False)
    dice = get5_by_method(user_vector, all, dice_distance, False)
    roger = get5_by_method(user_vector, all, rogers_tan_distance, False)
    russr = get5_by_method(user_vector, all, russel_rao_distance, False)
    eucl = get5_by_method(user_vector, all, euclidean_distance, False)
    list_of_top5s = [jacc, hamm, coss, kuzl, dice, roger, russr, eucl]
    sims = []
    sims.extend(['Jaccard', 'Hamming', 'Cossine', 'Kulzinsky', 'Dice', 'Rogers', 'Russ R', 'Euclid.'])
    return render_template("user_recipes.html", rec_list=rec_list, sims=sims, list_of_top5s=list_of_top5s)


@app.route("/")
def index():
    with db_session:
        all_recipes = set(select(p.id for p in PP_RECIPES))
        pick_ids = random.sample(all_recipes, k=5)
        u_v = get_user_vector(pick_ids)
        recipes = set(select((p.id, p.ingredient_ids) for p in PP_RECIPES)[:12000])
        with open(sys.argv[1], 'rb') as p_f:
            loaded = pickle.load(p_f)
        create_recipe_vectors_file(recipes)
        user_p = []
        for xxx in pick_ids:
            x = Recipe(None, list(select(p.name for p in RAW_RECIPES if p.id == xxx))[0], None)
            user_p.append(x)
        return read_recipe_file(os.getcwd() + "/test/Names.json", u_v, user_p)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
