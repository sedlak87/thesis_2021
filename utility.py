import random
from typing import List

from pony.orm import db_session, select, Error

from data_objects.RankedRecipe import RankedRecipe
from data_objects.Recipe import Recipe
from data_objects.User import User
from database.data_access import RECIPE_INGREDIENTS, RAW_RECIPES, RECIPE_INGREDIENTS_NF, INGREDIENTS_VECTOR_I, \
    INGREDIENTS_NF, RECIPE_INGREDIENT_VECTOR, get_recipe_name, get_ingredients_by_recipe_id, \
    get_metric_data_by_recipe_id, get_metric_top_recipes

__author__ = "Matúš Sedlák"


@db_session
def get_user_mock() -> User:
    random_recipe_ids = random.sample(list(select(p.id for p in RECIPE_INGREDIENTS if p.valid == 1)), 10)
    recipes = list(select((p.id, p.name) for p in RAW_RECIPES if p.id in random_recipe_ids))
    ingredients = set(select(p.ingredient_id for p in RECIPE_INGREDIENTS_NF if p.id in random_recipe_ids ))
    indeces = list(select(p.vector_i for p in INGREDIENTS_VECTOR_I if p.ingredient_id in ingredients))
    zero_vector = [0] * select(i.id for i in INGREDIENTS_NF if i.valid == 1).count()

    for i in indeces:
        zero_vector[i] = 1
    return User(name='Matúš', recipes=recipes, user_ingr_vector=zero_vector)


# Return top 5 Recipes by metric provided on input calculated with user_vector
@db_session
def get_recipe_vectors_metric(user_vector, f, reverse=False) -> List[RankedRecipe]:
    top_x_metric_recipes = []
    try:
        recipes = list(select(r for r in RECIPE_INGREDIENT_VECTOR if r.valid == 1))
        for r in recipes:
            ingredient_vector_int = [int(s) for s in r.ingredient_vector.split(',')]
            recipe_obj = Recipe(
                r.recipe_id, get_recipe_name(r.recipe_id), get_ingredients_by_recipe_id(r.recipe_id))
            recipe_metric_value = RankedRecipe(None, recipe_obj, f(ingredient_vector_int, user_vector))
            top_x_metric_recipes.append(recipe_metric_value)
        top_x_metric_recipes.sort(key=lambda v: (v.get_value(), v.get_recipe().get_id()), reverse=reverse)
    except Error:
        print(Error)
    [v.set_rank(i+1) for i, v in enumerate(top_x_metric_recipes)]  # assign ranks
    return top_x_metric_recipes


def get_ingredient_ids_from_string(ingredient_ids_string):
    stripped_brackets = ingredient_ids_string.strip('[]')
    return set(map(int, stripped_brackets.split(',')))


def get_metric_ranking(metric_name, data):
    recipe_ids = [r['recipe_id'] for r in data]
    metric_data = get_metric_data_by_recipe_id(metric_name, recipe_ids)
    metric_ranking = []
    sorted_data = sorted(metric_data, key=lambda i: i.get_rank())
    for metric_recipe in sorted_data:
        metric_ranking.append(metric_recipe.get_recipe().get_id())
    return metric_ranking


def get_user_ranking(data):
    user_ranking = []
    for recipe in sorted(data, key=lambda i: int(i['rank'])):
        user_ranking.append(recipe['recipe_id'])
    return user_ranking


def get_top_metrics_data(data):
    result = []
    for m in data:
        result.append(get_metric_top_recipes(m.get_metric_name()))
    return result
