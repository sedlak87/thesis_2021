from pony.orm import *

from data_objects.MetricData import MetricData
from data_objects.Recipe import Recipe
from data_objects.RankedRecipe import RankedRecipe

db = Database(provider='sqlite', filename='../../archive/backup/recipes.db')

__author__ = "Matúš Sedlák"


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
    recipe_id = Required(int)
    ingredient_id = Required(int)


class INGREDIENTS_NF(db.Entity):
    id = PrimaryKey(int, auto=True)
    ingredient_id = Required(int)
    valid = Required(int, default=1)


class INGREDIENTS_VECTOR_I(db.Entity):
    vector_i = PrimaryKey(int, auto=True)
    ingredient_id = Required(int)
    valid = Required(int, default=1)


class RECIPE_INGREDIENT_VECTOR(db.Entity):
    recipe_id = PrimaryKey(int, auto=True)
    ingredient_vector = Required(str)
    valid = Required(int, default=1)


class USER_RECIPES(db.Entity):
    id = PrimaryKey(int, auto=True)
    user_id = Required(int)
    recipe_id = Required(int)


class METRIC_DATA(db.Entity):
    metric_name = Required(str)
    recipe_id = Required(int)
    PrimaryKey(metric_name, recipe_id)
    rank = Required(int)


db.generate_mapping(create_tables=True)


@db_session
def get_recipe_name(recipe_id):
    p = RAW_RECIPES[recipe_id]
    return p.name
    # database session cache will be cleared automatically
    # database connection will be returned to the pool


@db_session
def get_ingredients_by_recipe_id(recipe_id):
    recipe_ingredients_str = select(
        r.ingredients for r in RAW_RECIPES if r.id == recipe_id).first().strip("[]")
    result = [s for s in recipe_ingredients_str.split(',')]
    return result


@db_session
def clean_metric_data():
    delete(m for m in METRIC_DATA)


@db_session
def create_metric_data(data, name):
    for s in data:
        METRIC_DATA(metric_name=name, recipe_id=s.get_recipe().get_id(), rank=s.get_rank())


@db_session
def get_metric_data_by_recipe_id(metric_name, recipe_ids):
    ranked_recipes = list(select((s.recipe_id, s.rank)
                                 for s in METRIC_DATA if s.recipe_id in recipe_ids and s.metric_name == metric_name))
    recipes = []
    for rr in ranked_recipes:
        r = Recipe(id=rr[0])
        s = RankedRecipe(rank=rr[1], recipe=r)
        recipes.append(s)
    return recipes


@db_session
def get_metric_top_recipes(metric_name):
    metric_data = list(select((m.rank, r.id, r.name, r.ingredients)
                              for m in METRIC_DATA for r in RAW_RECIPES
                              if m.recipe_id == r.id and m.metric_name == metric_name))
    recipes = []
    sorted_by_rank = sorted(metric_data, key=lambda i: i[0])
    for rr in sorted_by_rank[:10]:
        r = Recipe(name=rr[2], id=rr[1], ingredients=rr[3])
        s = RankedRecipe(rank=rr[0], recipe=r)
        recipes.append(s)
    m = MetricData(name=metric_name, data=recipes)
    return m


@db_session
def get_user_data():
    user_recipe_ids = list(select(u.recipe_id for u in USER_RECIPES))
    return list(select((r.id, r.name) for r in RAW_RECIPES if r.id in user_recipe_ids))


@db_session
def get_user_recipe(recipe_id):
    return select(r.id for r in USER_RECIPES if r.recipe_id == recipe_id).first()


@db_session
def add_recipe_to_user(recipe_id):
    return USER_RECIPES(user_id=1, recipe_id=recipe_id)


@db_session
def restore_user():
    return delete(u for u in USER_RECIPES)
