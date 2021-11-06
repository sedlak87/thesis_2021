from pony.orm import *


db = Database(provider='sqlite', filename='../../archive/backup/recipes.db')



class RAW_RECIPES(db.Entity):
   id = PrimaryKey(int, auto=True)
   name = Required(str)
   ingredients = Required(str)
   n_ingredients = Required(int)


class RECIPE_INGREDIENTS(db.Entity):
   id = PrimaryKey(int)
   ingredient_ids = Required(str)
   valid = Required(int, default=1)


class RECIPE_INGREDIENTS_NF(db.Entity):
   id = PrimaryKey(int, auto=True)
   RecipeId = Required(int)
   IngredientId = Required(int)


class Ingredients_NF(db.Entity):
   id = PrimaryKey(int, auto=True)
   IngredientValue = Required(int)
   Valid = Required(int, default=1)


class Ingredients_VectorI(db.Entity):
   Vector_I = PrimaryKey(int, auto=True)
   IngredientValue = Required(int)


class Recipe_IngredientVector(db.Entity):
   RecipeId = PrimaryKey(int, auto=True)
   IngredientVector = Required(str)
   valid = Required(int, default=1)


db.generate_mapping(create_tables=True)
