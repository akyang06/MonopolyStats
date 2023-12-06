import random

NUM_SQUARES = 40  # total number of squares on a Monopoly board
NUM_GAMES = 1000000  # the total number of games to simulate
NUM_TURNS = 100  # the number of turns per game
GO_TO_JAIL = 30  # position of "Go to Jail"
JAIL = 10  # position of "Jail"

# Names of all the squares on a Monopoly board
square_names = [
    "Go", "Mediterranean Avenue", "Community Chest 1", "Baltic Avenue", "Income Tax", "Reading Railroad", "Oriental Avenue", "Chance 1", "Vermont Avenue", "Connecticut Avenue", "Jail / Just Visiting", "St. Charles Place", "Electric Company", "States Avenue", "Virginia Avenue", "Pennsylvania Railroad", "St. James Place", "Community Chest 2", "Tennessee Avenue", "New York Avenue", "Free Parking", "Kentucky Avenue", "Chance 2", "Indiana Avenue", "Illinois Avenue", "B. & O. Railroad", "Atlantic Avenue", "Ventnor Avenue", "Water Works", "Marvin Gardens", "Go to Jail", "Pacific Avenue", "North Carolina Avenue", "Community Chest 3", "Pennsylvania Avenue", "Short Line", "Chance 3", "Park Place", "Luxury Tax", "Boardwalk"
]

# Below are Chance and Community Chest cards that send the players to a 
# new position
# Note: in a full deck, there are also cards that do not result in a direct 
# move but we did not include them in this simulation because of their 
# complexity
chance_moves = {
    "Advance to Go": "Go",
    "Go to Jail": "Jail / Just Visiting",
    "Advance to Illinois Ave": "Illinois Avenue",
    "Advance to St. Charles Place": "St. Charles Place",
    "Take a trip to Reading Railroad": "Reading Railroad",
    "Advance to Boardwalk": "Boardwalk",
}

community_chest_moves = {
    "Advance to Go": "Go",
    "Go to Jail": "Jail / Just Visiting",
}

# simulates drawing a card that moves the player to a new position
def draw_card(cards_dict):
    card = random.choice(list(cards_dict.keys()))
    return square_names.index(cards_dict[card]) if card in cards_dict else None

def simulate_monopoly():
    # initialize a list to hold the count of landings on each square
    landings = [0] * NUM_SQUARES

    # simulate the games
    for _ in range(NUM_GAMES):
        position = 0  # position 0 represents "GO"
        consecutive_doubles = 0  # count of consecutive doubles rolled
        turns_in_jail = 0  # count of turns spent in jail

        for _ in range(NUM_TURNS):
            if turns_in_jail:
                # if the player lands in jail, simulate a roll to see if they get doubles to get out of jail or pay after 3 turns
                if random.randint(1, 6) == random.randint(1, 6) or turns_in_jail == 3:
                    turns_in_jail = 0  # Reset jail turn count
                else:
                    turns_in_jail += 1
                    continue 
            # rolling two six-sided dice
            die1, die2 = random.randint(1, 6), random.randint(1, 6)  
            if die1 == die2:
                consecutive_doubles += 1
            else:
                # reset doubles counter
                consecutive_doubles = 0
            
            if consecutive_doubles == 3:
                position = JAIL
                consecutive_doubles = 0  # reset doubles counter
                turns_in_jail = 1  # start jail turn count
            else:
                position = (position + die1 + die2) % NUM_SQUARES  # Move around the board
            
            if position == GO_TO_JAIL:
                position = JAIL
                turns_in_jail = 1  # start jail turn count

            landings[position] += 1  # incrementing the landing count for the current square
            
            # draw a card for Chance or Community Chest if those are landed on
            if "Chance" in square_names[position]:
                new_position = draw_card(chance_moves)
                if new_position is not None:
                    position = new_position
            elif "Community Chest" in square_names[position]:
                new_position = draw_card(community_chest_moves)
                if new_position is not None:
                    position = new_position

    # probability calculations
    total_landings = sum(landings)
    probabilities = [landings[i] / total_landings for i in range(NUM_SQUARES)]

    return probabilities, landings

# property : [price, per house, 1 house, 2 houses, 3 houses, 4 houses, hotel]
property_values = {
    "Mediterranean Avenue" : [60, 50, 10, 30, 90, 160, 250],
    "Oriental Avenue" : [100, 50, 30, 90, 270, 400, 550],
    "St. Charles Place" : [140, 100, 50, 150, 450, 625, 750],
    "St. James Place" : [180, 100, 70, 200, 550, 750, 950],
    "Kentucky Avenue": [220, 150, 90, 250, 700, 875, 1050],
    "Atlantic Avenue" : [260, 150, 100, 300, 750, 925, 1100],
    "Pacific Avenue" : [300, 200, 130, 390, 900, 1100, 1275],
    "Park Place" : [350, 200, 175, 500, 1100, 1300, 1500]
}

# run the simulation
monopoly_probabilities, landings = simulate_monopoly()

for i in range(len(landings)):
    landings[i] /= NUM_GAMES

def first_house():
    one_house = open("one_house.txt", mode="wt")

    budget = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]

    j = 0
    # one house
    for i in range(len(square_names)):
            # index into budget array
            
            # finding the initial cost of a given property if it has a value
            # associated with it
            for key in property_values.keys():
                if square_names[i] == key:
                    # get initial cost of property, subtract it from budget
                    init_square_cost = property_values[square_names[i]][0]
                    budget[j] = budget[j] - init_square_cost

                    # get profit when opponent lands on square
                    curr_square_cost = property_values[square_names[i]][2]
                    profit = landings[i] * curr_square_cost
                    
                    # add profit to budget
                    budget[j] += profit

                    # originally tried to account for monetary loss, but because
                    # of how we set up our simulation, we realized we were 
                    # losing money much faster than gaining from one square
                    # for x in range(len(budget)):
                    #     if x != j:
                    #         budget[x] -= curr_square_cost

                    j += 1
                    

    property_names = list(property_values.keys())

    for i in range(len(property_names)):
        one_house.write(property_names[i] + ": " + str(budget[i]) + "\n")
        
    one_house.close()

def second_house():
    two_houses = open("two_houses.txt", mode="wt")

    budget = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]

    j = 0
    # one house
    for i in range(len(square_names)):
            # index into budget array
            
            # finding the initial cost of a given property if it has a value
            # associated with it
            for key in property_values.keys():
                if square_names[i] == key:
                    # get initial cost of property, subtract it from budget
                    init_square_cost = property_values[square_names[i]][0] + property_values[square_names[i]][1]
                    budget[j] = budget[j] - init_square_cost

                    # get profit when opponent lands on square
                    curr_square_cost = property_values[square_names[i]][3]
                    profit = landings[i] * curr_square_cost
                    
                    # add profit to budget
                    budget[j] += profit
    
                    j += 1
                    

    property_names = list(property_values.keys())

    for i in range(len(property_names)):
        two_houses.write(property_names[i] + ": " + str(budget[i]) + "\n")
    two_houses.close()
    
def third_house():
    three_houses = open("three_houses.txt", mode="wt")

    budget = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]

    j = 0
    # one house
    for i in range(len(square_names)):
            # index into budget array
            
            # finding the initial cost of a given property if it has a value
            # associated with it
            for key in property_values.keys():
                if square_names[i] == key:
                    # get initial cost of property, subtract it from budget
                    init_square_cost = property_values[square_names[i]][0] + (2 * property_values[square_names[i]][1])
                    budget[j] = budget[j] - init_square_cost

                    # get profit when opponent lands on square
                    curr_square_cost = property_values[square_names[i]][4]
                    profit = landings[i] * curr_square_cost
                    
                    # add profit to budget
                    budget[j] += profit

                    j += 1
                    

    property_names = list(property_values.keys())

    for i in range(len(property_names)):
        three_houses.write(property_names[i] + ": " + str(budget[i]) + "\n")
    three_houses.close()

def fourth_house():
    four_houses = open("four_houses.txt", mode="wt")

    budget = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]

    j = 0
    # one house
    for i in range(len(square_names)):
            # index into budget array
            
            # finding the initial cost of a given property if it has a value
            # associated with it
            for key in property_values.keys():
                if square_names[i] == key:
                    # get initial cost of property, subtract it from budget
                    init_square_cost = property_values[square_names[i]][0] + (3 * property_values[square_names[i]][1])
                    budget[j] = budget[j] - init_square_cost

                    # get profit when opponent lands on square
                    curr_square_cost = property_values[square_names[i]][5]
                    profit = landings[i] * curr_square_cost
                    
                    # add profit to budget
                    budget[j] += profit

                    j += 1
                    

    property_names = list(property_values.keys())

    for i in range(len(property_names)):
        four_houses.write(property_names[i] + ": " + str(budget[i]) + "\n")
    four_houses.close()

def hotel():
    hotel = open("hotels.txt", mode="wt")

    budget = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]

    j = 0
    # one house
    for i in range(len(square_names)):
            # index into budget array
            
            # finding the initial cost of a given property if it has a value
            # associated with it
            for key in property_values.keys():
                if square_names[i] == key:
                    # get initial cost of property, subtract it from budget
                    init_square_cost = property_values[square_names[i]][0] + (4 * property_values[square_names[i]][1])
                    budget[j] = budget[j] - init_square_cost

                    # get profit when opponent lands on square
                    curr_square_cost = property_values[square_names[i]][5]
                    profit = landings[i] * curr_square_cost
                    
                    # add profit to budget
                    budget[j] += profit

                    j += 1
                    

    property_names = list(property_values.keys())

    for i in range(len(property_names)):
        hotel.write(property_names[i] + ": " + str(budget[i]) + "\n")
    hotel.close()

first_house()
second_house()
third_house()
fourth_house()
hotel()
