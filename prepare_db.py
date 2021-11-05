import pickle
import sys
from pony.orm import *

from database.db_helper import RECIPE_INGREDIENTS_NF, RECIPE_INGREDIENTS, Ingredients_NF, Recipe_IngredientVector_NF


POPULAR_RECIPE_COUNT = 34000
RARE_RECIPE_COUNT = 3


def get_ingredient_ids_from_string(ingredient_ids_string):
    stripped_brackets = ingredient_ids_string.strip('[]')
    return set(map(int, stripped_brackets.split(',')))


def invalidate_ingredients(ingredient_ids):
    for r_id in ingredient_ids:
        rare_entry_list = list(select(p for p in RECIPE_INGREDIENTS_NF if p.IngredientId == r_id))
        for e in rare_entry_list:
            e.set(Valid=0)


# Input parameters
# file [1] data frame ingredients
# boolean [2] - remove ingredients that appear less than 3 times
# boolean [3] - remove very popular ingredients that appear in more than 34000 recipes
# boolean [4] - create ingredient table for vector purposes
# boolean [5] - create 0/1 recipe vector table
@db_session
def fix_db():
    normalized_data_count = select(r for r in RECIPE_INGREDIENTS_NF).count()
    if normalized_data_count == 0:
        print("Creating normalized table of recipe ingredients")
        recipes_not_normalized = list(select(r for r in RECIPE_INGREDIENTS))
        for recipe in recipes_not_normalized:
            ingredient_ids_int_array = get_ingredient_ids_from_string(recipe.ingredient_ids)
            for ingredient in ingredient_ids_int_array:
                RECIPE_INGREDIENTS_NF(RecipeId=recipe.id, IngredientId=ingredient)

    with open(sys.argv[1], 'rb') as p_f:
        df = pickle.load(p_f)
        if int(sys.argv[2]) == 1:  # remove rare ingredients
            print("Removing ingredients appearing in less than 3 recipes")
            max_three_times = df.query(f"count <= {RARE_RECIPE_COUNT}")
            rare_ingredient_ids = set(max_three_times['id'])
            invalidate_ingredients(rare_ingredient_ids)

        if int(sys.argv[3]) == 1:  # remove very popular ingredients
            print("Removing very popular ingredients, appearing in more than 34000 recipes")
            popular = df.query(f"count > {POPULAR_RECIPE_COUNT}")
            popular_ingredient_ids = set(popular['id'])
            invalidate_ingredients(popular_ingredient_ids)

        if int(sys.argv[4]) == 1:
            all_recipe_ingr_ids = list(select(p.IngredientID for p in RECIPE_INGREDIENTS_NF if p.Valid == 1))
            print("Creating ingredient table for vector index purposes")
            for recipe_ingr_id in all_recipe_ingr_ids:
                Ingredients_NF(IngredientValue=recipe_ingr_id)

        if int(sys.argv[5]) == 1:
            print("Creating table with recipe ID and ingredient vector")
            recipes = set(select(r.RecipeId for r in RECIPE_INGREDIENTS_NF if r.Valid == 1))
            totalIngredients = select(r.id for r in Ingredients_NF).count()
            ingredient_vector = [0]*totalIngredients
            for r in recipes:
                recipe_ingredient_values = list(select(ri.IngredientId for ri in RECIPE_INGREDIENTS_NF if ri.RecipeId == r))
                recipe_ingredient_ids = list(select(i for i in Ingredients_NF if i.IngredientValue in recipe_ingredient_values))
                for ingr_id in recipe_ingredient_ids:
                    ingredient_vector[ingr_id] = 1
                Recipe_IngredientVector_NF(RecipeId=r, IngredientVector=ingredient_vector)