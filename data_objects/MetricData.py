class MetricData:
    def __init__(self, name, data):
        self._name = name
        self._data = data

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_data(self):
        return self._data

    def set_data(self, value):
        self._data = value
