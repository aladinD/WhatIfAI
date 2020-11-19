"""provides the interface for data_management"""
import os
from abc import ABCMeta, abstractmethod
import joblib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class PreprocessDataInterface(metaclass=ABCMeta):
    """Edit doxy !!!"""
    NUMBER_ALGOS = 3
    PCA = 1
    STANDART_SCALING = 2
    MIN_MAX_SCALING = 3

    def __init__(self, name, scaling_algo=2):
        """
        Consructor of abstract class
        @param name : name of the dataset. Has to be identical to the folder name!!
        @param scaling_algo : select one of the scaling algo`s 1, 2, 3. Default is 2
        """
        self.scaling_algo = None
        path_to_res = os.path.join('.', 'res')
        self.path_to_processed = os.path.join(path_to_res, str(name), 'processed')      # path to processed folder
        self.path_processed_data = None                                                 # path to csv
        self.set_scalinging_algorithm(scaling_algo)
        self._path_to_scaler = os.path.join(self.path_to_processed, 'scaler.save')
        self.frame = self._load_data(name)

    def _load_data(self, name):  # pylint: disable=inconsistent-return-statements
        """
        Sets the paths to the raw and processed folders.
        Input should be a string similar to the naming in the res folder e.g 'pornhub'
        """
        # check if name object is string
        if isinstance(name, str):
            # we can be sure that every .csv has a different name so we iterate over the files in folder
            count = 0
            dirs = os.listdir(self.path_to_processed)
            for file in dirs:
                if file.endswith('.csv'):
                    count += 1
                    self.path_processed_data = os.path.join(self.path_to_processed, file)
                    frame = pd.read_csv(self.path_processed_data)

            if count == 1:
                return frame
            # raise Exception('There are too many .csv files in folder {}'.format(self.path_to_processed))
        else:
            raise Exception('ICollector : get_paths name is no valid string')

    def set_scalinging_algorithm(self, algo=2):
        """
        these functions only serve the purpose of providing an example
        NUMBER_ALGOS = 3
        PCA = 1
        STANDART_SCALING = 2
        MIN_MAX_SCALING = 3
        """
        if isinstance(algo, int) and 0 < algo <= self.NUMBER_ALGOS:
            self.scaling_algo = algo
        else:
            raise Exception('Enter a valid algorithem')

    def process(self, components=2):
        """feel free to replace them with something that actually makes sense"""
        if os.path.exists(self._path_to_scaler):
            os.remove(self._path_to_scaler)

        if self.scaling_algo == self.PCA:
            processed_data = self._pca(self.frame, components)
        elif self.scaling_algo == self.STANDART_SCALING:
            processed_data = self._standart_scaling(self.frame)
        elif self.scaling_algo == self.MIN_MAX_SCALING:
            processed_data = self._min_max_scaling(self.frame)
        else:
            raise Exception('Selected algorithem is not defined')

        # handle preprocessed data FIXME
        # self.__handle_processed_data(processed_data)
        return processed_data

    def inverse_preprocess(self, data, cols_to_scale=None):
        """
        Method for calculate the original values of processed data
        """
        return_data = pd.DataFrame()

        if os.path.exists(self._path_to_scaler):
            scaler = joblib.load(self._path_to_scaler)
        else:
            raise Exception('Can not inverse Process data. There is no scaler!!')
        if cols_to_scale is None:
            return_data[data.columns] = scaler.inverse_transform(data[data.columns])
        else:
            return_data[cols_to_scale] = scaler.inverse_transform(data[cols_to_scale])

        return return_data

    def plot_singular_values(self, data, colums_to_drop=None):
        """
        This function plots the singular values of a given dataset.
        Needed for pca to have insihgts in the data.
        """
        # first copy the frame and drop the date
        raw_data = data.copy()

        if colums_to_drop is not None:
            raw_data = raw_data.drop(columns=colums_to_drop, axis=1)

        # calculate svd
        _, sing, _ = np.linalg.svd(raw_data, full_matrices=True)

        # var_explained = np.round(sing**2/np.sum(sing**2), decimals=3)
        var_explained = sing**2/np.sum(sing**2)
        sns.barplot(x=list(range(1, len(var_explained)+1)),
                    y=var_explained, color="limegreen")
        plt.xlabel('Singular values', fontsize=16)
        plt.ylabel('Singular values of Corona dataset (normalized)', fontsize=10)
        path = os.path.join(self.path_to_processed, 'singular_val.png')
        plt.savefig(path, dpi=400)

    def __handle_processed_data(self, processed_data):
        """
        method stores the processed pandas frame as csv file.
        SET THE PATH with set_save_path(path) before executing preprocess!!
        """
        if self.path_processed_data is None:
            raise Exception('Set saving path before executing preprocess')
        processed_data.to_csv(self.path_processed_data)

    @abstractmethod
    def _pca(self, data, componenets):
        """Abstract method. Implement PCA"""
        raise NotImplementedError

    @abstractmethod
    def _standart_scaling(self, data):
        """Abstract method. Implement standart scaling"""
        raise NotImplementedError

    @abstractmethod
    def _min_max_scaling(self, data):
        """Abstract method. Implement z scaling"""
        raise NotImplementedError
