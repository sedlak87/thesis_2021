import pickle
import sys
from pony.orm import *

from database.db_helper import RECIPE_INGREDIENTS_NF, RECIPE_INGREDIENTS, Ingredients_NF, Recipe_IngredientVector, \
    Ingredients_VectorI

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
        df = pickle.load(p_f) # Data frame

        if int(sys.argv[2]) == 1:
            all_recipe_ingr_ids = set(select(p.IngredientId for p in RECIPE_INGREDIENTS_NF))
            print("Creating ingredient table for vector index purposes")
            for recipe_ingr_id in all_recipe_ingr_ids:
                Ingredients_NF(IngredientValue=recipe_ingr_id)

        if int(sys.argv[3]) == 1:
            print("Creating table with recipe ID and ingredient vector string")
            recipe_ids = set(select(r.id for r in RECIPE_INGREDIENTS if r.valid == 1))
            total_ingredients = select(i.id for i in Ingredients_NF if i.Valid == 1).count()
            for r_id in recipe_ids:
                ingredient_vector = [0] * total_ingredients
                recipe_ingredient_values = list(select(ri.IngredientId for ri in RECIPE_INGREDIENTS_NF if ri.RecipeId == r_id))
                ingredients_vector_i = list(select(i for i in Ingredients_VectorI if i.IngredientValue in recipe_ingredient_values))
                for ingr in ingredients_vector_i:
                    ingredient_vector[ingr.Vector_I] = 1
                ingredient_vector_string = ','.join([str(i) for i in ingredient_vector])
                Recipe_IngredientVector(RecipeId=r_id, IngredientVector=ingredient_vector_string)

## DELETED CODE

        # if int(sys.argv[2]) == 1:  # remove rare ingredients
        #     print("Removing ingredients appearing in less than 3 recipes")
        #     # SELECT DISTINCT IngredientId, COUNT(RecipeId)
        #     # FROM RECIPE_INGREDIENTS_NF group  by  IngredientId
        #     ingredient_ids = set(select(i.IngredientId for i in RECIPE_INGREDIENTS_NF))
        #
        #     recipe_ingredient_data = list(select(e for e in RECIPE_INGREDIENTS_NF))
        #     for i in recipe_ingredient_data:
        #         list(select(e for e in RECIPE_INGREDIENTS_NF))
        #     #max_three_times = df.query(f"count <= {RARE_RECIPE_COUNT}")
        #     #rare_ingredient_ids = set(max_three_times['id'])
        #     invalidate_ingredients(recipe_ingredient_data)  # fixme
        #
        # if int(sys.argv[3]) == 1:  # remove very popular ingredients
        #     print("Removing very popular ingredients, appearing in more than 34000 recipes")
        #     popular = df.query(f"count > {POPULAR_RECIPE_COUNT}")
        #     popular_ingredient_ids = set(popular['id'])
        #     invalidate_ingredients(popular_ingredient_ids)