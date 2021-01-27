import sys
import os
import pandas as pd
from datetime import datetime, time
import time
from collections.abc import Iterable
import json

""" Create a class that keeps records of parameters and results for a series of experiments
Tha data from completed runs need to be safe, even in case of crashes.
"""
class Keep_records():
    def __init__(self):
        self.ts = datetime.now().strftime("%H%M")
        self.records = []
        self.record = {} # In case I want to expand to partial updates
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.cache_path = os.path.join(dir_path, "results", "cached_results" )
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

    def get_headers(self):
        print(self.headers)
        print()

    def cache_results(self):
        json_path = os.path.join(self.cache_path, "results_"+self.ts+".json")
        with open(json_path, "w") as wf:
            json.dump(self.records, wf)


    def keep(self, rec: dict):
        """
        Adds the provided dict into self.records
        Saves the result into cache
        """
        self.record = rec
        self.record["timestamp"] = datetime.now().strftime("%H%M%S")
        self.records.append(self.record)
        self.cache_results()
        return pd.DataFrame.from_dict(self.records)

    def get_df(self):
        print("results_"+self.ts+".json")
        return pd.DataFrame.from_dict(self.records)
    
    def from_json(self, filename):
        with open( os.path.join(self.cache_path, filename)) as rf:
            return pd.DataFrame(json.load(rf))


if __name__ == "__main__":
    print('running independently')
    keeper = Keep_records()
    keeper.keep({2:20, 3:33, 4:44})
    time.sleep(4)
    df = keeper.keep({1:11, 2:22, 3:30, 4:3})
    print(df, "\n")
    print(keeper.from_json("results_2304.json"))
