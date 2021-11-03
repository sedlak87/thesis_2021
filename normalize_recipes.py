import pickle
import sys
from pony.orm import *

from main import RECIPE_INGREDIENTS, RECIPE_INGREDIENTS_NF


db = Database(provider='sqlite', filename='../archive/backup/recipes.db')


def get_ingredient_ids_from_string(ingredient_ids_string):
    stripped_brackets = ingredient_ids_string.strip('[]')
    return set(map(int, stripped_brackets.split(',')))


@db_session
def fix_db():
    normalized_data_count = select(r for r in RECIPE_INGREDIENTS_NF).count()
    if normalized_data_count == 0:
        recipes_not_normalized = list(select(r for r in RECIPE_INGREDIENTS))
        for recipe in recipes_not_normalized:
            ingredient_ids_int_array = get_ingredient_ids_from_string(recipe.ingredient_ids)
            for ingredient in ingredient_ids_int_array:
                RECIPE_INGREDIENTS_NF(RecipeID=recipe.id, IngredientID=ingredient)
    with open(sys.argv[1], 'rb') as p_f:
        df = pickle.load(p_f)
        max_three_times = df.query('count <= 3')
        rare_ingredient_ids = list(max_three_times['id'])
        for r_id in rare_ingredient_ids:
            rare_entry_list = list(select(p for p in RECIPE_INGREDIENTS_NF if p.IngredientID == r_id))
            for e in rare_entry_list:
                e.set(Valid=0)
        return


if __name__ == '__main__':
    fix_db()
