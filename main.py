import pickle
import sys
from random import random

from pony.orm import *
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from typing import List
from wtforms import StringField, IntegerField, FieldList, SubmitField, FormField, DecimalField
from wtforms.validators import DataRequired
from dto.Similarity import Similarity
from dto.Recipe import Recipe

from database.db_helper import RAW_RECIPES
from prepare_db import fix_db


__author__ = "Matúš Sedlák"

from utils import get_user_vector_mock, jaccard_similarity

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
def get_top5_recipe_vectors_metric(user_vector, method, reverse=True) -> List[Similarity]:
    top_5_metric_recipes = []
    recipe_data = [Recipe(1, 'Burgir', None, [0]*6227)]
    try:
        for recipe in recipe_data:
            obj = Similarity(recipe.id, recipe.name, recipe.ingredients,
                             method(recipe.ingr_vector, user_vector))
            top_5_metric_recipes.append(obj)
        top_5_metric_recipes.sort(key=lambda v: v.value, reverse=reverse)
    except Error:
        print(Error)
    return top_5_metric_recipes[:20]


@app.route("/metrics")
def show_metrics():
    form = MetricListForm()
    user_vector = get_user_vector_mock()



    jacc = get_top5_recipe_vectors_metric(user_vector, jaccard_similarity)
    return render_template("metrics_recommendations.html", form=form)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)


