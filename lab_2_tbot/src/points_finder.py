import pandas as pd
import math


class PointsFinder:
    def __init__(self, data_path):
        self._data = pd.read_csv(data_path, header=None)

    def __call__(self, latitude, longitude, n=3, *args, **kwargs):
        """ Returns n places nearby the given coordinates. """
        distances = self._data.apply(lambda row: self.distance(latitude, longitude, row[1], row[2]), axis=1)
        top3 = distances.nsmallest(3).index.values
        return self._data.iloc[top3].to_dict(orient='records')

    @staticmethod
    def distance(lat1, lon1, lat2, lon2):
        diam_Earth = 12742
        a = 0.5 - math.cos(math.radians(lat2 - lat1)) / 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (1 - math.cos(math.radians(lon2 - lon1))) / 2
        return diam_Earth * math.asin(math.sqrt(a))
