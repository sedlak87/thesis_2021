class Recipe:
    def __init__(self, id, name=None, ingredients=None, ingr_vector=None):
        self._id = id
        self._name = name
        self._ingredients = ingredients
        self._ingr_vector = ingr_vector

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_ingredients(self):
        return self._ingredients

    def get_vector(self):
        return self.ingr_vector

    def __key(self):
        return self._id, self._name

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Recipe):
            return self.__key() == other.__key()
        return NotImplemented
