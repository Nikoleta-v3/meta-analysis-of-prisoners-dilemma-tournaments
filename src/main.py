"""
A script to run and summarise random tournaments.
"""

import axelrod as axl
import random
import glob

max_size = len(axl.strategies)  # Max number of strategies
turns = 100  # Number of turns of each tournament
repetitions = 200  # Number of repetitions
directory = "../data/"  # Directory in which to save the files

try:
    # Attempt to read directory to count number of tournaments that have been
    # run
    seed = max([int(f[len(directory):-4])
                for f in glob.glob("{}*csv".format(directory))])
    seed += 1
except ValueError:
    seed = 0

while True:
    axl.seed(seed)  # Seed the tournament

    # Select the strategies
    size = random.randint(2, 10)
    strategies = random.sample(axl.strategies, size)
    players = [s() for s in strategies]

    # Run the tournament
    tournament = axl.Tournament(players, turns=turns, repetitions=repetitions)
    results = tournament.play()
    results.write_summary("{}{}.csv".format(directory, seed))

    # Increment the seed
    seed += 1
