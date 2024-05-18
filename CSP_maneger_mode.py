#!/usr/bin/env python
#coding:utf-8

import pandas as pd
import itertools

def csp(candidates, players, team, requested_positions_attributes, budget):
    if len(requested_positions_attributes) == 0: 
        suggested_positions = team_positional_needs(candidates, team)
        print("No positions specified; suggesting based on following weaknesses:")
        print(suggested_positions)
        backtracking(candidates.to_dict(orient='records'), players, team, suggested_positions, budget)
    else:
        requested_positions = positions(requested_positions_attributes)
        backtracking(candidates.to_dict(orient='records'), players, team, requested_positions, budget)

def hill_climb(candidates, init_state, team, requested_positions_attributes, budget):
    cur_state = init_state
    while True:
        print_output(cur_state)
        print(heur(cur_state, requested_positions_attributes, budget))
        neighbors = generate_neighbors(candidates, cur_state, team, budget)
        best_neighbor = max(neighbors, key=lambda x: heur(x, requested_positions_attributes, budget))
        if heur(best_neighbor, requested_positions_attributes, budget) <= heur(cur_state, requested_positions_attributes, budget):
            return cur_state
        cur_state = best_neighbor

def heur(players, requested_positions_attributes, budget):
    result = 0.0
    rating_comp = 0.0
    budget_comp = 0.0
    attr_comp = 0.0
    for player in players:
        rating_comp += player['rating'] / len(players)
        budget_comp += 2.5 * proportion_of_budget(player, budget)
    if len(players) != 0:
        attr_comp = 2 * max_attribute_assignment_value(players, requested_positions_attributes) / len(players)

    # print(rating_comp)
    # print(budget_comp)
    # print(attr_comp)

    result += rating_comp
    result += budget_comp
    result += attr_comp

    return result

# Report: How to explain why weights are good?
# Demo that ratings are high while we're still getting 
# Ideally: Figure out how to print attribute assigned to each player and said attribute/player value

def positions(requested_positions_attributes):
    requested_positions = []
    for x in requested_positions_attributes:
        requested_positions.append(x[0])
    return requested_positions

def attributes_at_position(requested_positions_attributes, pos):
    requested_attributes = []
    for x in requested_positions_attributes:
        if x[0] == pos:
            requested_attributes.append(x[1])
    return requested_attributes

def max_attribute_assignment_value(players, requested_positions_attributes):
    # print("Heur computation process")
    requested_positions = unique_positions(players)
    result = 0.0
    for position in requested_positions:
        players_at_pos = players_at_position(players, position)
        position_attributes = attributes_at_position(requested_positions_attributes, position)
        max_position_sum = -20.0
        attribute_permutations = list(itertools.permutations(position_attributes))
        for permutation in attribute_permutations:
            cur_position_sum = 0.0
            for i in range(len(players_at_pos)):
                if not permutation[i] == 'None':
                    cur_position_sum += players_at_pos[i][permutation[i]]
            max_position_sum = max(max_position_sum, cur_position_sum)
            # print("{}: {}".format(permutation, cur_position_sum))
        result += max_position_sum
    return result

def total_price(players):
    result = 0
    for player in players:
        result += player['price']
    return result

def proportion_of_budget(player, budget):
    return player['price'] / budget

def unique_positions(players):
    result = set()
    for player in players:
        result.add(player['position'])
    return result

def players_at_position(players, pos):
    result = []
    for player in players:
        if player['position'] == pos:
            result.append(player)
    return result

def generate_neighbors(candidates, players, team, budget):
    result = []
    for pos in unique_positions(players):
        candidates_pos = candidates[candidates['position'] == pos]
        for cur_player in players_at_position(players, pos):
            for _, new_player in candidates_pos.iterrows():
                if new_player.to_dict() not in players and new_player['team'] != team:
                    new_state_players = players.copy()
                    new_state_budget = total_price(players)
                    new_state_players.remove(cur_player)
                    new_state_budget -= cur_player['price']
                    new_state_players.append(new_player.to_dict())
                    new_state_budget += new_player['price']
                    if new_state_budget <= budget:
                        result.append(new_state_players)
    return result

def team_common_players_positions(common_players_data, team):
    df_team_roster = common_players_data[common_players_data['Squad'] == team]
    df_team_roster = df_team_roster.sort_values(by=['90s'], ascending=False)
    return df_team_roster['sub_position'].tolist()[:11]

def team_positional_needs(candidates, team):
    df_team_roster = candidates[candidates['team'] == team]
    df_common_players = df_team_roster[df_team_roster['games'] >= 10]

    print("Before normalization")
    print(df_common_players[['name', 'rating']])

    text_cols = df_common_players.select_dtypes(include='object')

    numerical_cols = df_common_players.select_dtypes(include=['float', 'int'])
    normalized_numerical_cols = (numerical_cols - numerical_cols.mean()) / numerical_cols.std()

    df_common_players_norm = pd.concat([normalized_numerical_cols, text_cols], axis=1)

    print("After normalization")
    print(df_common_players_norm[['name', 'rating']])

    df_common_weaknesses = df_common_players_norm[df_common_players_norm['rating'] < -1]
    df_common_weaknesses = df_common_weaknesses.sort_values(by=['rating'], ascending=True)

    print("Weaknesses")
    print(df_common_weaknesses[['name', 'rating']])
    if len(df_common_weaknesses) == 0:
        # Find the index of the row with the lowest rating
        min_rating_index = df_common_players_norm['rating'].idxmin()

        # Get the position of the row with the lowest rating
        position_lowest_rating = df_common_players_norm.at[min_rating_index, 'position']
        print("Lowest rating position is:", position_lowest_rating)
        return [position_lowest_rating]

    return df_common_weaknesses['position'].to_list()[:5]

# Unique Non-GK Positions:
# Attacking Midfield (M)
# Central Midfield (M)
# Centre-Back (D)
# Centre-Forward (F)
# Defensive Midfield (M)
# Left Winger (F)
# Left-Back (D)
# Right Winger (F)
# Right-Back (D)
# Second Striker (F)

def backtracking(candidates, players, team, requested_positions, budget):

    if len(requested_positions) == 0:
        return True

    else:
        candidates_temp = candidates.copy()
        requested_positions_updated = requested_positions.copy()
        while(len(candidates_temp) > 0):
            player = candidates.pop(0) # in the candidates list, to be checked
            if Is_valid(player, team, requested_positions, budget):
                players.append(player)
                requested_positions_updated.remove(player['position'])
                candidates_temp.remove(player)
                if backtracking(candidates_temp, players, team, requested_positions_updated, budget - player['price']):
                    return True
                players.pop()
                requested_positions_updated.append(player['position'])
                candidates_temp.append(player)
    return False

def Is_valid(player, team, requested_positions, budget): # Done psudo code check validation

    # the constraint
    # financial constraints

    # print("Budget  = {}, this player's price = {}".format(budget, player['price']))
    if budget < player['price'] : # financial constraint failed
        # print("Budget insufficient")
        return False
    
    # Position constraints
    # if requested_positions[0] != player['position']:
    if player['position'] not in requested_positions:
        # print("Not looking for this position")
        return False

    # Don't need to get players already on this team!
    if player['team'] == team:
        return False
         
    # print("Player is valid")
    return True
    
def print_output(output):
    for item in output:
        print('name:', item['name'], 
              'position:', item['position'], 
              'team:', item['team'],
              'price:', item['price'],
              'rating:', item['rating'])

if __name__ == '__main__':
    
    import pandas as pd

    ## load candidates   
    df_transfers = pd.read_csv('new_player_scores.csv')
    # pick useful information
    df_transfers = df_transfers[['Player', '90s', 'sub_position', 'Squad', 'market_value_in_eur', 'score', 'FK', 'SoT', 'PrgDist', 'Blocks', 'CrsPA', 'KP']]
    # rename columns
    df_transfers.columns=['name', 'games', 'position', 'team', 'price', 'rating', 'Free-kick Specialist', 'Sharp-shooter', 'Playmaker', 'Impenetrable Wall', 'Crossing Specialist', 'Assisting Machine']

    # print("Before normalization")
    # print(df_transfers.head())

    data_to_normalize = df_transfers[['Free-kick Specialist', 'Sharp-shooter', 'Playmaker', 'Impenetrable Wall', 'Crossing Specialist', 'Assisting Machine']]
    data_not_to_normalize = df_transfers[['name', 'games', 'position', 'team', 'price', 'rating']]

    data_normalized = (data_to_normalize - data_to_normalize.min()) / (data_to_normalize.max() - data_to_normalize.min())

    df_transfers_norm = pd.concat([data_not_to_normalize, data_normalized], axis=1)

    # print("After normalization")
    # print(df_transfers_norm.head())

    ## budget and requeted_position. We can change it to input file later
    # The following is just for testing now
    budget = 74000000
    # requested_positions_attributes = [['Attacking Midfield', 'Playmaker'], ['Centre-Forward', 'Sharp-shooter'], ['Attacking Midfield', 'Free-kick Specialist']]
    requested_positions_attributes = []
    # requested_positions = []
    team = 'Milan'
    # requested_positions = ['Goalkeeper'] # WORKING
    # requested_positions = ['Goalkeeper', 'Centre-Back'] # WORKING

    # initial condition
    players = []  # the players we choose under restrictions

    csp(df_transfers_norm, players, team, requested_positions_attributes, budget)

    if len(requested_positions_attributes) == 0:
        suggested_positions = team_positional_needs(df_transfers_norm, team)
        requested_positions_attributes = [[position, 'None'] for position in suggested_positions]
        players = hill_climb(df_transfers_norm, players, team, requested_positions_attributes, budget)
    
    else:
        players = hill_climb(df_transfers_norm, players, team, requested_positions_attributes, budget)

    # print_output(players)