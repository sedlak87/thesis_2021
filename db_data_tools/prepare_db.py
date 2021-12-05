import pickle
import sys
from pony.orm import *

from database.data_access import RECIPE_INGREDIENTS_NF, RECIPE_INGREDIENTS, INGREDIENTS_NF, RECIPE_INGREDIENT_VECTOR

__author__ = "Matúš Sedlák"

from utility import get_ingredient_ids_from_string


# Input parameters
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
            all_recipe_ingr_ids = set(select(p.ingredient_id for p in RECIPE_INGREDIENTS_NF))
            print("Creating ingredient table for vector index purposes")
            for recipe_ingr_id in all_recipe_ingr_ids:
                INGREDIENTS_NF(ingredient_value=recipe_ingr_id)

        if int(sys.argv[3]) == 1:
            print("Creating table with recipe ID and ingredient vector string")
            recipe_ids = set(select(r.id for r in RECIPE_INGREDIENTS if r.valid == 1))
            total_ingredients = select(i.id for i in INGREDIENTS_NF if i.valid == 1).count()
            for r_id in recipe_ids:
                ingredient_vector = [0] * total_ingredients
                recipe_ingredient_values = list(select(ri.ingredient_id for ri in RECIPE_INGREDIENTS_NF if ri.recipe_id==r_id))
                ingredients_vector_i = list(select(i for i in INGREDIENTS_NF if i.ingredient_id in recipe_ingredient_values))
                for ingr in ingredients_vector_i:
                    ingredient_vector[ingr.id] = 1
                ingredient_vector_string = ','.join([str(i) for i in ingredient_vector])
                RECIPE_INGREDIENT_VECTOR(recipe_id=r_id, ingredient_vector=ingredient_vector_string)
