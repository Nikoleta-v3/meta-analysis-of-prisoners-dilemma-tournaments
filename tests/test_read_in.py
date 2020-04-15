import imp
import unittest

import axelrod
import numpy
import pandas

read_in = imp.load_source("read_in", "src/read_in.py")

df = read_in.strategies_properties()


def test_strategies_properties():
    assert isinstance(df, pandas.DataFrame)
    assert len(df) == len(axelrod.strategies)

    for memory_depth in df["Memory_depth"]:
        assert isinstance(memory_depth, float)

    for use_of_game in df["Makes_use_of_game"]:
        assert isinstance(use_of_game, bool)

    for use_of_length in df["Makes_use_of_length"]:
        assert isinstance(use_of_length, bool)


def test_specific_strategy_properties():

    tit_for_tat = df[df["Name"] == "Tit For Tat"]
    assert tit_for_tat.Name.all() == "Tit For Tat"
    assert tit_for_tat.Memory_depth.values == 1.0
    assert tit_for_tat.Stochastic.values == False
    assert tit_for_tat.Makes_use_of_game.values == 0.0
    assert tit_for_tat.Makes_use_of_length.values == 0.0

    adaptive = df[df["Name"] == "Adaptive"]
    assert adaptive.Name.all() == "Adaptive"
    assert adaptive.Memory_depth.values == numpy.inf
    assert adaptive.Stochastic.values == False
    assert adaptive.Makes_use_of_game.values == 1.0
    assert adaptive.Makes_use_of_length.values == 0.0


def test_parameters_data_frame():
    parameters_df = read_in.parameters_data_frame("data/raw_data/")

    assert isinstance(parameters_df, pandas.DataFrame)
    assert all(
        parameters_df.columns.values
        == ["index", "noise", "probend", "repetitions", "seed", "size", "turns"]
    )


parameters_df = read_in.parameters_data_frame("data/raw_data/")
row = parameters_df.sample(n=1)
reader = read_in.Reader(row, "data/raw_data/")


def test_reader_init():
    assert reader.noise_param.values[0] == row.noise.values[0]
    assert reader.probend_param.values[0] == row.probend.values[0]
    assert reader.seed.values[0] == row.seed.values[0]
    assert reader.size.values[0] == row["size"].values[0]
    assert reader.turns_param.values[0] == row.turns.values[0]


def test_get_noise_df():
    noise = reader.get_noise_df()
    assert isinstance(noise, pandas.DataFrame)
    assert all(
        noise.columns.values
        == [
            "Rank",
            "Name",
            "Median_score",
            "Cooperation_rating",
            "Wins",
            "Initial_C_rate",
            "CC_rate",
            "CD_rate",
            "DC_rate",
            "DD_rate",
            "CC_to_C_rate",
            "CD_to_C_rate",
            "DC_to_C_rate",
            "DD_to_C_rate",
            "noise",
            "turns",
        ]
    )


def test_get_probend_noise_df():
    probend_noise = reader.get_probend_noise_df()
    assert isinstance(probend_noise, pandas.DataFrame)
    assert all(
        probend_noise.columns.values
        == [
            "Rank",
            "Name",
            "Median_score",
            "Cooperation_rating",
            "Wins",
            "Initial_C_rate",
            "CC_rate",
            "CD_rate",
            "DC_rate",
            "DD_rate",
            "CC_to_C_rate",
            "CD_to_C_rate",
            "DC_to_C_rate",
            "DD_to_C_rate",
            "noise",
            "probend",
        ]
    )


def test_get_standar_df():
    std = reader.get_standar_df()
    assert isinstance(std, pandas.DataFrame)
    assert all(
        std.columns.values
        == [
            "Rank",
            "Name",
            "Median_score",
            "Cooperation_rating",
            "Wins",
            "Initial_C_rate",
            "CC_rate",
            "CD_rate",
            "DC_rate",
            "DD_rate",
            "CC_to_C_rate",
            "CD_to_C_rate",
            "DC_to_C_rate",
            "DD_to_C_rate",
            "turns",
        ]
    )


def test_get_proend_df():
    probend = reader.get_proend_df()
    assert isinstance(probend, pandas.DataFrame)
    assert all(
        probend.columns.values
        == [
            "Rank",
            "Name",
            "Median_score",
            "Cooperation_rating",
            "Wins",
            "Initial_C_rate",
            "CC_rate",
            "CD_rate",
            "DC_rate",
            "DD_rate",
            "CC_to_C_rate",
            "CD_to_C_rate",
            "DC_to_C_rate",
            "DD_to_C_rate",
            "probend",
        ]
    )


def test_reading_in_data():
    parameters_df = read_in.parameters_data_frame("data/raw_data/")
    parameters_df = parameters_df.sample(n=1)
    df = read_in.reading_in_data(parameters_df, "data/raw_data/")

    probend_data = df[df["turns"].isnull()]
    assert len(probend_data) == len(df[df["probend"].notnull()])
    assert list(probend_data.CC_rate) == list(
        df[df["probend"].notnull()].CC_rate
    )

    turns_data = df[df["probend"].isnull()]
    assert len(turns_data) == len(df[df["turns"].notnull()])
    assert list(turns_data.CC_rate) == list(df[df["turns"].notnull()].CC_rate)
    assert sum(df.turns.notnull()) + sum(df.probend.notnull()) == len(df)

    # some extra tests
    assert all(df.seed.notnull())
    assert all(df.repetitions.notnull())
    assert all(df["size"].notnull())
