"""
Parameter file defining a singelton parameter class.
"""

import os
import datetime as dt


class Parameter:
    """
    This class contains parameters and methods to convert them.
    This is a Singleton object check for thread safety.
    Init with s = Parameter.getInstance()
    s = Parameter() will raise an exception.
    With each .getInstance you will get the same (id) object
    """
    DEBUG = True

    # private attributes PLEASE USE GETTER AND SETTER!!
    __instance = None
    __CWD = None
    __logfile_path = None

    @staticmethod
    def get_instance():
        """
        Static access method.
        Use instead of Parameter(). So you get everytime the same instance of the object.
        """
        if Parameter.__instance is None:
            Parameter()
            Parameter.__instance.__singelton_init()   # pylint: disable=protected-access

        return Parameter.__instance

    def __singelton_init(self):
        """
        This is the singelton init function if you want to init attributes do it here
        """
        self.working_directory = os.path.dirname(os.path.abspath(__file__))
        self.logfile_path = os.path.join(self.working_directory, 'documentation', 'logfiles', 'aml_log.log')
        self.__start_date_data = dt.datetime(2017, 1, 1)
        self.__end_date_data = dt.datetime(2020, 7, 1)

        # Financial Data
        # Corresponding Symbol Table -> /src/data_management/res/dailyCSV/financeAbbreviations.md
        self.__med_comp = ['EVT', 'SHL', 'BAS', 'BAYN', 'JNJ',
                           'PFE', 'FMS', 'FRE.DE', 'ABT', 'KMB',
                           'MDT', 'PHG', 'GE', 'BDX', 'CAH', 'SYK']

        self.__banking = ['DB', 'CMC', 'NCB', 'GS', 'BRYN', 'WFC',
                          'JPHLF', 'CICHY', 'ACGBY', 'CRARY', 'BACHF', 'C']

        self.__stock_index = ['DAX', 'TDXP', 'INDU', 'NDAQ', 'NKY']

        self.__energy_comp = ['SIEGY', 'EOAN.DE', 'RWE.DE',
                              'DUK', 'ENGI.PA', 'NGG', 'NEE', 'EDF']

        self.__oil_comp = ['CVX', 'XOM', 'PTR', 'XONA', 'RDS-A',
                           'LUK', 'ROSN', 'TOT', 'BP', 'SNP']

        self.__steel_comp = ['TKA.DE', 'MT', 'NISTF', 'PKX',
                             'SHE:000709', 'SHA:600019', 'SHE:002075']

        self.__automotive_comp = ['TM', 'GM', 'HYMTF', 'BMW.DE',
                                  'NSU', 'VOW.DE', 'DAI.DE', 'CON', 'TSLA']

        self.__telecom_comp = ['DTE', 'DRI', 'TEF', 'O2D.DE', 'T',
                               'TMUS', 'VOD', 'CTM', 'VZ', 'NTT.F',
                               'SFTBY', 'AMOV', 'CHA']

        self.__tec_comp = ['AAPL', 'AMZN', 'GOOGL', 'CCCMF',
                           'IFX.DE', 'SAP', 'CSCO', 'IBM', 'INL',
                           'INTC', 'MSF', 'EBAY', 'TWRT', 'QCOM',
                           'TXN', 'SNE']

        self.__finance_companies = (self.__med_comp + self.__energy_comp +
                                    self.__oil_comp + self.__steel_comp +
                                    self.__banking + self.__stock_index +
                                    self.__automotive_comp +
                                    self.__telecom_comp + self.__tec_comp)

        self.__folders = ['covid', 'finance', 'playstation', 'ix',
                          'socialblade', 'steam', 'twitch']

    def __init__(self):
        """Virtual private constructor."""
        if Parameter.__instance is not None:
            raise Exception("This class is a singleton!")

        Parameter.__instance = self
        self.__singelton_init()

    def get_working_directory(self):
        """Returns current working directory"""
        return self.working_directory

    def get_logfile_path(self):
        """Returns file path"""
        filepath = self.__logfile_path
        return filepath

    @property
    def start_date_data(self):
        """Getter method for start date of data collection"""
        return self.__start_date_data

    @start_date_data.setter
    def start_date_data(self, start_date):
        """Setter method for start date of data collection"""
        if isinstance(start_date, dt.date):
            self.__start_date_data = start_date
        else:
            raise Exception('Your start date is no valid datetime object!')

    @property
    def end_date_data(self):
        """Getter method for start date of data collection"""
        return self.__end_date_data

    @end_date_data.setter
    def end_date_data(self, start_date):
        """Setter method for start date of data collection"""
        if isinstance(start_date, dt.date):
            self.__end_date_data = start_date
        else:
            raise Exception('Your start date is no valid datetime object!')

    @property
    def stock_companies(self):
        """Getter method for stock companies list"""
        return self.__finance_companies

    @stock_companies.setter
    def stock_companies(self, companies_list):
        """Setter method for stock companies list"""
        print('I hope you know what you are doing, if not you`d better not do that')
        self.__finance_companies = companies_list

    @property
    def folders(self):
        """Getter method"""
        return self.__folders
