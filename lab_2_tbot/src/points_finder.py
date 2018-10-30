import math
import sys

import pandas as pd

sys.path.append("..")
import locationiq_utils
import time


class PointsFinder:
    OFFLINE_RADIUS = 700

    def __init__(self, data_path):
        self.data_path = data_path
        self._data = pd.read_csv(self.data_path, header=None, sep="\t")

    def __call__(self, latitude, longitude, n=3, *args, **kwargs):
        """ Returns n places nearby the given coordinates. """
        distances = self._data.apply(lambda row: self.distance(latitude, longitude, row[1], row[2]), axis=1)
        minimum = distances.nsmallest(3).min()
        if minimum < self.OFFLINE_RADIUS:
            top3 = distances.nsmallest(3).index.values
            result = pd.concat([self._data.iloc[top3], distances.nsmallest(3)], axis=1, ignore_index=True)
            result_json = result.to_dict(orient="records")
            return result_json
        else:
            records = []
            records += locationiq_utils.get_nearbys(latitude, longitude, radius=self.OFFLINE_RADIUS, tag='pharmacy')
            time.sleep(0.6)
            records += locationiq_utils.get_nearbys(latitude, longitude, radius=self.OFFLINE_RADIUS, tag='supermarket')
            for record in records:
                if type(record) == dict:
                    if "name" in record.keys():
                        json_address = locationiq_utils.get_address(record["lat"], record["lon"])
                        time.sleep(0.8)
                        if json_address:
                            new_record = "\t".join([record["name"],
                                                    record["lat"],
                                                    record["lon"],
                                                    locationiq_utils.format_address(json_address)]) + "\n"
                            with open(self.data_path, 'a') as f:
                                f.write(new_record)

            self._data = pd.read_csv(self.data_path, header=None, sep="\t")

            distances = self._data.apply(lambda row: self.distance(latitude, longitude, row[1], row[2]), axis=1)
            distances.drop_duplicates(keep=False, inplace=True)
            smallest_distances = distances.nsmallest(n)
            top3 = smallest_distances.index.values
            result = pd.concat([self._data.iloc[top3], smallest_distances], axis=1, ignore_index=True)
            return result.to_dict(orient="records")

    @staticmethod
    def distance(lat1, lon1, lat2, lon2):
        diam_Earth = 12742
        a = 0.5 - math.cos(math.radians(lat2 - lat1)) / 2 + math.cos(math.radians(lat1)) * math.cos(
            math.radians(lat2)) * (1 - math.cos(math.radians(lon2 - lon1))) / 2
        return int(1000 * (diam_Earth * math.asin(math.sqrt(a))))
