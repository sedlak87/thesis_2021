from numpy import genfromtxt, array
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import *
from pony.orm import *


db = Database(provider='sqlite', filename='../archive/backup/test.db')
INGR_COUNT = 8023


class PP_RECIPES(db.Entity):
    id = PrimaryKey(int, auto=True)
    ingredient_ids = Required(str)


class RAW_RECIPES(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    ingredients = Required(str)


if __name__ == '__main__':
    db.generate_mapping(create_tables=True)
    with db_session:
        data = RAW_RECIPES.select(lambda p: p.id < 500)
        for i in data:
            print("[ID] = " + str(i.id) + "| [name] = " + i.name)


# if __name__ == '__main__':
#     x = [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1]
#     y = [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1]
#     x_b = array(x, dtype=bool)
#     y_b = array(y, dtype=bool)
#
#     a = [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1]
#     b = [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
#     a_b = array(a, dtype=bool)
#     b_b = array(b, dtype=bool)
#
#     print ("Jaccard Viac podobne: " + str(jaccard_similarity(x, y)))
#     print ("Jaccard Menej podobne: " + str(jaccard_similarity(a, b)))
#
#     print("hamming Viac podobne: " + str(1 - hamming_distance(x, y)))
#     print("hamming Menej podobne: " + str(1 - hamming_distance(a, b)))
#
#     print("cossine Viac podobne: " + str(1 - cossine_distance(x, y)))
#     print("cossine Menej podobne: " + str(1 - cossine_distance(a, b)))
#
#     print("kulzinsky Viac podobne: " + str(1 - kulzinsky_distance(x, y)))
#     print("kulzinsky Menej podobne: " + str(1 - kulzinsky_distance(a, b)))
#
#     print("dice Viac podobne: " + str(1 - dice_distance(x, y)))
#     print("dice Menej podobne: " + str(1 - dice_distance(a, b)))
#
#     print("R&T Viac podobne: " + str(1 - rogers_tan_distance(x, y)))
#     print("R&T Menej podobne: " + str(1 - rogers_tan_distance(a, b)))
#
#     print("R&R Viac podobne: " + str(1 - russel_rao_distance(x, y)))
#     print("R&R Menej podobne: " + str(1 - russel_rao_distance(a, b)))
#
#     print("BC Viac podobne: " + str(euclidean_distance(x, y)))
#     print("BC Menej podobne: " + str(euclidean_distance(a, b)))


#if __name__ == '__main__':
#    engine = create_engine('sqlite:///archive/csv_test.db')
#   Base.metadata.create_all(engine)
#
   # Create the session
#    session = sessionmaker()
#    session.configure(bind=engine)
#    s = session()


