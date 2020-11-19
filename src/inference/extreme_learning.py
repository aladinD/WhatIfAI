'''
File implemanting Extrem Learning Machine (ELM).
I tried to make this class scjíkit learn compatibel
(see :https://scikit-learn.org/stable/developers/develop.html)

How to use this class:
(1) Run fit before predict!
(2) The input for the fit method are the stacked time series data!
    As you get (for every attribute) from :
    x_train_test, y_train_test = elm.prepare_data(loaded_data['stock_automotive'])
'''
import datetime
from pathlib import Path
from keras import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn import linear_model

# For scikitlearn cross validation
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

# Constants
TRAIN_WINDOW = 30


# Extreme Learning Class
class ExtremeLearningMachine(BaseEstimator, ClassifierMixin):
    '''
    Implementation of extreme Learning machine.
    As proposed in paper from Guang-Bin Huang.
    Can be used like any scikit learn predictor.
    '''

    def __init__(self, neurons=128, lambd=0.01, regu='L1',
                 __measure='mse', weights=None, train_window=None,
                 model=None):
        '''
        The params define the neural network!
        @param data : the dataset in sequential form
        @param layer : number of layers of the network
        @param neurons : number of neurons
        @param activation : activation function of the neurons
        @param train_window : number of inputs for the net
        @param error_measure : error measure e.g mse
        '''
        self.lambd = lambd
        self.neurons = neurons
        self.regu = regu

        self.__measure = __measure
        self.weights = weights
        self.train_window = train_window
        self.model = model

    def fit(self, x_train, y_train):
        '''
        The weights of the Extreme Learning Readout
        are calculated in the following method.
        We fit a single data attribute! But with the same nn!
        '''
        # To be scikit learn comp we build the model outside the init method
        self.build_network()
        self.__measure = 'mse'
        error_tol = 0.01

        transformed_features = self.model.predict(x_train)

        # Simple way without Regularization
        if self.regu == 'no':
            sol_eqs = np.linalg.lstsq(transformed_features, y_train, rcond=None)
            self.weights = sol_eqs[0]

        # Lasso regularization
        elif self.regu == 'L1':
            lasso = linear_model.Lasso(alpha=self.lambd, fit_intercept=False, tol=error_tol)
            lasso.fit(transformed_features, y_train)
            self.weights = np.array(lasso.coef_)

        # Ridge regression
        elif self.regu == 'L2':
            ridge = linear_model.Ridge(alpha=self.lambd, fit_intercept=False, tol=error_tol)
            ridge.fit(transformed_features, y_train)
            self.weights = np.array(ridge.coef_)

        else:
            raise Exception('No valid regularization selected')

    def score(self, x_test, y_test):  # pylint: disable=arguments-differ
        '''
        Scoring method returns test error
        '''
        y_predict = self.predict(x_test)

        if self.__measure == 'mse':
            error = self.mse(y_predict, y_test)

        elif self.__measure == 'mae':
            error = self.mae(y_predict, y_test)

        # Default value == MSE
        else:
            error = self.mse(y_predict, y_test)

        return error

    def predict(self, x_vals):
        '''
        Predict method
        '''
        if self.weights is None:
            raise Exception("Need to call fit() before predict()")

        # I really do not know why this is needed
        if x_vals.shape == (self.train_window,):
            x_vals = x_vals.reshape(1, -1)
        features = self.model.predict(x_vals)
        return np.matmul(features, self.weights)

    def predict_next_days(self, regu, lambd, num_neurons, train_win,
                          do_plot=False, data=None, days=None, date=None):
        '''
        Method that predicts the next days. You can also hand a model (ELM) to this method.
        @param days : Number of days you want to predict.
        @param date : Optional you can select a date till you cant to predict.
        @param data : Data on which we w<nt to train the model and start predictions
        @param model :
        '''
        if data is None:
            raise Exception('Extreme learning machine.predict_next_days : No valid data!')

        if (days is None and date is None):
            raise Exception('Extreme Learning Machine predict_next_days : days and date is None')

        elif days is None:
            today = datetime.date.today()
            days = date - today

        # Set params
        self.lambd = lambd
        self.neurons = num_neurons
        self.regu = regu
        self.train_window = train_win

        # At this point we can be sur that days is defined
        # last_elements = data[-(self.train_window):len(data)].copy()

        # build and train network
        x_train, y_train = self.prepare_data(data)
        self.fit(x_train, y_train)
        last_elements = x_train[-1]

        # First predict
        predictions = []

        # predict using last data points
        for _ in range(days):
            value = self.predict(last_elements)
            predictions = np.append(predictions, value)

            # Insert prediction and delet first element
            last_elements = np.delete(last_elements, 0)
            last_elements = np.append(last_elements, value)

        if do_plot:
            num_x = len(data) + days
            x_values = range(num_x)
            plt.title(data.name)
            plt.plot(x_values[0:len(data)], data, label='Data')
            plt.plot(x_values[len(data):], predictions, label='Prediction')
            plt.show()

        return predictions

    def build_network(self, neurons=128, layers=1, train_window=TRAIN_WINDOW,
                      activation='relu', metric='mean_squared_error'):
        '''error_measure
        Method that builds and compiles the model (network)
        '''
        # Init neural network
        self.train_window = train_window
        self.model = Sequential()
        self.model.add(Dense(neurons,
                             activation=activation,
                             input_shape=(train_window,),
                             bias_initializer='glorot_uniform'))
        for _ in range(1, layers):
            self.model.add(Dense(neurons, activation=activation))
        self.model.compile(loss=metric, optimizer='adam')
        # self.model._make_predict_function()

        # Regression part
        self.weights = None

    def prepare_data(self, data, train_window=TRAIN_WINDOW):
        '''
        Shifting method that generates a x and y like dataset
        out of a time series.
        @param data: 1-D List containing the data.
        '''
        x_train_test = []
        y_train_test = []

        for iterator in range(self.train_window, len(data)):
            x_vals = data[(iterator-train_window):iterator]
            x_train_test.append(x_vals)
            y_train_test.append(data[iterator])

        # Cast this stuff to numpy
        x_train_test = np.array(x_train_test)
        y_train_test = np.array(y_train_test)

        return x_train_test, y_train_test

    # Error measure dependent things
    def get_error_measure(self):
        '''
        Getter method error measure
        '''
        return self.__measure

    def set_error_measure(self, error_measure):
        '''
        Setter method for error measure.
        @param error_measure : error measure e.g mse, mae
        @return : boolean value indicates if we seted the value or not
        '''
        bool_ret = False
        if isinstance(self.__measure, str):
            if (self.__measure == 'mse' or self.__measure == 'mae'):
                self.__measure = error_measure
                bool_ret = True
            else:
                print('{} is no valid Error measure for ELM'.format(error_measure))
                bool_ret = False
        else:
            print('Your input is not even a string =(')
            bool_ret = False
        return bool_ret

    def mse(self, y_real, y_predict):
        '''
        Calculate mean squared error
        '''
        difference_array = np.subtract(y_real, y_predict)
        squared_array = np.square(difference_array)
        mse = squared_array.mean()
        return mse

    def mae(self, y_real, y_predict):
        '''
        Calculate the Mean Absolute error
        '''
        difference_array = np.subtract(y_real, y_predict)
        abs_array = np.abs(difference_array)
        error = abs_array.mean()
        return error

    # Prpoerties
    error_measure = property(get_error_measure, set_error_measure)


def test_cv():
    ''' Test running sckikit learn cross validation'''
    root = Path().absolute().parent.parent
    dataset_path = root.joinpath('AML', 'group11', 'res', 'pipeline', 'scaled_corona_df.csv')
    loaded_data = pd.read_csv(dataset_path)
    elm = ExtremeLearningMachine()

    # Test if it works as expected
    my_train_attr = ['stock_automotive', 'stock_energy']
    for attr in my_train_attr:
        # First step prepare dat
        x_train_test, y_train_test = elm.prepare_data(loaded_data[attr])
        scores = cross_val_score(elm, x_train_test, y_train_test, cv=5, scoring='r2')
        print('scores ELM:')
        print(scores)


def test_grid_search():
    ''' Test running sckikit learn cross validation'''
    root = Path().absolute().parent.parent
    dataset_path = root.joinpath('AML', 'group11', 'res', 'pipeline', 'scaled_corona_df.csv')
    loaded_data = pd.read_csv(dataset_path)
    elm = ExtremeLearningMachine()

    # Test if it works as expected
    my_train_attr = ['stock_automotive', 'stock_energy']
    for attr in my_train_attr:
        print(elm.get_params())

        # First step prepare dat
        x_train_test, y_train_test = elm.prepare_data(loaded_data[attr])
        # Set the parameters by cross-validation
        tuned_parameters = {'neurons': [10, 20],
                            'lambd': [0.001, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5],
                            'regu': ['no', 'L1', 'L2']}
        clf = GridSearchCV(ExtremeLearningMachine(),
                           tuned_parameters)
        clf.fit(x_train_test, y_train_test)
        print(clf.best_params_)


def test():
    ''' Test running sckikit learn cross validation'''
    root = Path().absolute().parent.parent
    dataset_path = root.joinpath('AML', 'group11', 'res', 'pipeline', 'scaled_corona_df.csv')
    loaded_data = pd.read_csv(dataset_path)

    days_to_predict = 60
    elm = ExtremeLearningMachine()

    my_train_attr = ['stock_automotive', 'stock_energy']
    for attr in my_train_attr:
        train_size = len(loaded_data) - days_to_predict
        train_data = loaded_data[attr][:train_size]
        test_data = loaded_data[attr][train_size:]
        predictions = elm.predict_next_days(regu='no', train_win=TRAIN_WINDOW, do_plot=False,
                                            lambd=0.01, num_neurons=128, days=days_to_predict,
                                            data=train_data)

        x_values = range(len(loaded_data))
        plt.title('No name')
        plt.plot(x_values[:train_size], train_data, label='Train data')
        plt.plot(x_values[train_size:], predictions, label='Prediction')
        plt.plot(x_values[train_size:], test_data, label='Test data')
        plt.legend()
        plt.show()


if __name__ == '__main__':
    test()
    # test_cv()
    # test_grid_search()
