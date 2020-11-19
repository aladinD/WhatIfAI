""" !@brief File to start backend and handle incoming requests """

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import pandas as pd
from src.inference.model_comparison import get_predict_data as predictor

APP = Flask(__name__)
CORS(APP)

API = Api(APP)  # Require a parser to parse our POST request.
PARSER = reqparse.RequestParser()
PARSER.add_argument("dataset_id_req")
PARSER.add_argument("ping")
PARSER.add_argument("selected_graph")


class Switcher():
    """ !@brief Implemets a switch-case function in python to select the right dataset name for a specified ID """

    def dataset_switch(self, dataset_id):
        """
        !@brief Is used to select the right name for a specific dataset id
        @param Id of an dataset to recive the according name from
        @return For the specified integer ID in the dataset_swicht function,
        the name of the according dataset is returned as a string
        """

        default = "incorrect dataset"
        # getattr returns function from within the class, matching to 'dataset_id'
        # lambda gets returned, if not matching class was found
        return getattr(self, 'dataset_' + str(dataset_id), lambda: default)()

    @staticmethod
    def dataset_0():
        """ !@brief A switch case containing the datset name to an according id """
        return "ix_bitrate"

    @staticmethod
    def dataset_1():
        """ !@brief A switch case containing the datset name to an according id """
        return "youtube_viewchange"

    @staticmethod
    def dataset_2():
        """ !@brief A switch case containing the datset name to an according id """
        return "youtube_views"

    @staticmethod
    def dataset_3():
        """ !@brief A switch case containing the datset name to an according id """
        return "steam_users"

    @staticmethod
    def dataset_4():
        """ !@brief A switch case containing the datset name to an according id """
        return "steam_ingame"

    @staticmethod
    def dataset_5():
        """ !@brief A switch case containing the datset name to an according id """
        return "twitch_views"

    @staticmethod
    def dataset_6():
        """ !@brief A switch case containing the datset name to an according id """
        return "twitch_channels"

    @staticmethod
    def dataset_7():
        """ !@brief A switch case containing the datset name to an according id """
        return "twitch_viewtime"

    @staticmethod
    def dataset_8():
        """ !@brief A switch case containing the datset name to an according id """
        return "twitch_streams"

    @staticmethod
    def dataset_9():
        """ !@brief A switch case containing the datset name to an according id """
        return "ps_users"

    @staticmethod
    def dataset_10():
        """ !@brief A switch case containing the datset name to an according id """
        return "stock_med"

    @staticmethod
    def dataset_11():
        """ !@brief A switch case containing the datset name to an according id """
        return "stock_bank"

    @staticmethod
    def dataset_12():
        """ !@brief A switch case containing the datset name to an according id """
        return "stock_energy"

    @staticmethod
    def dataset_13():
        """ !@brief A switch case containing the datset name to an according id """
        return "stock_oil"

    @staticmethod
    def dataset_14():
        """ !@brief A switch case containing the datset name to an according id """
        return "stock_steel"

    @staticmethod
    def dataset_15():
        """ !@brief A switch case containing the datset name to an according id """
        return "stock_automotive"

    @staticmethod
    def dataset_16():
        """ !@brief A switch case containing the datset name to an according id """
        return "stock_telecom"

    @staticmethod
    def dataset_17():
        """ !@brief A switch case containing the datset name to an according id """
        return "stock_tech"


class Predict(Resource):
    """
    !@brief Is used to recive incoming requests, process the request and
    respond with an according response message
    """

    @staticmethod
    def post():
        """
        !@brief Is getting called, when a http request has been received.
        The content gets extracted and either a ping-return is sent or a ML-Model is loaded
        and predicts data for a requested dataset, which will be returned.
        """

        args = PARSER.parse_args()  # Sklearn is VERY PICKY on how you put your values in...

        print("\n---New request is processed---")
        print("Args: {}".format(args))

        if args["ping"] == "1":
            print("answered keep-alive")
            return {"alive": 1}

        # Print for checking parameter during development
        print("Received 'selected_graph' paramter: {}".format(args["selected_graph"]))

        # Switch statement depending on the requested dataset to reiceive the dataset name out of it´s ID.
        # The allocation from the id to the lable (name) can be found in /.../allocation_datasets_id.CSV
        dataset_lable = Switcher().dataset_switch(args["dataset_id_req"])

        # Use function to predict values and get raw and predicted data returned
        predicted_df, prophet_attr_df_post, prophet_attr_df_pre = predictor(dataset_lable)

        # Unpredicted data is processed
        # Received data is merged together with data up to and after the 1.1.2020.
        # Drop last row to not use it twice
        prophet_attr_df_pre = prophet_attr_df_pre.drop(prophet_attr_df_pre.index[-1])
        datasets_unpredicted = [prophet_attr_df_pre, prophet_attr_df_post]
        result_unpredicted = pd.concat(datasets_unpredicted)
        result_unpredicted.reset_index(inplace=True)

        # Get the index of the 2020-01-01 (where the rpediction starts)
        index_prediction_start = result_unpredicted.loc[result_unpredicted["Date"] == "2020-01-01"].index.item()

        # Predicted data processed
        # Change data type into pandas series
        result_predicted = pd.Series(predicted_df)

        # Generate lists out of dataframes to send to frontend
        complete_unpredicted_data = result_unpredicted[dataset_lable].to_list()
        complete_model_data = result_predicted.to_list()
        complete_predicted_data = result_predicted.to_list()
        result_dates = result_unpredicted["Date"].to_list()

        for index in range(index_prediction_start, len(complete_model_data)):
            complete_model_data[index] = None

        for index in range(0, index_prediction_start - 1):
            complete_predicted_data[index] = None

        # The return statement will be sent to the frontend.
        return {"class": 42,
                "datecheck": 2,
                "chart_data_1": complete_unpredicted_data,
                "chart_data_2": complete_model_data,
                "chart_data_3": complete_predicted_data,
                "labels": result_dates,
                "selected_graph": args["selected_graph"]
                }


API.add_resource(Predict, "/predict")


def main():
    """ !@brief Main function """
    print("Starting server.")
    APP.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    main()
