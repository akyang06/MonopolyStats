# Simple simulation which only simulates rolling two die and following their movements, no game rules or movement logic to affect the results 

import random

NUM_SQUARES = 40  # total number of squares on a Monopoly board
NUM_GAMES = 100000  # the total number of games to simulate
NUM_TURNS = 100  # the number of turns per game

# names of the squares on a Monopoly board
square_names = [
    "Go", "Mediterranean Avenue", "Community Chest 1", "Baltic Avenue", "Income Tax", "Reading Railroad", "Oriental Avenue", "Chance 1", "Vermont Avenue", "Connecticut Avenue", "Jail / Just Visiting", "St. Charles Place", "Electric Company", "States Avenue", "Virginia Avenue", "Pennsylvania Railroad", "St. James Place", "Community Chest 2", "Tennessee Avenue", "New York Avenue", "Free Parking", "Kentucky Avenue", "Chance 2", "Indiana Avenue", "Illinois Avenue", "B. & O. Railroad", "Atlantic Avenue", "Ventnor Avenue", "Water Works", "Marvin Gardens", "Go to Jail", "Pacific Avenue", "North Carolina Avenue", "Community Chest 3", "Pennsylvania Avenue",
    "Short Line", "Chance 3", "Park Place", "Luxury Tax", "Boardwalk"
]

def simulate_monopoly():
    # initialize a list to hold the count of landings on each square
    landings = [0] * NUM_SQUARES

    # simulates the games
    for _ in range(NUM_GAMES):
        position = 0  # position 0 marks 'Go'
        for _ in range(NUM_TURNS):
            # simulates rolling two six-sided dice
            roll = random.randint(1, 6) + random.randint(1, 6)  
            position = (position + roll) % NUM_SQUARES  # to move around the board
            landings[position] += 1  # increments the landing count for the current square

    # calculates probabilities
    total_landings = sum(landings)
    probabilities = [landings[i] / total_landings for i in range(NUM_SQUARES)]

    return probabilities

# runs the simulation
monopoly_probabilities = simulate_monopoly()

# write percentages to files
names = open("square_names_simple.txt", mode="wt")
percentages = open("square_percentages_simple.txt", mode="wt")

for square, probability in enumerate(monopoly_probabilities):
    names.write(square_names[square] + "\n")
    percentages.write(str(probability) + "\n")
names.close()
percentages.close()

