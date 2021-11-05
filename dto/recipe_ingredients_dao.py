class Recipe_Ingredients_Dao:
    def __init__(self, id, name, ingredients, ingr_vector=None):
        self.id = id
        self.name = name
        self.ingredients = ingredients
        self.ingr_vector = ingr_vector

    def get_vector(self):
        return self.ingr_vector
