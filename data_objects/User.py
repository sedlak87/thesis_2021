class User:
    def __init__(self, name, recipes, user_ingr_vector):
        self._name = name
        self._recipes = recipes
        self._user_ingr_vector = user_ingr_vector

    def get_recipes(self):
        return self._recipes

    def get_user_ingr_vector(self):
        return self._user_ingr_vector
