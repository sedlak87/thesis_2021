class Similarity:
    def __init__(self, recipe_id, recipe_name, ingredients, value):
        self._recipe_id = recipe_id
        self._recipe_name = recipe_name
        self._ingredients = ingredients
        self._value = value

    def get_recipe_name(self):
        return self._recipe_name

    def get_ingredients(self):
        return self._ingredients

    def get_value(self):
        return self._value

    def set_recipe_name(self, recipe_name):
        self._recipe_name = recipe_name

    def set_ingredients(self, ingredients):
        self._ingredients = ingredients
