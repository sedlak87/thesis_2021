class MetricRankResult:
    def __init__(self, metric_name, value):
        self._metric_name = metric_name
        self._value = value

    def get_metric_name(self):
        return self._metric_name

    def set_metric_name(self, metric_name):
        self._metric_name = metric_name

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value
