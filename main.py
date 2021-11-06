import pickle
import sys
from random import random

import rbo
from pony.orm import *
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from typing import List
from wtforms import StringField, IntegerField, FieldList, SubmitField, FormField, DecimalField
from wtforms.validators import DataRequired
from dto.Similarity import Similarity
from dto.Recipe import Recipe

from database.db_helper import RAW_RECIPES, Recipe_IngredientVector, RECIPE_INGREDIENTS_NF
from prepare_db import fix_db


__author__ = "Matúš Sedlák"

from utils import *

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = "password"
app.static_folder = 'static'


class RecipeForm(FlaskForm):
    id = IntegerField('id')
    name = StringField('name')
    ingredients = StringField('ingredients')


class SearchRecipeForm(FlaskForm):
    search_text = StringField('search')
    search_submit = SubmitField('Search')
    recipes = FieldList(FormField(RecipeForm))
    user_recipes = StringField('User recipes')


class MetricRecipeForm(FlaskForm):
    id = IntegerField('id')
    name = StringField('name')
    ingredients = StringField('ingredients')
    decimal_value = DecimalField('decimal')


class MetricForm(FlaskForm):
    user_rating = IntegerField('Rating')
    name = StringField('name')
    recipes = FieldList(FormField(MetricRecipeForm))


class MetricListForm(FlaskForm):
    metrics = FieldList(FormField(MetricForm))


@app.route("/")
def index():
    fix_db()  # Prepare data
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def recipe_search():
    form = SearchRecipeForm()
    if request.method == 'POST':
        with db_session:
            db_recipes = set(select(p for p in RAW_RECIPES)[:5])
            form_recipes = list()
            for db_r in db_recipes:
                recipe_item = dict()
                recipe_item["id"] = db_r.id
                recipe_item["name"] = db_r.name
                recipe_item["ingredients"] = db_r.ingredients
                form_recipes.append(recipe_item)
            form.recipes = form_recipes
            return render_template("input_user_data.html", form=form)
    else:
        return render_template("input_user_data.html", form=form)


# Return top 5 Recipes by metric provided on input calculated with user_vector
@db_session
def get_top_x_recipe_vectors_metric(x, user_vector, f, reverse=False) -> List[Similarity]:
    top_x_metric_recipes = []
    try:
        recipes = list(select(r for r in Recipe_IngredientVector if r.valid == 1))
        for recipe in recipes:
            ingredient_vector_int = [int(s) for s in recipe.IngredientVector.split(',')]
            recipe_name = select(r.name for r in RAW_RECIPES if r.id == recipe.RecipeId).first()
            recipe_metric_value = Similarity(recipe.RecipeId, recipe_name, None, f(ingredient_vector_int, user_vector))
            top_x_metric_recipes.append(recipe_metric_value)
        top_x_metric_recipes.sort(key=lambda v: (v.get_value(), v.get_recipe_id()), reverse=reverse)
    except Error:
        print(Error)
    return top_x_metric_recipes[:x]




@app.route("/metrics")
def show_metrics():
    form = MetricListForm()
    user_vector = get_user_vector_mock()
    metrics = ['Jaccard', 'Hamming', 'Cossine', 'Kulzinsky', 'Dice', 'Rogers', 'Russ R', 'Euclid.']
    data = []
    for name, f in metric_dic.items():
        # name = 'Jaccard'
        # f = function(a,b)
        metric_results = get_top_x_recipe_vectors_metric(
            x=10, user_vector=user_vector, f=f)
        data.append({'name': name, 'data': metric_results})

    return render_template("metrics_recommendations.html", data=data)


@app.route("/result")
def compare_rankings():
    S = [1, 2, 2]
    T = [1, 3, 2]

    res = rbo.RankingSimilarity(S,T).rbo()
    print(res)

    return "<h1> TEST </h1>"


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)


