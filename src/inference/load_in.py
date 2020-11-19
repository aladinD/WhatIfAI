"""
This module handles the loading and management of data for model training
and model testing. Any and all functions that directly handle data for a learning
task MUST go through here.
"""

import os
from pathlib import Path
import pandas as pd

DATA_FILE = "res/{}/{}/{}.csv"
DATA_DIRECTORY = "res/{}/{}"


class LoadIn():
    """
    This class handles imports and persistent storage of datasets
    """
    def __init__(self):
        """
        Constructor. Initaliaze a loading manager.
        """
        self.datasets = {
            "app": "apple-mobility",
            "cov": "covid",
            "dec": "de-cix",
            "fin": "finance",
            "ggm": "google_mobility",
            "ggt": "google_trends",
            "iex": "ix",
            "pip": "pipeline",
            "pla": "playstation",
            "soc": "socialblade",
            "ste": "steam",
            "twi": "twitch"
        }
        self.dataframe = None
        self.dataframes = {}
        self.keys = {}
        self.path = Path(__file__).resolve().parent.parent.parent

    def load_sets(self, strs, typ="processed"):
        """ Get dataframes for each dataset, load them """
        dataframes = {}
        for dset in strs:
            for file in os.listdir(DATA_DIRECTORY.format(self.datasets[dset], typ)):
                if file.endswith(".csv") and not self.dataframes[file]:
                    path = os.path.join(self.path, 'res', file)
                    self.dataframes[file] = pd.read_csv(path)
                    dataframes[file] = self.dataframes[file]
                    self.keys[file] = dset
                if self.dataframes[file]:
                    dataframes[file] = self.dataframes[file]
        return dataframes

    def load_all(self, typ="pre"):
        """
        Load compiled data sets
        """
        if typ == "pre":
            path = os.path.join(self.path, "res", "pipeline", "scaled_pre_corona_df.csv")
        else:
            path = os.path.join(self.path, "res", "pipeline", "scaled_corona_df.csv")
        self.dataframe = pd.read_csv(path)
        return self.dataframe

    def get_all(self):
        """
        Return the compiled dataset
        """
        return self.dataframe

    def get_comp_sets(self):
        """
        Return all currently stored datasets
        """
        return self.dataframes

    def get_keys(self):
        """
        Get all the current subset keys
        """
        return self.keys

    def get_set_keys(self):
        """
        Get all the dataset keys
        """
        return self.datasets

    def clear_all(self):
        """
        Use this setter to clear the object for reuse
        """
        self.dataframes = {}
        self.keys = {}

    def clear_set(self, dset):
        """
        Setter removes a set from the object
        """
        del self.dataframes[dset]
        raise NotImplementedError
