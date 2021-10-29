import pickle
import sys
from pony.orm import *

from utils import get_ingredient_ids

db = Database(provider='sqlite', filename='../archive/backup/recipes.db')

class RECIPE_INGREDIENTS(db.Entity):
    id = PrimaryKey(int)
    ingredient_ids = Required(str)

db.generate_mapping(create_tables=True)

if __name__ == '__main__':
    print('Opening file: ' + sys.argv[1])
    data = list(select(p.ingredient_ids for p in RECIPE_INGREDIENTS))

    with open(sys.argv[1], 'rb') as p_f:
        df = pickle.load(p_f)
        three_times = df.query('count <= 3')
        ids_less_than_three = list(three_times['id'])


    # with open(sys.argv[1], 'rb') as p_f:
    #     ingredient_ids = pickle.load(p_f).id.unique()
    #
    # with open(sys.argv[1], 'rb') as p_f:
    #     loaded = pickle.load(p_f)

    pass


