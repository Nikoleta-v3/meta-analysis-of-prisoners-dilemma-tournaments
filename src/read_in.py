import pandas as pd
import axelrod as axl


def strategies_properties():
    """
     A function that returns a data frame with the strategies of the Axelrod
     library and for each strategy it's property.
    """
    axl_strategies = pd.DataFrame(columns=['Name', 'Stochastic',
                                           'Memory_depth', 'Makes_use_of_game',
                                           'Makes_use_of_length'])

    for i, strategy in enumerate(axl.strategies):
        use_of_game = 0
        use_of_length = 0

        if 'game' in strategy.classifier['makes_use_of']:
            use_of_game = 1
        if 'length' in strategy.classifier['makes_use_of']:
            use_of_length = 0
        axl_strategies.loc[i] = [strategy.name,
                                 strategy.classifier['stochastic'],
                                 strategy.classifier['memory_depth'],
                                 use_of_game,
                                 use_of_length]
    return axl_strategies


def parameters_data_frame():
    """
    A function for reading in the parameters data frame.
    """
    df = pd.read_csv("../data/parameters.csv")
    df = df[['noise', 'probend', 'repetitions', 'seed', 'size', 'turns']]

    return df


class Reader():
    """
    A class for retrieving the four data frames corresponding to each
    row of the parameters csv file.
    """

    def __init__(self, row):
        self.seed = row.seed
        self.size = row['size']
        self.repetitions = row.repetitions
        self.noise_param = row.noise
        self.probend_param = row.probend
        self.turns_param = row.turns

    def get_noise_df(self):
        noise = pd.read_csv('../data/noise-data/{}.csv'.format(int(self.seed)))
        noise['noise'] = [self.noise_param for _ in range(len(noise))]
        noise['turns'] = [self.turns_param for _ in range(len(noise))]

        return noise

    def get_probend_noise_df(self):
        probend_noise = pd.read_csv('../data/noise-probend-data/{}.csv'.format(
                                                                int(self.seed)))
        probend_noise['noise'] = [self.noise_param
                                  for _ in range(len(probend_noise))]
        probend_noise['probend'] = [self.probend_param
                                    for _ in range(len(probend_noise))]

        return probend_noise

    def get_standar_df(self):
        std = pd.read_csv('../data/std-data/{}.csv'.format(int(self.seed)))
        std['turns'] = [self.turns_param for _ in range(len(std))]

        return std

    def get_proend_df(self):
        probend = pd.read_csv('../data/probend-data/{}.csv'.format(int(
                                                                    self.seed)))
        probend['probend'] = [self.probend_param for _ in range(len(probend))]

        return probend

    def common_rows(self, df):
        for i in range(len(df)):
            df[i]['repetitions'] = [self.repetitions for _ in range(len(df[i]))]
            df[i]['size'] = [self.size for _ in range(len(df[i]))]
            df[i]['seed'] = [self.seed for _ in range(len(df[i]))]

        return df


def reading_in_data(parameters_df):
    """
    A function for reading in each of the 4 data sets for a given parameters
    row. It concats everything together and returns a pandas Data Frame.
    """
    data_frame = []
    for i in parameters_df.index:
        dfs = []
        row = parameters_df.loc[i]
        reader = Reader(row)

        # get noise
        noise = reader.get_noise_df()
        dfs.append(noise)

        # get probend noise
        probend_noise = reader.get_probend_noise_df()
        dfs.append(probend_noise)

        # get standar
        std = reader.get_standar_df()
        dfs.append(std)

        # get probend
        probend = reader.get_proend_df()
        dfs.append(probend)

        # add the common params
        dfs = reader.common_rows(dfs)

        data_frame.append(dfs)

    return data_frame

# parameters_df = parameters_data_frame()
# df = reading_in_data(parameters_df)
# strategies_df = strategies_properties()
#
# final_df = pd.merge(df, strategies_df, on='Name')
# final_df.to_csv('data.csv')