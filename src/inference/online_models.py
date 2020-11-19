"""
Implementation of online models for our dataset
"""
import datetime as dt
from datetime import timedelta
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from keras.layers import concatenate
from keras.layers import Dense
from keras.layers import Input
from keras.models import Model
from keras.optimizers import Adam


class OnlineDense():
    """
    Class contains an online linear model and all of its pre and post
    training attributes.
    """
    def __init__(self, dataframe, output, dset, settings):
        """
        Constructor
        """
        self.dataframe = dataframe
        self.settings = self.init_settings(settings)
        self.predictions = []
        self.model = None
        self.dset = dset
        self.output = output
        self.metrics = ['mae']
        self.data_length = len(self.dataframe)
        self.last_day = dataframe["Date"][dataframe.index[-1]]

    def inc_dataframe(self, dataframe):
        """
        Fill in missing dataframe
        """

    def init_model(self):
        """
        Model setup
        """
        optimizer = Adam(learning_rate=0.03)
        neurons = self.settings["neurons"]
        layer_number = self.settings["layers"]
        input_a = Input(shape=(1,))
        input_b = Input(shape=(2,))
        inp_a = Dense(2, activation="linear")(input_a)
        inp_b = Dense(12, activation=self.settings["lay_activ"])(input_b)
        for layer in range(1, layer_number):
            inp_b = Dense(neurons[layer], activation=self.settings["lay_activ"])(inp_b)
        inp_b = Dense(1, activation=self.settings["out_activ"])(inp_b)
        inp_a = Model(inputs=input_a, outputs=inp_a)
        inp_b = Model(inputs=input_b, outputs=inp_b)
        combined = concatenate([inp_a.output, inp_b.output])
        out = Dense(2, activation="relu")(combined)
        out = Dense(1, activation="linear")(out)
        self.model = Model(inputs=[inp_a.input, inp_b.input], outputs=out)
        self.model.compile(loss=self.settings["loss"], optimizer=optimizer, metrics=self.metrics)
        self.model.summary()
        return self.model

    def set_metric(self, metrics):
        """
        Set the desired performance metric
        """
        self.metrics = metrics
        return self.metrics

    def fit_model(self):
        """
        Train the model
        """
        window = self.settings["window"]
        for itr in range(0, 300):
            print(f"This is iteration: {itr}, with max nat. points: {self.data_length}")
            inp_a, inp_b, out = self.data_transform(itr + 1, itr + window)
            self.model.fit([inp_a, inp_b], out, epochs=1, batch_size=8)
            if itr == 0:
                self.predictions = np.array(self.output[0:window+1]).tolist()
            if itr > 0:
                passed = itr + window
                month = self.get_pred_month(passed)
                day = self.get_pred_week(passed)
                inp = self.dataframe[["month", "day"]].copy().to_numpy()
                if itr >= window-1:
                    self.dataframe = self.dataframe.append([{"month": month, "day": day, "Date": "none"}])
                inp = inp[-1, :]
                prediction = self.model.predict([np.arange(passed, passed + 1, 1).reshape((1, 1)), inp.reshape((1, 2))])
                if passed >= self.data_length - 1:
                    self.output = self.output.append(pd.Series([prediction[0][0]]))
                self.predictions.append(prediction)

    def data_transform(self, start, end):
        """
        Pandas to Numpy python
        """
        inp_a = np.arange(start=start, stop=end+1, step=1)
        inpt_b = self.dataframe[["month", "day"]].copy().to_numpy()
        inp_b = inpt_b[start:end+1, :]
        out = np.array(self.output[start:end+1])
        return inp_a, inp_b, out

    def plot_model(self):
        """
        Plot predictions against labels
        """
        x_ax = np.arange(0, len(self.predictions), 1)
        y_ax = np.arange(0, len(self.output), 1)
        plt.xlabel("Days since 01.01.2020")
        plt.ylabel(self.dset)
        plt.plot(x_ax, self.predictions, label="Predictions")
        plt.plot(y_ax, self.output, label="Outputs")
        plt.show()

    def save_model(self):
        """
        Saves a model
        """

    def load_model(self, time):
        """
        Loads a pretrained model
        """

    def init_settings(self, settings):
        """
        Initialize settings
        """
        self.settings = {"in_dim": 2,
                         "layers": 2,
                         "lay_activ": "relu",
                         "out_activ": "linear",
                         "neurons": [4, 2],
                         "loss": "mean_absolute_error",
                         "window": 91,
                         "end": 1000}
        for setter in settings:
            self.settings[setter] = settings[setter]
        return self.settings

    def get_pred_month(self, days):
        """
        Get month of predicted day
        """
        date = dt.datetime.strptime(self.last_day, '%Y-%m-%d')
        new_day = date + timedelta(days=days)
        return new_day.month

    def get_pred_week(self, days):
        """
        Get weekday of predicted day
        """
        date = dt.datetime.strptime(self.last_day, '%Y-%m-%d')
        new_day = date + timedelta(days=days)
        return new_day.weekday()
