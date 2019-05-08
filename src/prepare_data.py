import glob
import sys

import pandas as pd

import axelrod as axl


def strategies_properties():
    """
     A function that returns a data frame with the strategies of the Axelrod
     library and for each strategy it's property.
    """
    axl_strategies = pd.DataFrame(
        columns=[
            "Name",
            "Stochastic",
            "Memory_depth",
            "Makes_use_of_game",
            "Makes_use_of_length",
        ]
    )

    for i, strategy in enumerate(axl.strategies):
        use_of_game = False
        use_of_length = False

        if "game" in strategy().classifier["makes_use_of"]:
            use_of_game = True
        if "length" in strategy().classifier["makes_use_of"]:
            use_of_length = True
        axl_strategies.loc[i] = [
            strategy().name,
            strategy().classifier["stochastic"],
            strategy().classifier["memory_depth"],
            use_of_game,
            use_of_length,
        ]
    return axl_strategies


def get_parameters_data_frame(directory):
    """
    A function for reading in the parameters data frame.
    """
    csv_files = glob.glob("{}parameters_*-*.csv".format(directory))
    dfs = (pd.read_csv(f) for f in csv_files)
    df = pd.concat(dfs)
    df = df[["noise", "probend", "repetitions", "seed", "size", "turns"]]

    return df.sort_values(["seed"]).reset_index()


class Reader:
    """
    A class for retrieving the four data frames corresponding to each
    row of the parameters csv file.
    """

    def __init__(self, row, directory=None):
        if directory:
            self.directory = directory
        else:
            self.directory = "data/raw_data/"
        self.seed = row.seed
        self.size = row["size"]
        self.repetitions = row.repetitions
        self.noise_param = row.noise
        self.probend_param = row.probend
        self.turns_param = row.turns

    def get_noise_df(self):
        noise = pd.read_csv(
            "{}noise-data/{}.csv".format(self.directory, int(self.seed))
        )
        noise["noise"] = self.noise_param
        noise["turns"] = self.turns_param

        return noise

    def get_probend_noise_df(self):
        probend_noise = pd.read_csv(
            "{}noise-probend-data/{}.csv".format(self.directory, int(self.seed))
        )
        probend_noise["noise"] = self.noise_param
        probend_noise["probend"] = self.probend_param

        return probend_noise

    def get_standard_df(self):
        std = pd.read_csv(
            "{}std-data/{}.csv".format(self.directory, int(self.seed))
        )
        std["turns"] = self.turns_param
        return std

    def get_proend_df(self):
        probend = pd.read_csv(
            "{}probend-data/{}.csv".format(self.directory, int(self.seed))
        )
        probend["probend"] = self.probend_param

        return probend

    def common_rows(self, df):
        df["repetitions"] = self.repetitions
        df["size"] = self.size
        df["seed"] = self.seed

        return df


def prepare_type_dataframes(parameters_df, directory):
    """
    A function for reading in each of the 4 data sets for a given parameters
    row. It concats everything together and returns a pandas Data Frame.
    """
    std_frames, noise_frames, probend_frames, noise_probend_frames = (
        [],
        [],
        [],
        [],
    )
    for _, row in parameters_df.iterrows():
        reader = Reader(row, directory)

        std = reader.get_standard_df()
        std = reader.common_rows(std)
        std_frames.append(std)

        noise = reader.get_noise_df()
        noise = reader.common_rows(noise)
        noise_frames.append(noise)

        probend = reader.get_proend_df()
        probend = reader.common_rows(probend)
        probend_frames.append(probend)

        probend_noise = reader.get_probend_noise_df()
        probend_noise = reader.common_rows(probend_noise)
        noise_probend_frames.append(probend_noise)

        data_frames = [
            pd.concat(frames, ignore_index=True)
            for frames in [
                std_frames,
                noise_frames,
                probend_frames,
                noise_probend_frames,
            ]
        ]
    return data_frames


if __name__ == "__main__":

    directory = sys.argv[1]
    labels = ["standard", "noise", "probend", "probend_noise"]

    print("Reading parameters data frames.")
    parameters_df = get_parameters_data_frame(directory)
    print("Creating type data frames.")
    dfs = prepare_type_dataframes(parameters_df, directory)

    # if sys.argv[2] == "extra_columns":
    #     print("Extra columns")
    #     pass

    print("Exporting data frames.")
    for df, label in zip(dfs, labels):
        df.to_csv("data/%s.csv" % label)
