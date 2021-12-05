from data_objects.Recipe import Recipe


class RankedRecipe:
    def __init__(self, rank, recipe: Recipe, value=0):
        self._rank = rank
        self._recipe = recipe
        self._value = value

    def get_recipe(self):
        return self._recipe

    def get_value(self):
        return self._value

    def set_recipe(self, recipe):
        self._recipe = recipe

    def get_rank(self):
        return self._rank

    def set_rank(self, rank):
        self._rank = rank

    def __key(self):
        return self._recipe, self._value

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, RankedRecipe):
            return self.__key() == other.__key()
        return NotImplemented
