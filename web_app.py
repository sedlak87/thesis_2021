import rbo
from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, SubmitField, FormField
from pony.orm import *
from database.data_access import create_metric_data, clean_metric_data, get_user_data, \
    restore_user, add_recipe_to_user, get_user_recipe, RAW_RECIPES, get_metric_data_by_recipe_id
from data_objects.MetricData import MetricData
from data_objects.MetricRankResult import MetricRankResult
from metric_tools import *
from utility import get_user_mock, get_user_ranking, get_recipe_vectors_metric, get_metric_ranking, get_top_metrics_data

__author__ = "Matúš Sedlák"


app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = "password"
app.static_folder = 'static'


class RankedRecipeForm(FlaskForm):
    rank = StringField('rank')
    recipe_id = IntegerField('id')
    recipe_name = StringField('name')
    ingredients = StringField('ingredients')


class RankedRecipeListForm(FlaskForm):
    ranked_recipes = FieldList(FormField(RankedRecipeForm))


class RecipeForm(FlaskForm):
    id = IntegerField('id')
    name = StringField('name')
    ingredients = StringField('ingredients')


class SearchRecipeForm(FlaskForm):
    search_text = StringField('search')
    search_submit = SubmitField('Search')
    recipes = FieldList(FormField(RecipeForm))
    user_recipes = StringField('User recipes')


@app.route("/")
def index():
    # fix_db()  # Prepare data, need to set web_app.py input parameters
    restore_user()
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def recipe_search():
    form = SearchRecipeForm()
    if request.method == 'POST':
        recipe_id = request.form.get('add_recipe')
        if recipe_id is not None:
            db_recipe = get_user_recipe(recipe_id)
            if db_recipe is None:
                flash('Recipe added successfully')
                add_recipe_to_user(recipe_id)
            else:
                flash('Recipe already in the database', 'error')
        with db_session:
            db_recipes = set(select(p for p in RAW_RECIPES)[:5])  # TODO: implement searching
            form_recipes = list()
            for db_r in db_recipes:
                recipe_item = dict()
                recipe_item["id"] = db_r.id
                recipe_item["name"] = db_r.name
                recipe_item["ingredients"] = db_r.ingredients
                form_recipes.append(recipe_item)
            form.recipes = form_recipes
            user_data = get_user_data()
            return render_template("input_user_data.html", form=form, user_data=user_data)
    else:
        user_data = get_user_data()
        return render_template("input_user_data.html", form=form, user_data=user_data)


@app.route("/metrics")
def show_metrics():
    form = RankedRecipeListForm()
    user = get_user_mock()
    data = []
    recipe_set = set()
    clean_metric_data()
    top_x = 5
    for name, f in metric_dic.items():
        # name = 'Jaccard'
        # f = function(a,b)
        recommendations = get_recipe_vectors_metric(user_vector=user.get_user_ingr_vector(), f=f)
        metric_dto = MetricData(name, recommendations)
        recommendations_top_x = recommendations[:top_x]
        create_metric_data(metric_dto.get_data(), name)
        data.append(MetricData(name, recommendations_top_x))
        recipe_set.update([o.get_recipe() for o in recommendations_top_x])  # potential recipes for the user

    for r in recipe_set:
        ranked_recipe_form = RankedRecipeForm()
        ranked_recipe_form.recipe_id = r.get_id()
        ranked_recipe_form.rank = ""
        ranked_recipe_form.recipe_name = r.get_name()
        ranked_recipe_form.ingredients = r.get_ingredients()
        form.ranked_recipes.append_entry(ranked_recipe_form)
    return render_template("recommendations_ranking.html", data=data, user_data=user, form=form)


@app.route("/result", methods=["POST", "GET"])
def compare_rankings():
    form = RankedRecipeListForm()
    user_ranking_data = form.ranked_recipes.data
    metric_to_user_value = []
    for name in metric_dic.keys():
        metric_ranking = get_metric_ranking(name, user_ranking_data)
        user_ranking = get_user_ranking(user_ranking_data)
        res = rbo.RankingSimilarity(metric_ranking, user_ranking).rbo()
        metric_to_user_value.append(MetricRankResult(metric_name=name, value=res))

    top_metrics_data = get_top_metrics_data(metric_to_user_value)
    return render_template("results.html", data=metric_to_user_value, top_metrics_data=top_metrics_data)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)


