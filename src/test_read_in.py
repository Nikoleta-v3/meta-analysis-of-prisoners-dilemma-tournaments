import unittest
import read_in
import axelrod
import pandas
import numpy


class TestStrategies(unittest.TestCase):
    df = read_in.strategies_properties()

    def test_strategies_properties(self):

        self.assertIsInstance(self.df, pandas.DataFrame)
        self.assertEqual(len(self.df), len(axelrod.strategies))
        self.assertTrue([nm.name for nm in axelrod.strategies],
                        self.df['Name'])
        for memory_depth in self.df['Memory_depth']:
            self.assertIsInstance(memory_depth, float)

        for use_of_game in self.df['Makes_use_of_game']:

            self.assertIsInstance(use_of_game, bool)

        for use_of_length in self.df['Makes_use_of_length']:
            self.assertIsInstance(use_of_length, bool)

    def test_specific_strategy_properties(self):

        tit_for_tat = self.df[self.df['Name'] == 'Tit For Tat']
        self.assertTrue(tit_for_tat.Name.all(), 'Tit For Tat')
        self.assertTrue(tit_for_tat.Memory_depth.all(), 1.0)
        self.assertFalse(tit_for_tat.Stochastic.all())
        self.assertEqual(tit_for_tat.Makes_use_of_game.all(), 0.0)
        self.assertEqual(tit_for_tat.Makes_use_of_length.all(), 0.0)

        adaptive = self.df[self.df['Name'] == 'Adaptive']
        self.assertTrue(adaptive.Name.all(), 'Adaptive')
        self.assertTrue(adaptive.Memory_depth.all(), numpy.inf)
        self.assertFalse(adaptive.Stochastic.all())
        self.assertEqual(adaptive.Makes_use_of_game.all(), 1.0)
        self.assertEqual(adaptive.Makes_use_of_length.all(), 0.0)


class TestParameters(unittest.TestCase):

    def test_pameters_data_frame(self):
        parameters_df = read_in.parameters_data_frame()

        self.assertIsInstance(parameters_df, pandas.DataFrame)
        self.assertEqual(len(parameters_df), 10002)
        self.assertTrue(parameters_df.columns.all(), ['noise', 'probend',
                                                      'repetitions', 'seed',
                                                      'size', 'turns'])


class TestReader(unittest.TestCase):
    parameters_df = read_in.parameters_data_frame()
    row = parameters_df.sample(n=1)
    reader = read_in.Reader(row)

    def test_reader_init(self):

        self.assertEqual(self.reader.noise_param.values[0],
                         self.row.noise.values[0])
        self.assertEqual(self.reader.probend_param.values[0],
                         self.row.probend.values[0])
        self.assertEqual(self.reader.seed.values[0],
                         self.row.seed.values[0])
        self.assertEqual(self.reader.size.values[0],
                         self.row['size'].values[0])
        self.assertEqual(self.reader.turns_param.values[0],
                         self.row.turns.values[0])

    def test_get_noise_df(self):
        noise = self.reader.get_noise_df()
        self.assertIsInstance(noise, pandas.DataFrame)
        self.assertTrue(noise.columns.all(), ['Rank', 'Name', 'Median_score',
                                              'Cooperation_rating', 'Wins',
                                              'CC_rate', 'CD_rate', 'DC_rate',
                                              'DD_rate', 'noise', 'turns',
                                              'repetitions', 'size', 'seed'])

    def test_get_probend_noise_df(self):
        probend_noise = self.reader.get_probend_noise_df()
        self.assertIsInstance(probend_noise, pandas.DataFrame)
        self.assertTrue(probend_noise.columns.all(), ['Rank', 'Name',
                                                      'Median_score',
                                                      'Cooperation_rating',
                                                      'Wins', 'CC_rate',
                                                      'CD_rate', 'DC_rate',
                                                      'DD_rate', 'noise',
                                                      'probend', 'repetitions',
                                                      'size', 'seed'])

    def test_get_standar_df(self):
        std = self.reader.get_standar_df()
        self.assertIsInstance(std, pandas.DataFrame)
        self.assertTrue(std.columns.all(), ['Rank', 'Name', 'Median_score',
                                            'Cooperation_rating', 'Wins',
                                            'CC_rate', 'CD_rate', 'DC_rate',
                                            'DD_rate', 'turns', 'repetitions',
                                            'size', 'seed'])

    def test_get_proend_df(self):
        probend = self.reader.get_proend_df()
        self.assertIsInstance(probend, pandas.DataFrame)
        self.assertTrue(probend.columns.all(), ['Rank', 'Name', 'Median_score',
                                                'Cooperation_rating', 'Wins',
                                                'CC_rate', 'CD_rate',
                                                'DC_rate',  'DD_rate',
                                                'probend', 'repetitions',
                                                'size', 'seed'])


class TestReadingIn(unittest.TestCase):
    parameters_df = read_in.parameters_data_frame()
    parameters_df = parameters_df.sample(n=2)

    def test_reading_in_data(self):
        df = read_in.reading_in_data(self.parameters_df)

        probend_data = df[df['turns'].isnull()]
        self.assertEqual(len(probend_data), len(df[df['probend'].notnull()]))
        self.assertEqual(list(probend_data.CC_rate),
                         list(df[df['probend'].notnull()].CC_rate))

        turns_data = df[df['probend'].isnull()]
        self.assertEqual(len(turns_data), len(df[df['turns'].notnull()]))
        self.assertEqual(list(turns_data.CC_rate),
                         list(df[df['turns'].notnull()].CC_rate))
        self.assertEqual(sum(df.turns.notnull()) + sum(df.probend.notnull()),
                         len(df))

        # some extra tests
        self.assertTrue(all(df.seed.notnull()))
        self.assertTrue(all(df.repetitions.notnull()))
        self.assertTrue(all(df['size'].notnull()))


