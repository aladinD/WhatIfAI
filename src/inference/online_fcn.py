"""
Implementation of an online fcn model for our dataset
"""
import datetime as dt
import pickle
import numpy as np
from matplotlib import pyplot as plt
from creme import linear_model
from creme import metrics
from creme import preprocessing
from creme import stream
from creme import ensemble


class OnlineFCN():
    """
    Class contains an online linear model and all of its pre and post
    training attributes.
    """
    def __init__(self, dataframe, output, dset):
        """
        Constructor
        """
        self.dataframe = dataframe
        self.settings = {}
        self.history = []
        self.trained_model = None
        self.init_model = None
        self.metric = self.set_metric()
        self.dset = dset
        self.output = output

    def setup_model(self):
        """
        Model setup
        """
        model = preprocessing.StandardScaler()
        model |= ensemble.BaggingRegressor(
            model=linear_model.LinearRegression(intercept_lr=0.1),
            n_models=30,
            seed=42
        )
        self.init_model = model
        self.trained_model = model
        return self.init_model

    def set_metric(self):
        """
        Set the desired performance metric
        """
        self.metric = metrics.MAE()
        return self.metric

    def do_fitting(self):
        """
        Train the model
        """
        for inp, lbl in stream.iter_pandas(self.dataframe, self.output):
            prediction = self.trained_model.predict_one(inp)
            metric = self.metric.update(lbl, prediction)
            self.trained_model = self.trained_model.fit_one(inp, lbl)
            self.history.append(prediction)
        print(metric)
        return self.trained_model

    def plot(self):
        """
        Plot predictions against labels
        """
        x_ax = np.arange(0, len(self.history), 1)
        plt.xlabel("Days since 01.01.2020")
        plt.ylabel(self.dset)
        plt.plot(x_ax, self.history, label="Predictions")
        plt.plot(x_ax, self.output, label="Outputs")
        plt.show()

    def save_model(self):
        """
        Saves a model
        """
        with open("onln_fcn_"+self.dset+"_"+str(dt.time)+".pkl", 'wb') as f:
            pickle.dump(self.trained_model, f)
            return self.trained_model

    def load_model(self, time):
        """
        Loads a pretrained model
        """
        with open("onln_fcn_"+str(self.dset)+"_"+str(time)+".pkl", 'rb') as f:
            model = pickle.load(f)
            return model
