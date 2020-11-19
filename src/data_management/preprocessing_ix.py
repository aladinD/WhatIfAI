"""
Everything related to preprocessing - might be extended to a whole package if required
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sns.set(rc={'figure.figsize': (11, 4)})
RESOURC_PATH = '../../res/ix'


def read_dataset(path, name):
    """
    Reads dataset
    """
    return pd.read_csv(os.path.join(path, name + '.csv'))


def main():
    """!@brief Main function of the script.

    Parses arguments, registers the client and starts containers for all jobs that were specified.
    """
    data = read_dataset(RESOURC_PATH, 'all')
    _, axs = plt.subplots(2, 1, constrained_layout=True)
    axs[0].plot(data["Date"], data["bitrate"], 'o', )
    plt.show()
    print('done')


if __name__ == "__main__":
    main()
