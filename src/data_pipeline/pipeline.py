"""!@brief Pipeline to process the gathered data from our sources.
@details Scales the data, computes running averages for time series where deemed appropriate and saves the scaled data
set into two files. One contains all data prior to the corona pandemic start (which we determined to be at 01.01.2020),
and the other one all data points from during the pandemic.
@file Data pipeline file.
@author Martin Schuck
@date 11.8.2020
"""


from pathlib import Path
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import sector_tuple_list, index_codes


def pipeline(verbose=False, plot=False):
    """!@brief Pipeline process to filter, process, sum and scale the raw data.

    Saves the resulting data frames into two files at /res/pipeline.

    @param verbose Toggles verbose output over the terminal.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    # Load the raw data set and clean dirty columns.
    data_frame = load_data_set(verbose=verbose)

    # Get the data frame index for 01.01.2020 to separate pre and post corona data.
    end_date = '2020-01-01'
    end_index = data_frame.index[(data_frame['Date'] == end_date).values][0]

    # Execute processing steps.
    df_processing(data_frame, plot=plot)
    # Clean data frame and rename into a unified naming scheme.
    clean_df(data_frame)
    if verbose:
        data_frame.info()
    # Split data set into a pre corona data set and a corona data set. Scale both appropriately.
    scaled_pre_corona_df, scaled_corona_df, scaler = scale_split_df(data_frame, end_index=end_index)
    if plot:
        fig = plt.figure(figsize=(24, 24))
        axis = fig.add_axes([0, 0, 1, 1])
        pd.plotting.scatter_matrix(scaled_pre_corona_df, ax=axis)
        plt.show()
        fig = plt.figure(figsize=(24, 24))
        axis = fig.add_axes([0, 0, 1, 1])
        pd.plotting.scatter_matrix(scaled_corona_df, ax=axis)
        plt.show()
    save_individual_scalers(scaled_pre_corona_df)
    # Save data frame.
    save_df(scaled_pre_corona_df, scaled_corona_df, scaler)


def load_data_set(verbose=False):
    """!@brief Loads the raw data frame from the resource folder.

    @param verbose Toggles verbose output over the terminal.
    """
    root = Path().absolute().parent.parent
    dataset_path = root.joinpath('res', 'all_raw.csv')

    data_frame = pd.read_csv(dataset_path)
    if verbose:
        data_frame.info()

    data_frame.drop('Unnamed: 0', axis=1, inplace=True)
    data_frame.drop('Unnamed: 0.1', axis=1, inplace=True)
    data_frame['Date'] = data_frame['Date'].apply(lambda x: x[:-15])  # Drop the UTC string part.
    return data_frame


def df_processing(data_frame, plot=False):
    """!@brief Runs the individual processing steps for the data.

    @param data_frame The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    processing_collection = [corona_processing, ix_processing, playstation_processing, steam_processing,
                             twitch_processing, socialblade_processing, stock_processing]
    for function in processing_collection:
        function(data_frame, plot=plot)


def corona_processing(data_frame, plot):
    """!@brief Corona processing function.

    @param data_frame The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    data_frame['deaths'].fillna(0, inplace=True)
    data_frame['recovered'].fillna(0, inplace=True)
    data_frame['active'].fillna(0, inplace=True)
    data_frame['confirmed'].fillna(0, inplace=True)
    data_frame['new_confirmed'].fillna(0, inplace=True)
    data_frame['new_recovered'].fillna(0, inplace=True)
    data_frame['new_deaths'].fillna(0, inplace=True)
    if plot:
        corona_processing_plot(data_frame)


def corona_processing_plot(data_frame):
    """!@brief Plots the results from the corona processing.

    @param data_frame The data frame to use for plotting.
    """
    covid_df = data_frame.melt('Date', value_vars=['deaths', 'recovered', 'active', 'confirmed', 'new_confirmed',
                                                   'new_recovered', 'new_deaths'],
                               var_name='cols', value_name='vals')
    graph = sns.lineplot(x="Date", y="vals", hue='cols', data=covid_df)
    graph.set_xticks(np.arange(0, len(data_frame['Date']), 300))
    graph.plot()
    plt.show()


def ix_processing(data_frame, plot):
    """!@brief IX processing function.

    @param data_frame The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    data_frame['bitrate'] = data_frame['bitrate'].rolling(7, win_type='triang', min_periods=1).sum()
    # Drop outliers at the very beginning.
    for idx in range(181, 184):
        data_frame.at[idx, 'bitrate'] = np.nan
    if plot:
        ix_processing_plot(data_frame)


def ix_processing_plot(data_frame):
    """!@brief Plots the results from the IX processing.

    @param data_frame The data frame to use for plotting.
    """
    ix_df = data_frame.melt('Date', value_vars=['bitrate'], var_name='cols', value_name='vals')

    graph = sns.lineplot(x="Date", y="vals", hue='cols', data=ix_df)
    graph.set_xticks(np.arange(0, len(data_frame['bitrate']), 300))
    graph.plot()
    plt.show()


def playstation_processing(data_frame, plot):
    """!@brief Playstation processing function.

    @param data_frame The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    ps_keys = ['PS3', 'PS4', 'Vita']
    if all(key in data_frame.keys() for key in ps_keys):
        data_frame['PS'] = data_frame['PS3'] + data_frame['PS4'] + data_frame['Vita']
        data_frame.drop('PS3', axis=1, inplace=True)
        data_frame.drop('PS4', axis=1, inplace=True)
        data_frame.drop('Vita', axis=1, inplace=True)
        # Smooth time series with rolling average.
        data_frame['PS'] = data_frame['PS'].rolling(7, win_type='triang', min_periods=1).sum()
    else:
        print('Warning: Keys not present in playstation_processing in src/data_pipeline/pipeline.py')
        return
    # Drop outliers at the data frame edges.
    for idx in range(0, 5):
        data_frame.at[idx, 'PS'] = np.nan
    for idx in range(1215, 1225):
        data_frame.at[idx, 'PS'] = np.nan

    if plot:
        playstation_processing_plot(data_frame)


def playstation_processing_plot(data_frame):
    """!@brief Plots the results from the playstation processing.

    @param data_frame The data frame to use for plotting.
    """
    ps_df = data_frame.melt('Date', value_vars=['PS'], var_name='cols', value_name='vals')

    graph = sns.lineplot(x="Date", y="vals", hue='cols', data=ps_df)
    graph.set_xticks([0, 600, 1200])
    graph.plot()
    plt.show()


def steam_processing(data_frame, plot):
    """!@brief Steam processing function.

    @param data_frame The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    data_frame['Users'] = data_frame['Users'].rolling(14, win_type='triang', min_periods=1).sum()
    data_frame['In-Game'] = data_frame['In-Game'].rolling(14, win_type='triang', min_periods=1).sum()
    # Drop outliers at the edges of the data frame.
    for idx in range(315, 327):
        data_frame.at[idx, 'Users'] = np.nan
        data_frame.at[idx, 'In-Game'] = np.nan
    for idx in range(1261, 1272):
        data_frame.at[idx, 'Users'] = np.nan
        data_frame.at[idx, 'In-Game'] = np.nan
    if plot:
        steam_processing_plot(data_frame)


def steam_processing_plot(data_frame):
    """!@brief Plots the results from the steam processing.

    @param data_frame The data frame to use for plotting.
    """
    steam_df = data_frame.melt('Date', value_vars=['Users', 'In-Game'], var_name='cols', value_name='vals')

    graph = sns.lineplot(x="Date", y="vals", hue='cols', data=steam_df)
    graph.set_xticks(np.arange(0, len(data_frame['Users']), 300))
    graph.plot()
    plt.show()


def twitch_processing(data_frame, plot):
    """!@brief Twitch processing function.

    @param data_frame The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    # Drop outliers at the end of the data frame.
    data_frame.at[1247, 'time_watched'] = np.nan
    data_frame.at[1247, 'active_streamers'] = np.nan
    data_frame['av_conc_viewers'].interpolate(method='polynomial', order=3, inplace=True)
    data_frame['av_conc_channels'].interpolate(method='polynomial', order=3, inplace=True)
    data_frame['time_watched'].interpolate(method='polynomial', order=3, inplace=True)
    data_frame['active_streamers'].interpolate(method='polynomial', order=3, inplace=True)
    if plot:
        twitch_processing_plot(data_frame)


def twitch_processing_plot(data_frame):
    """!@brief Plots the results from the twitch processing.

    @param data_frame The data frame to use for plotting.
    """
    _, axes = plt.subplots(2, 2, sharex=False, sharey=False, figsize=(10, 10))

    twitch_df0 = data_frame.melt('Date', value_vars=['av_conc_viewers'], var_name='cols', value_name='vals')
    twitch_df1 = data_frame.melt('Date', value_vars=['av_conc_channels'], var_name='cols', value_name='vals')
    twitch_df2 = data_frame.melt('Date', value_vars=['time_watched'], var_name='cols', value_name='vals')
    twitch_df3 = data_frame.melt('Date', value_vars=['active_streamers'], var_name='cols', value_name='vals')

    graph0 = sns.lineplot(x="Date", y="vals", hue='cols', data=twitch_df0, ax=axes[0, 0])
    graph1 = sns.lineplot(x="Date", y="vals", hue='cols', data=twitch_df1, ax=axes[0, 1])
    graph2 = sns.lineplot(x="Date", y="vals", hue='cols', data=twitch_df2, ax=axes[1, 0])
    graph3 = sns.lineplot(x="Date", y="vals", hue='cols', data=twitch_df3, ax=axes[1, 1])
    graph0.set_xticks(np.arange(0, len(data_frame['av_conc_viewers']), 400))
    graph1.set_xticks(np.arange(0, len(data_frame['av_conc_channels']), 400))
    graph2.set_xticks(np.arange(0, len(data_frame['time_watched']), 400))
    graph3.set_xticks(np.arange(0, len(data_frame['active_streamers']), 400))
    graph0.plot()
    graph1.plot()
    graph2.plot()
    graph3.plot()
    plt.show()


def socialblade_processing(data_frame, plot):
    """!@brief Socialblade processing function.

    @param data_frame The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    data_frame['Weekly_average_change_views'] = data_frame['Weekly_average_change_views'].\
        interpolate(method='polynomial', order=3)
    data_frame['Weekly_average_change_views'] = data_frame['Weekly_average_change_views'].rolling(20, win_type='triang',
                                                                                                  min_periods=1).sum()

    data_frame['Weekly_average_views'] = data_frame['Weekly_average_views'].interpolate(method='polynomial', order=3)
    mask = np.arange(0, len(data_frame.Weekly_average_views))
    mask = mask < 905
    data_frame.loc[mask, 'Weekly_average_views'] = np.where(data_frame.loc[mask, 'Weekly_average_views'] > 3000000, 0,
                                                            data_frame.loc[mask, 'Weekly_average_views'])
    data_frame.loc[:, 'Weekly_average_views'] = np.where(data_frame.loc[:, 'Weekly_average_views'] < 0, 0,
                                                         data_frame.loc[:, 'Weekly_average_views'])
    weights = np.linspace(1, 4, 905)
    data_frame.loc[mask, 'Weekly_average_views'] = data_frame.loc[mask, 'Weekly_average_views'].to_numpy() * weights

    data_frame['Weekly_average_views'] = data_frame['Weekly_average_views'].rolling(40, win_type='triang',
                                                                                    min_periods=1).sum()
    if plot:
        socialblade_processing_plot(data_frame)


def socialblade_processing_plot(data_frame):
    """!@brief Plots the results from the socialblade processing.

    @param data_frame The data frame to use for plotting.
    """
    _, axes = plt.subplots(1, 2, sharex=False, sharey=False, figsize=(15, 15))
    socialblade_df0 = data_frame.melt('Date', value_vars=['Weekly_average_change_views'],
                                      var_name='cols', value_name='vals')
    socialblade_df1 = data_frame.melt('Date', value_vars=['Weekly_average_views'], var_name='cols', value_name='vals')
    graph0 = sns.lineplot(x="Date", y="vals", hue='cols', data=socialblade_df0, ax=axes[0])
    graph1 = sns.lineplot(x="Date", y="vals", hue='cols', data=socialblade_df1, ax=axes[1])

    graph0.set_xticks(np.arange(0, len(data_frame['Weekly_average_change_views']), 300))
    graph0.set_title('Weekly_average_change_views')
    graph1.set_xticks(np.arange(0, len(data_frame['Weekly_average_views']), 300))
    graph1.set_title('Weekly_average_views')

    graph0.plot()
    graph1.plot()
    plt.show()


def stock_processing(data_frame, plot):
    """!@brief Stock processing function.

    @param data_frame The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    # Some keys were saved wrong, other stock codes contain mostly dirty information. Rename wrong named ones and delete
    # garbage information stocks determined by visual data inspection.
    data_frame['PTR'] = data_frame['PTR_x']
    data_frame['EBAY'] = data_frame['EBAY_x']
    for key in ['EBAY_x', 'EBAY_y', 'PTR_x', 'PTR_y', 'SHL', 'BAYN', 'JPHLF', 'SHE:002075', 'CON', 'CCCMF', 'INL']:
        if key in data_frame.keys():
            data_frame.drop(key, axis=1, inplace=True)

    # Interpolate stock data to avoid missing values due to NaN sums.
    for domain in sector_tuple_list:
        for code in domain.stock_code_list:
            if code in data_frame.keys():
                data_frame[code].interpolate(inplace=True)
        nomalized_average = sum([(data_frame[stock] - data_frame[stock].mean()) / data_frame[stock].std()
                                 for stock in domain.stock_code_list if stock in data_frame.keys()])
        data_frame[domain.df_column_name] = nomalized_average / len(domain.stock_code_list)
        data_frame[domain.df_column_name].replace(min(data_frame[domain.df_column_name]), np.nan, inplace=True)
        data_frame[domain.df_column_name].interpolate(method='polynomial', order=3, inplace=True)
    if plot:
        stock_processing_plot(data_frame)


def stock_processing_plot(data_frame):  # pylint: disable-msg=too-many-locals
    """!@brief Plots the results from the stock processing.

    @param data_frame The data frame to use for plotting.
    """
    med_df = data_frame.melt('Date', value_vars=['stock_med'], var_name='cols', value_name='vals')
    bank_df = data_frame.melt('Date', value_vars=['stock_bank'], var_name='cols', value_name='vals')
    energy_df = data_frame.melt('Date', value_vars=['stock_energy'], var_name='cols', value_name='vals')
    oil_df = data_frame.melt('Date', value_vars=['stock_oil'], var_name='cols', value_name='vals')
    steel_df = data_frame.melt('Date', value_vars=['stock_steel'], var_name='cols', value_name='vals')
    automotive_df = data_frame.melt('Date', value_vars=['stock_automotive'], var_name='cols', value_name='vals')
    telecom_df = data_frame.melt('Date', value_vars=['stock_telecom'], var_name='cols', value_name='vals')
    tech_df = data_frame.melt('Date', value_vars=['stock_tech'], var_name='cols', value_name='vals')

    fig, axes = plt.subplots(4, 2, sharex=False, sharey=False, figsize=(15, 15))
    graph0 = sns.lineplot(x="Date", y="vals", hue='cols', data=med_df, ax=axes[0, 0])
    graph1 = sns.lineplot(x="Date", y="vals", hue='cols', data=bank_df, ax=axes[0, 1])
    graph2 = sns.lineplot(x="Date", y="vals", hue='cols', data=energy_df, ax=axes[1, 0])
    graph3 = sns.lineplot(x="Date", y="vals", hue='cols', data=oil_df, ax=axes[1, 1])
    graph4 = sns.lineplot(x="Date", y="vals", hue='cols', data=steel_df, ax=axes[2, 0])
    graph5 = sns.lineplot(x="Date", y="vals", hue='cols', data=automotive_df, ax=axes[2, 1])
    graph6 = sns.lineplot(x="Date", y="vals", hue='cols', data=telecom_df, ax=axes[3, 0])
    graph7 = sns.lineplot(x="Date", y="vals", hue='cols', data=tech_df, ax=axes[3, 1])

    graph0.set_xticks(np.arange(0, 801, 200))
    graph0.set_title('Average medical stock performance')
    graph1.set_xticks(np.arange(0, 801, 200))
    graph1.set_title('Average finance stock performance')
    graph2.set_xticks(np.arange(0, 801, 200))
    graph2.set_title('Average energy stock performance')
    graph3.set_xticks(np.arange(0, 801, 200))
    graph3.set_title('Average oil stock performance')
    graph4.set_xticks(np.arange(0, 801, 200))
    graph4.set_title('Average steel stock performance')
    graph5.set_xticks(np.arange(0, 801, 200))
    graph5.set_title('Average automotive stock performance')
    graph6.set_xticks(np.arange(0, 801, 200))
    graph6.set_title('Average telecom stock performance')
    graph7.set_xticks(np.arange(0, 801, 200))
    graph7.set_title('Average tech stock performance')

    graph0.plot()
    graph1.plot()
    graph2.plot()
    graph3.plot()
    graph4.plot()
    graph5.plot()
    graph6.plot()
    graph7.plot()

    fig.tight_layout()
    plt.show()


def index_processing(data_frame, plot):
    """!@brief Stock index processing function.

    @param data_frame The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    for code in index_codes:
        data_frame[code] = (data_frame[code] - data_frame[code].mean()) / data_frame[code].std()
    if plot:
        index_processing_plot(data_frame)


def index_processing_plot(data_frame):
    """!@brief Plots the results from the stock index processing.

    @param data_frame The data frame to use for plotting.
    """
    dax_df = data_frame.melt('Date', value_vars=['DAX'], var_name='cols', value_name='vals')
    ndaq_df = data_frame.melt('Date', value_vars=['NDAQ'], var_name='cols', value_name='vals')

    fig, axes = plt.subplots(1, 2, sharex=False, sharey=False, figsize=(15, 4))
    graph0 = sns.lineplot(x="Date", y="vals", hue='cols', data=dax_df, ax=axes[0])
    graph1 = sns.lineplot(x="Date", y="vals", hue='cols', data=ndaq_df, ax=axes[1])

    graph0.set_xticks(np.arange(0, 801, 200))
    graph0.set_title('DAX performance')
    graph1.set_xticks(np.arange(0, 801, 200))
    graph1.set_title('NDAQ performance')

    graph0.plot()
    graph1.plot()

    fig.tight_layout()
    plt.show()


def clean_df(data_frame, verbose=False):
    """!@brief Dataframe cleaning function.

    Removes unnecessary columns and messy keys. Also unifies the naming scheme.

    @param data_frame The data frame to process.
    @param verbose Toggles verbose output over the terminal.
    """
    for domain in sector_tuple_list:
        for code in domain.stock_code_list:
            if code in data_frame.keys():
                data_frame.drop(code, axis=1, inplace=True)

    for code in index_codes:
        if code in data_frame.keys():
            data_frame.drop(code, axis=1, inplace=True)

    messy_key_list = ['TDXP', 'INDU', 'NKY']
    for key in messy_key_list:
        if key in data_frame.keys():
            data_frame.drop(key, axis=1, inplace=True)

    # Unify naming scheme.
    data_frame.rename(columns={'deaths': 'corona_deaths', 'confirmed': 'corona_confirmed',
                               'recovered': 'corona_recovered', 'active': 'corona_active',
                               'new_recovered': 'corona_new_recovered', 'new_deaths': 'corona_new_deaths',
                               'bitrate': 'ix_bitrate', 'Weekly_average_change_views': 'youtube_viewchange',
                               'Weekly_average_views': 'youtube_views', 'Users': 'steam_users',
                               'In-Game': 'steam_ingame', 'av_conc_viewers': 'twitch_views',
                               'av_conc_channels': 'twitch_channels', 'time_watched': 'twitch_viewtime',
                               'active_streamers': 'twitch_streams', 'PS': 'ps_users'}, inplace=True)
    if verbose:
        data_frame.info()


def scale_split_df(data_frame, end_index):
    """!@brief Data frame split and scaling.

    Scales the data with a fitted standard scaler from pre Corona times. Splits the data sets into two sets, one for pre
    Corona, one for during Corona.

    @param data_frame The data frame to process.
    @param end_index Index of the 01.01.2020 in the data set.
    """
    # Rearrange column order to make scaling easy.
    cols = data_frame.columns.tolist()
    cols = cols[8:26] + cols[1:7] + [cols[0]]
    data_frame = data_frame[cols]

    pre_corona_df = data_frame.truncate(after=end_index)
    corona_df = data_frame.truncate(before=end_index)

    scaler = StandardScaler()
    column_transformer = ColumnTransformer([('scaler', scaler, np.arange(0, 24))], remainder='passthrough')
    scaled_pre_corona_data = column_transformer.fit_transform(pre_corona_df)
    # Only transform, do not fit with corona data.
    scaled_corona_data = column_transformer.transform(corona_df)

    scaled_pre_corona_df = pd.DataFrame(columns=pre_corona_df.columns, data=scaled_pre_corona_data.copy())
    scaled_corona_df = pd.DataFrame(columns=corona_df.columns, data=scaled_corona_data.copy())

    for key in corona_df.keys():
        if not key == 'Date':
            scaled_pre_corona_df[key] = pd.to_numeric(scaled_pre_corona_df[key], downcast="float")
            scaled_corona_df[key] = pd.to_numeric(scaled_corona_df[key], downcast="float")
    return scaled_pre_corona_df, scaled_corona_df, column_transformer


def save_df(scaled_pre_corona_df, scaled_corona_df, scaler):
    """!@brief Saves the data frames as well as the scaler.

    @param scaled_pre_corona_df The pre Corona data frame.
    @param scaled_corona_df The during Corona data frame.
    @param scaler The fitted scaler for the data sets.
    """
    root = Path().absolute().parent.parent

    scaled_pre_corona_df_path = root.joinpath('res', 'pipeline', 'scaled_pre_corona_df.csv')
    scaled_corona_df_path = root.joinpath('res', 'pipeline', 'scaled_corona_df.csv')

    scaled_pre_corona_df.to_csv(scaled_pre_corona_df_path)
    scaled_corona_df.to_csv(scaled_corona_df_path)

    # Save the scaler.
    joblib.dump(scaler, root.joinpath('res', 'pipeline', 'scaler.save'))
    print('Data sets saved.')


def save_individual_scalers(scaled_pre_corona_df):
    """!@brief Saves the individual scalers into a folder for later inverse transform.

    @param scaled_pre_corona_df The scaled pre corona data frame that is used for the individual transformers.
    """
    root = Path().absolute().parent.parent
    for column in scaled_pre_corona_df:
        if not column == 'Date':
            print(root.joinpath('res', 'pipeline', f'scaler_{column}.save'))
            st_scaler = StandardScaler()
            st_scaler.fit(scaled_pre_corona_df[column].values.reshape(-1, 1))

            # Save the scaler.
            joblib.dump(st_scaler, root.joinpath('res', 'pipeline', f'scaler_{column}.save'))
    print('Scalers saved.')


if __name__ == '__main__':
    pipeline(verbose=False, plot=False)
