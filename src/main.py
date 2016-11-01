"""
A script to run and summarise random tournaments.

Generates:

    - <directory>/parameters.csv a csv file with parameters for each tournament
    - <directory>/data/<seed>.csv a csv file summarising a tournament for a
      given <seed>.
"""

import axelrod as axl
import pandas as pd
import random
import sys

max_size = len(axl.strategies)  # Max number of strategies
min_size = 3  # Min number of strategies

max_turns = 200
min_turns = 1

max_repetitions = 100
min_repetitions = 10

# Read the directory
try:
    directory = sys.argv[1]
except IndexError:
    directory = "../data/"

# Attempt to read directory to count number of tournaments that have been run
try:
    parameters_df = pd.read_csv("{}parameters.csv".format(directory))
    seed = int(parameters_df.seed.max() + 1)
except OSError:
    parameters_df = pd.DataFrame(columns=["seed", "size",
                                          "turns", "repetitions",
                                          "noise", "probend"])
    seed = 0

while True:
    # Define parameter
    axl.seed(seed)
    size = random.randint(min_size, max_size)
    strategies = random.sample(axl.strategies, size)
    players = [s() for s in strategies]
    next_sample = seed + 20

    while seed < next_sample:
        # Select the parameters
        turns = random.randint(min_turns, max_turns)
        repetitions = random.randint(min_repetitions, max_repetitions)
        noise = random.random()
        prob_end = random.random()
        df = pd.DataFrame([[seed, size, turns,
                            repetitions, noise, prob_end] + players],
                          columns=["seed", "size", "turns",
                                   "repetitions", "noise", "probend"] +
                                  ["player_{}".format(i) for i in range(size)])
        parameters_df = pd.concat([parameters_df, df], ignore_index=True)

        # Create the tournaments
        tournaments = []
        tournaments.append(axl.Tournament(players, turns=turns,
                                          repetitions=repetitions))
        tournaments.append(axl.Tournament(players, turns=turns,
                                          repetitions=repetitions, noise=noise))
        tournaments.append(axl.ProbEndTournament(players, prob_end=prob_end,
                                                 repetitions=repetitions))

        # Run the tournaments
        for tournament, name in zip(tournaments, ["std", "noise", "probend"]):
            axl.seed(seed)
            results = tournament.play(processes=0, progress_bar=False)
            results.write_summary("{}{}-data/{}.csv".format(directory, name,
                                                            seed))
        # Write the parameters for the complete tournament
        parameters_df.to_csv("{}parameters.csv".format(directory), index=False)

        # Increment the seed
        seed += 1
