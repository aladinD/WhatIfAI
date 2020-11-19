"""
@author: Aron Endres
@date: 18.08.20
@brief: Facebooks Prophet prediction embedded in an scikit
"""

import os
from pathlib import Path
import pickle
import datetime as dt
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.model_selection import GridSearchCV

from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics

from src.inference.load_in import LoadIn


class MyProphet(BaseEstimator, RegressorMixin):
    """
    @brief: Prophet class for handling forecasts.
    @param BaseEstimator: get necessary function to be abele to use Scikit GridSearchCV
    @param RegressorMixin: get score function
    """

    def __init__(self):
        """
        @brief: Input data must be a dataframe containing a Date and a target value.
        """
        self.cols = ['ds', 'y']
        self.dset = None
        self.period = 183  # Predict 6 months in advance.
        self.metric = 'mse'
        self.growth = 'linear'
        self.changepoint_prior_scale = 0.05  # Sensitivity to data variance.
        self.interval_width = 0.8  # Necessary accumulated confidence for the returned interval.
        self.seasonality_mode = 'additive'
        self.model = Prophet(growth=self.growth, changepoint_prior_scale=self.changepoint_prior_scale,
                             interval_width=self.interval_width, seasonality_mode=self.seasonality_mode)
        self.cap = 1.5
        self.floor = -1.5
        self.param = {'stock_med': {'growth': 'logistic', 'changepoint_prior_scale': 0.05, 'interval_width': 0.8,
                                    'seasonality_mode': 'multiplicative', 'cap': 1.5, 'floor': -1.5},
                      'stock_bank': {'growth': 'logistic', 'changepoint_prior_scale': 0.065, 'interval_width': 0.8,
                                     'seasonality_mode': 'multiplicative', 'cap': 1.5, 'floor': -1.5},
                      'stock_energy': {'growth': 'linear', 'changepoint_prior_scale': 0.055, 'interval_width': 0.8,
                                       'seasonality_mode': 'additive', 'cap': 1.5, 'floor': -1.5},
                      'stock_oil': {'growth': 'logistic', 'changepoint_prior_scale': 0.185, 'interval_width': 0.8,
                                    'seasonality_mode': 'additive', 'cap': 1.5, 'floor': -1.5},
                      'stock_steel': {'growth': 'logistic', 'changepoint_prior_scale': 0.05, 'interval_width': 0.8,
                                      'seasonality_mode': 'multiplicative', 'cap': 1.5, 'floor': -1.5},
                      'stock_automotive': {'growth': 'linear', 'changepoint_prior_scale': 0.085, 'interval_width': 0.8,
                                           'seasonality_mode': 'multiplicative', 'cap': 1.5, 'floor': -1.5},
                      'stock_telecom': {'growth': 'logistic', 'changepoint_prior_scale': 0.055, 'interval_width': 0.8,
                                        'seasonality_mode': 'multiplicative', 'cap': 1.5, 'floor': -1.5},
                      'stock_tech': {'growth': 'linear', 'changepoint_prior_scale': 0.03, 'interval_width': 0.8,
                                     'seasonality_mode': 'additive', 'cap': 1.5, 'floor': -1.5},
                      'ix_bitrate': {'growth': 'logistic', 'changepoint_prior_scale': 0.195, 'interval_width': 0.8,
                                     'seasonality_mode': 'additive', 'cap': 1, 'floor': -1},
                      'youtube_viewchange': {'growth': 'logistic', 'changepoint_prior_scale': 0.105,
                                             'interval_width': 0.8, 'seasonality_mode': 'multiplicative',
                                             'cap': 1.5, 'floor': -1.5},
                      'youtube_views': {'growth': 'linear', 'changepoint_prior_scale': 0.04, 'interval_width': 0.8,
                                        'seasonality_mode': 'multiplicative', 'cap': 1.5, 'floor': -1.5},
                      'steam_users': {'growth': 'linear', 'changepoint_prior_scale': 0.135, 'interval_width': 0.8,
                                      'seasonality_mode': 'additive', 'cap': 1.5, 'floor': -1.5},
                      'steam_ingame': {'growth': 'linear', 'changepoint_prior_scale': 0.105, 'interval_width': 0.8,
                                       'seasonality_mode': 'multiplicative', 'cap': 1.5, 'floor': -1.5},
                      'twitch_views': {'growth': 'linear', 'changepoint_prior_scale': 0.09, 'interval_width': 0.8,
                                       'seasonality_mode': 'multiplicative', 'cap': 1.5, 'floor': -1.5},
                      'twitch_channels': {'growth': 'logistic', 'changepoint_prior_scale': 0.115, 'interval_width': 0.8,
                                          'seasonality_mode': 'additive', 'cap': 1.5, 'floor': -1.5},
                      'twitch_viewtime': {'growth': 'logistic', 'changepoint_prior_scale': 0.13, 'interval_width': 0.8,
                                          'seasonality_mode': 'additive', 'cap': 1.5, 'floor': -1.5},
                      'twitch_streams': {'growth': 'linear', 'changepoint_prior_scale': 0.05, 'interval_width': 0.8,
                                         'seasonality_mode': 'multiplicative', 'cap': 1.5, 'floor': -1.5},
                      'ps_users': {'growth': 'linear', 'changepoint_prior_scale': 0.16, 'interval_width': 0.8,
                                   'seasonality_mode': 'multiplicative', 'cap': 1.5, 'floor': -1.5}}

    def set_dset(self, dset):
        """
        @brief: Sets dset
        @param dset: new dset
        """
        self.dset = dset

    def set_cap(self, cap=1):
        """
        @brief: sets the cap for max in logistic growth
        @param cap: max logistic growth
        """
        self.cap = cap

    def set_floor(self, floor=1):
        """
        @brief: sets the floor for min in logistic growth
        @param floor min logistic growth
        """
        self.floor = floor

    def set_metric(self, metric='mse'):
        """
        @brief: sets the score unit
        @param metric: decide which metric for evaluation should be set avaiable is mse, rmse, mae, mape
        """
        self.metric = metric

    def set_model(self, after_best=False, growth='linear',  # pylint: disable=too-many-arguments
                  changepoint_prior_scale=0.05, interval_width=0.8,\
                  seasonality_mode='additive'):
        """
        @brief: Adapt the model
        @param growth: is the model linear or logistic in rising/falling
        @param changepoint_prior_scale: how flexibel ist the model greater more felxibel
        @param interval_width: the width of the uncertantiy
        @param seasonality_mode: additive or multiplicative if datapoint distirbution over time
        @param after_best: only used after gridsearchcv get model with best parameters
        """
        if after_best:
            self.model = Prophet(growth=self.growth, changepoint_prior_scale=self.changepoint_prior_scale,
                                 interval_width=self.interval_width, seasonality_mode=self.seasonality_mode)
        else:
            self.model = Prophet(growth=growth, changepoint_prior_scale=changepoint_prior_scale,
                                 interval_width=interval_width, seasonality_mode=seasonality_mode)

    def set_period(self, period):
        """
        @brief: set timespan to predict
        @param period: timespan of prediction
        """
        self.period = period

    def fit(self, x_date, y_data):
        """
        @brief: Data must be a pd frame in the form Date | y
        @param x_date: data for training
        @param y_data The time series values to fit the prophet to.
        """
        data = pd.concat([x_date, y_data], axis=1)
        data.columns = self.cols
        # for logistic growth
        data['cap'] = self.cap
        data['floor'] = self.floor
        return self.model.fit(data)

    def predict(self, label, do_plot=False):
        """
        @brief: Predict the next values
        @param do_plot: Do a plot of the forcast and the seasonalities
        """
        # get the current timeline plus a future timeline specified in period
        future = self.model.make_future_dataframe(periods=self.period)
        future['cap'] = self.cap
        future['floor'] = self.floor

        forecast = self.model.predict(future)

        if do_plot:
            self.plot(forecast, label)
        #   fig = plot_plotly(model, forecast)  # This returns a plotly Figure
        #   py.iplot(fig)

        return forecast.drop(['ds'], axis=1)

    def plot(self, forecast, label):
        """
        @brief: Plot and save the predictions
        """
        fig1 = self.model.plot(forecast)
        fig2 = self.model.plot_components(forecast)
        fig1.savefig(f'prophet plots/prophet_{label}.png')
        fig2.savefig(f'prophet plots/prophet_components{label}.png')

    def cross_validation(self):
        """
        @brief: Cross evaluates the data frames
        """
        horizon = str(self.period) + ' days'
        dataframe_cv = cross_validation(self.model, initial='400 days', period='100 days', horizon=horizon)

        return dataframe_cv

    def score_cross(self, dataframe_cv):
        """
        @brief: Evaluates the Model by cross validation
        @param dataframe_cv: data frame from cross validation
        """
        dataframe_metric = performance_metrics(dataframe_cv, rolling_window=0.1)
        # print(dataframe_metric.head())
        return np.float(dataframe_metric[self.metric][-1:])

    def gridsearchcv(self, parameters, dataframe, safe=False):
        """
        @brief: Custom grid search via cross validation. Necessary because of Prophets unique prediction interface.
        @brief: Looking for the best parameters to fit the model.
        @param parameters: parameters that give the option where to look is a dict
        @param dataframe The data frame to predict for cross validation.
        @param safe Option to save the resulting data frame.
        """
        # init dataframe to locate maximum
        data = {'growth': [], 'changepoint_prior_scale': [], 'interval_width': [], 'seasonality_mode': [], 'metric': []}
        df_metric = pd.DataFrame(data=data)
        # iterate through all possibilities
        for growth in parameters['growth']:
            for changepoint_prior_scale in parameters['changepoint_prior_scale']:
                for interval_width in parameters['interval_width']:
                    for seasonality_mode in parameters['seasonality_mode']:
                        self.set_model(growth=growth, changepoint_prior_scale=changepoint_prior_scale,
                                       interval_width=interval_width, seasonality_mode=seasonality_mode)
                        self.fit(x_date=dataframe['Date'], y_data=dataframe.iloc[:, 1])
                        dataframe_cv = self.cross_validation()
                        metric = self.score_cross(dataframe_cv)
                        new_row = {'growth': growth, 'changepoint_prior_scale': changepoint_prior_scale,
                                   'interval_width': interval_width, 'seasonality_mode': seasonality_mode,
                                   'metric': metric}
                        df_metric = df_metric.append(new_row, ignore_index=True)
        if safe:
            save_path = Path(__file__).resolve().parent.parent.parent
            save_path = os.path.join(save_path, 'prophet_gridseachcv_values.csv')
            df_metric.to_csv(save_path, sep='\t')

        print(df_metric.head)
        # get best parameters
        best_parameters = best_param(df_metric)
        # update parameters
        self.growth = best_parameters['growth']
        self.changepoint_prior_scale = best_parameters['changepoint_prior_scale']
        self.interval_width = best_parameters['interval_width']
        self.seasonality_mode = best_parameters['seasonality_mode']

        print(best_parameters)
        return best_parameters

    def load_best_param(self, label):
        """
        @brief: Loads the best parameters for the given dataset
        @param label: name of the dataset
        """
        self.set_dset(label)
        loaded_param = self.param[label]
        self.set_model(growth=loaded_param['growth'], changepoint_prior_scale=loaded_param['changepoint_prior_scale'],
                       interval_width=loaded_param['interval_width'], seasonality_mode=loaded_param['seasonality_mode'])
        self.set_cap(loaded_param['cap'])
        self.set_floor(loaded_param['floor'])

    def score(self, x, y, sample_weight=None):  # pylint: disable=arguments-differ
        """
        @brief: Evalute the Models performance via MSE
        @param x: dates to predict
        @param y: true values to that time
        @param sample_weight Possible interface for future sample weighting mechanisms.
        """
        y_true = y.copy()
        # Reset index for looking for nan to get the correct index to delete
        y_true = y_true.reset_index(drop=True)
        # get to predicting timestamps
        date = {'ds': x.iloc[:]}
        future = pd.DataFrame(data=date)
        # for logistic growth
        future['cap'] = self.cap
        future['floor'] = self.floor
        # make prediction
        forecast = self.model.predict(future)
        y_pred = forecast['yhat']

        # drop nan an adjust length of y_pred
        index = y_true.index[y_true.apply(np.isnan)]
        y_pred = y_pred.drop(index)
        y_true = y_true.dropna()
        if y_true.empty:
            return np.nan
        return r2_score(y_true, y_pred)

    def save_model(self):
        """
        @brief: Saves a model
        """
        with open(f"prophet{self.dset}_{dt.time}.pkl", 'wb') as f:
            pickle.dump(self.model, f)

    def load_model(self, dset, time):
        """
        @brief: Loads a pretrained model
        """
        with open(f"prophet{dset}_{time}.pkl", 'rb') as f:
            self.model = pickle.load(f)

    def set_params(self, **parameters):
        '''
        @brief: sets all the parameters that are given
        @param parameters: pointer to the location of the parameters
        '''
        # set default values
        growth = 'linear'
        changepoint_prior_scale = 0.05
        interval_width = 0.8
        seasonality_mode = 'additive'
        for parameter, value in parameters.items():
            if parameter == 'growth':
                growth = value
            if parameter == 'changepoint_prior_scale':
                changepoint_prior_scale = value
            if parameter == 'interval_width':
                interval_width = value
            if parameter == 'seasonality_mode':
                seasonality_mode = value

        self.set_model(growth=growth, changepoint_prior_scale=changepoint_prior_scale, interval_width=interval_width,
                       seasonality_mode=seasonality_mode)
        return self


def best_param(dataframe):
    """
    @brief: get the parameters which result in the best results
    @param dataframe: select best parameters given dataframe
    """
    idx = dataframe['metric'].idxmin()
    param = {'growth': dataframe['growth'][idx], 'changepoint_prior_scale': dataframe['changepoint_prior_scale'][idx],
             'interval_width': dataframe['interval_width'][idx], 'seasonality_mode': dataframe['seasonality_mode'][idx],
             'metric': dataframe['metric'][idx]}
    return param


def sklearn_gridsearch():
    """
    @brief: Test data on sklearn Gridsearchcv
    """
    attr = 'youtube_viewchange'
    dataframes = LoadIn().load_all(typ='pre')
    dataframes = dataframes.dropna()
    testframes = dataframes.iloc[-100:]
    dataframes = dataframes.iloc[:-100]

    print(dataframes[['Date', attr]].head())

    pro = MyProphet()

    changepoint_prior_scale = np.arange(0.03, 0.2, 0.005)
    parameters = {'growth': ['linear', 'logistic'],
                  'changepoint_prior_scale': changepoint_prior_scale,
                  'interval_width': [0.8],
                  'seasonality_mode': ['additive', 'multiplicative']}

    grid = GridSearchCV(estimator=pro, param_grid=parameters)
    grid.fit(dataframes['Date'], dataframes[attr])

    #  get best paramaters and set them
    best_parameters = grid.best_params_
    pro.growth = best_parameters['growth']
    pro.changepoint_prior_scale = best_parameters['changepoint_prior_scale']
    pro.interval_width = best_parameters['interval_width']
    pro.seasonality_mode = best_parameters['seasonality_mode']
    metric = grid.best_score_

    # set best model
    pro.set_model(after_best=True)

    # test if metric is correct
    metric_check = pro.score(x=testframes['Date'], y=testframes[attr])

    print('growth:', best_parameters['growth'], '\n',
          'changepoint_prior_scale:', best_parameters['changepoint_prior_scale'], '\n',
          'interval_width:', best_parameters['interval_width'], '\n',
          'seasonality_mode:', best_parameters['seasonality_mode'], '\n',
          'Best metric:', metric, '\n',
          'Metric Check', metric_check, '\n')

    print('Test_scroes: ', grid.cv_results_['mean_test_score'])

    # plot best
    pro.fit(x_date=dataframes['Date'], y_data=dataframes[attr])
    pro.predict(do_plot=True, label=attr)


def fbprophet_gridsearch():
    """
    @breif: Test data on fbprophet Gridsearchcv
    """
    attr = 'steam_users'
    dataframes = LoadIn().load_all(typ='pre')
    print(dataframes[['Date', attr]].head())

    pro = MyProphet()

    changepoint_prior_scale = np.arange(0.01, 0.12, 0.01)
    parameters = {'growth': ['linear', 'logistic'],
                  'changepoint_prior_scale': changepoint_prior_scale,
                  'interval_width': [0.8],
                  'seasonality_mode': ['additive', 'multiplicative']}

    best_parameters = pro.gridsearchcv(parameters, dataframe=dataframes[['Date', attr]], safe=True)
    print('growth:', best_parameters['growth'], '\n',
          'changepoint_prior_scale:', best_parameters['changepoint_prior_scale'], '\n',
          'interval_width:', best_parameters['interval_width'], '\n',
          'seasonality_mode:', best_parameters['seasonality_mode'], '\n',
          'metric:', best_parameters['metric'], '\n')

    # plot best
    pro.set_model(after_best=True)
    pro.fit(x_date=dataframes['Date'], y_data=dataframes[attr])
    pro.predict(do_plot=True, label=attr)


def test():
    """
    @brief: Test function
    """
    #########################################################
    # Gridseachcv with sklearn

    sklearn_gridsearch()

    ##########################################################
    # Gridsearchcv with fb crossval

    # fbprophet_gridsearch()

    ############################################################


if __name__ == '__main__':
    test()
