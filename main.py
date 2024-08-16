import os
from player import Player
from formation import Formation
from role import Role
import numpy as np
from scipy.optimize import linear_sum_assignment

import csv
import itertools
import random
import multiprocessing
n_runs = 1


def randomStart(players, formation):
    chosen_players = dict({})
    already_picked = set({})


    for role in formation:
        pick = random.choice(players)

        while pick in already_picked:
            pick = random.choice(players)
        chosen_players[role] = (formation[role], pick)
        already_picked.add(pick)
    return chosen_players

def initializePopulation(players, formation, population_size = 5, team_size = 11):

    population = []
    for i in range(population_size):
        population.append(randomStart(players, formation))
    return population

def crossOver(parent_1, parent_2):

    num_positions_to_swap = random.randint(0, len(parent_1.keys()))
    positions_to_swap = random.sample(list(parent_1.keys()), num_positions_to_swap)


    for position in positions_to_swap:
        if canSwap(position, parent_1, parent_2):        
            parent_1[position], parent_2[position] = parent_2[position], parent_1[position]

    return (parent_1, parent_2)

def canSwap(position, parent_one, parent_two):

    player_one = parent_one[position][1]
    player_two = parent_two[position][1]

    for player in parent_one:
        if parent_one[player][1] == player_two:
            return False
    for player in parent_two:
        if parent_two[player][1] == player_one:
            return False
        
    return True

def mutate(players, team):

    position_to_mutate = random.choice(list(team.keys()))
    mutated_player = random.choice(players)
    current_players = set({})
    for position in team:
        current_players.add(team[position][1])
    while mutated_player in current_players:
        mutated_player = random.choice(players)
    team[position_to_mutate] = (team[position_to_mutate][0], mutated_player)
    return team

def tournamentSelect(population, tournament_size = 3):

    participants = random.sample(population, tournament_size)
    fitness_scores = []
    for participant in participants:
        fitness_scores.append(evaluateTeam(participant))
    return participants[fitness_scores.index(max(fitness_scores))]

def evaluateTeam(team, forbidden_names = None):

    roles = Formation().roles
    score = 0
    perfect_score = 0
    #forbidden_names = ["Deniz Kahraman", "Yusuf Sertkaya", "Lokman Özlü", "Jack Platt", "Abdullah Koç", "Fatih Dalgıç", "Danny Burns",
    #                   "Tony García", "Charles Barkei", "Serkan Kazan", "Jovan Mijatović"]
    for position in team:
        for attribute in team[position][1].attributes:
            score += team[position][1].attributes[attribute]*team[position][0].weights[attribute]
            perfect_score += 20*team[position][0].weights[attribute]
        #if team[position][1].name in forbidden_names:
        #    return -120
        
    return (20*(score/(perfect_score/20)) - 120)

def evaluatePlayer(player, role):

    score = 0
    perfect_score = 0

    for attribute in role.weights:
        score += player.attributes[attribute]*role.weights[attribute]
        perfect_score += 20*role.weights[attribute]
    return (20*(score/(perfect_score/20)) - 120)

def geneticOptimization(players, formation, population_size = 4000, generations = 25, mutation_rate= 0.1, crossover_rate = 0.7, elitism = 0.0, min_max = False):

    best_individual = None
    population = initializePopulation(players, formation, population_size)
    best_fitness = float("-inf")
    fitness_scores = []
    selected_parents = []
    num_elites = int(elitism * population_size)
    for generation in range(generations):

        fitness_scores = [evaluateTeam(team) for team in population]
        sorted_population = [x for _, x in sorted(zip(fitness_scores, population), key = lambda pair: pair[0], reverse=True)]
        selected_parents = [tournamentSelect(sorted_population[num_elites:]) for _ in range(population_size)]

        new_population = sorted_population[:num_elites].copy()

        for i in range(0, population_size, 2):
            parent_one = selected_parents[i].copy()
            parent_two = selected_parents[i + 1].copy()
            if random.uniform(0, 1) < crossover_rate:
    
                child_one, child_two = crossOver(parent_one, parent_two)
                if random.uniform(0, 1) < mutation_rate:
                    child_one = mutate(players, child_one).copy()
                    child_two = mutate(players, child_two).copy()
                new_population.extend([child_one.copy(), child_two.copy()])
            else:
                if random.uniform(0, 1)< mutation_rate:
                    new_population.extend([mutate(players, parent_one), mutate(players, parent_two)])
        current_best_fitness = evaluateTeam(sorted_population[0])
        if current_best_fitness > best_fitness:
            print(f"Changing up best individual because: {current_best_fitness} > {best_fitness}")
            print(f"new best team has fitness: {current_best_fitness}")
            #generation = 0
            for position in sorted_population[0]:
                print(f"{position}: {sorted_population[0][position]}")
            print("------------------------------------------------------------")
            best_fitness = current_best_fitness
            best_individual = sorted_population[0].copy()


        new_population.extend([best_individual])
        population = new_population[:]
        print(f"Generation: {generation + 1}\n Best of this generation: {current_best_fitness} vs {best_fitness}")

    return best_individual

def getTeam(team_name):

    players = []
    with open(f"teams/{team_name}", "r", encoding= "utf-8") as file:
        lines = file.readlines()
        # Process the header to get attribute names
        lines = [line.strip() for line in lines if line.strip() and '---' not in line]
        headers = [header.strip() for header in lines[0].split("|") if header.strip()]
        headers = headers[1:]  # Skip 'Name' column in headers
        for line in lines[1:]:
            values = [value.strip() for value in line.split("|") if value.strip()]
            if len(values) == len(headers) + 1:  # Ensure there are enough values
                name = values[0]
                attributes = {headers[i]: int(values[i+1]) for i in range(len(headers))}
                players.append(Player(name=name, attributes=attributes))
    return players

def hungarianAlgorithm(players, tactic):
    profit_matrix = []
    # Build the profit matrix
    for player in players:
        temp_row = [-evaluatePlayer(player, tactic[position]) for position in tactic]
        profit_matrix.append(temp_row)
    
    # Make the matrix square by adding dummy roles
    num_players = len(profit_matrix)
    num_roles = len(profit_matrix[0])
    diff = num_players - num_roles

    if diff > 0:
        for i in range(num_players):
            profit_matrix[i].extend([0] * diff)
    elif diff < 0:
        print("Warning: More roles than players. Adding dummy players.")
        for i in range(-diff):
            profit_matrix.append([0] * num_roles + [0])
    profit_matrix = np.array(profit_matrix)

    row_ind, col_ind = linear_sum_assignment(profit_matrix)

    assignments = list(zip(row_ind, col_ind))
    return assignments

def main():
    team_files = []
    #gather all files within the teams folder
    for entry in os.listdir('./teams'):
        team_files.append(entry)
    print("Which team do you want to optimize for your tactic(If you don't see the team you want to use make sure the file is in the teams folder)?")
    for i in range(len(team_files)):
        print(f"{i + 1}: {team_files[i]}")
    team_file_name = team_files[int(input(": ")) - 1]
    roster = getTeam(team_file_name)
    roles = Formation().roles
    '''
    formation = {"GK": "SweeperKeeper-Defend", "LB": "InvertedFullBack-Defend", "CDL": "CentralDefender-Defend", "CDR": "CentralDefender-Defend", "RB": "InvertedWingback-Defend",
                 "DM": "DeepLyingPlayMaker-Defend", "MCL": "Mezalla-Support", "MCR": "Mezalla-Support", "AML": "Winger-Attack", 
                 "AMR": "Winger-Attack", "ST": "FalseNine-Support"
                 }
    formation = {"GK": "SweeperKeeper-Attack", "CDL": "WideCenterBack-Defend", "CDC": "CentralDefender-Defend", "CDR": "WideCenterBack-Defend", "LB": "CompleteWingback-Attack",
                 "MCL": "BallWinningMidFielder-Defend", "MC": "AdvancedPlayMaker-Support", "MCR": "BallWinningMidFielder-Defend", "RB": "CompleteWingback-Attack", "STL": "PressingForward-Support", 
                 "STR": "PressingForward-Support"
                 }
    formation =  {"GK": "SweeperKeeper-Attack", "LB": "InvertedWingback-Defend", "CDL": "CentralDefender-Defend", "CDR": "CentralDefender-Defend", "RB": "CompleteWingback-Attack",
                 "DM": "HalfBack-Defend", "MCL": "DeepLyingPlayMaker-Support", "MCR": "Mezalla-Attack", "MR": "WidePlaymaker-Attack", "ML": "Winger-Attack", "ST": "FalseNine-Support"
                 }
    '''

    formation =  dict({"GK": "SweeperKeeper-Attack", "CDL": "WideCenterBack-Defend", "CD": "CentralDefender-Defend", "CDR": "WideCenterBack-Defend",
                 "DML": "DefensiveMidfielder-Defend", "DMR": "DefensiveMidfielder-Defend", "MCL": "Mezalla-Attack", "MCR": "Mezalla-Attack",
                  "ML": "DefensiveWinger-Support", "MR": "DefensiveWinger-Support", "ST": "FalseNine-Support"
                 })

    for position in formation:
        formation[position] = roles[formation[position]]
    #team = [
    #        "SweeperKeeper-Defend", "InvertedFullBack-Defend", "InvertedWingback-Defend", "CentralDefender-Defend", "DeepLyingPlayMaker-Defend",
    #        "Mezalla-Support", "Winger-Attack", "FalseNine-Support"
    #        ]
    
    assignments = hungarianAlgorithm(roster, formation)
    assignments = [(row, col) for row, col in assignments if col < 11]
    print(f"Hungarian Optimization Squad:")
    keys = list(formation.keys())
    for assignment in assignments:
        print(f"{keys[assignment[1]]}: {roster[assignment[0]]}")
    
    print(f"Now lets do genetic Optimization and see if we get the same result")
    optimized_team = geneticOptimization(roster, formation)
    for position in optimized_team:
        print(f"{position}: {optimized_team[position]}")

if __name__ == "__main__":
    main()
