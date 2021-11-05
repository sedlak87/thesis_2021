from pony.orm import *


db = Database(provider='sqlite', filename='../../archive/backup/recipes.db')


class RECIPE_INGREDIENTS_NF(db.Entity):
   id = PrimaryKey(int, auto=True)
   RecipeId = Required(int)
   IngredientId = Required(int)
   Valid = Required(int, default=1)


class RECIPE_INGREDIENTS(db.Entity):
   id = PrimaryKey(int)
   ingredient_ids = Required(str)


class Ingredients_NF(db.Entity):
   id = PrimaryKey(int, auto=True)
   IngredientValue = Required(int)


class Recipe_IngredientVector_NF(db.Entity):
   RecipeId = PrimaryKey(int, auto=True)
   IngredientVector = Required(str)


class RAW_RECIPES(db.Entity):
   id = PrimaryKey(int, auto=True)
   name = Required(str)
   ingredients = Required(str)


db.generate_mapping(create_tables=True)
