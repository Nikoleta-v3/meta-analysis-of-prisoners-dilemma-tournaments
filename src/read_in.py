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
        use_of_game = False
        use_of_length = False

        if 'game' in strategy.classifier['makes_use_of']:
            use_of_game = True
        if 'length' in strategy.classifier['makes_use_of']:
            use_of_length = True
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
        noise['noise'] = self.noise_param
        noise['turns'] = self.turns_param

        return noise

    def get_probend_noise_df(self):
        probend_noise = pd.read_csv('../data/noise-probend-data/{}.csv'.format(
                                                                int(self.seed)))
        probend_noise['noise'] = self.noise_param
        probend_noise['probend'] = self.probend_param


        return probend_noise

    def get_standar_df(self):
        std = pd.read_csv('../data/std-data/{}.csv'.format(int(self.seed)))
        std['turns'] = self.turns_param
        return std

    def get_proend_df(self):
        probend = pd.read_csv('../data/probend-data/{}.csv'.format(int(
                                                                    self.seed)))
        probend['probend'] = self.probend_param

        return probend

    def common_rows(self, df):
        df['repetitions'] = self.repetitions
        df['size'] = self.size
        df['seed'] = self.seed

        return df


def reading_in_data(parameters_df):
    """
    A function for reading in each of the 4 data sets for a given parameters
    row. It concats everything together and returns a pandas Data Frame.
    """
    list_frames = []
    for _, row in parameters_df.iterrows():
        reader = Reader(row)

        # get noise
        noise = reader.get_noise_df()
        noise = reader.common_rows(noise)
        list_frames.append(noise)

        # get probend noise
        probend_noise = reader.get_probend_noise_df()
        probend_noise = reader.common_rows(probend_noise)
        list_frames.append(probend_noise)

        # get standar
        std = reader.get_standar_df()
        std = reader.common_rows(std)
        list_frames.append(std)

        # get probend
        probend = reader.get_proend_df()
        probend = reader.common_rows(probend)
        list_frames.append(probend)

    data_frame = pd.concat(list_frames, ignore_index=True)

    return data_frame

