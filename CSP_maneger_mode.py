#!/usr/bin/env python
#coding:utf-8

import pandas as pd

def csp(candidates, players, team, requested_positions, budget, attributes):
    if len(requested_positions) == 0: 
        suggested_positions = team_positional_needs(candidates, team)
        print("No positions specified; suggesting based on following weaknesses:")
        print(suggested_positions)
    backtracking(candidates.to_dict(orient='records'), players, team, suggested_positions, budget)

def hill_climb(candidates, init_state, team, budget):
    cur_state = init_state
    while True:
        print_output(cur_state)
        print(heur(cur_state, budget))
        neighbors = generate_neighbors(candidates, cur_state, team, budget)
        best_neighbor = max(neighbors, key=lambda x: heur(x, budget))
        if heur(best_neighbor, budget) <= heur(cur_state, budget):
            return cur_state
        cur_state = best_neighbor

def heur(players, budget):
    result = 0.0
    for player in players:
        result += player['rating'] / len(players)
    result += 1.5 * proportion_of_budget(players, budget)
    return result

def total_price(players):
    result = 0
    for player in players:
        result += player['price']
    return result

def proportion_of_budget(players, budget):
    return total_price(players) / budget

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

# Change this to suggest positions for which a common player has a rating SD < -1, -1.25, or -1.5
# But always suggest lowest.
def team_positional_needs(candidates, team):
    df_team_roster = candidates[candidates['team'] == team]
    df_common_players = df_team_roster[df_team_roster['games'] >= 14]

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
    df_transfers = df_transfers[['Player', '90s', 'sub_position', 'Squad', 'market_value_in_eur', 'score', 'FK', 'SoT%', 'PrgDist']]
    # rename columns
    df_transfers.columns=['name', 'games', 'position', 'team', 'price', 'rating', 'Free-kick Specialist', 'Sharp-shooter', 'Playmaker']

    ## budget and requeted_position. We can change it to input file later
    # The following is just for testing now
    budget = 50000000
    requested_positions = []
    # requested_positions = []
    team = 'Liverpool'
    # requested_positions = ['Goalkeeper'] # WORKING
    # requested_positions = ['Goalkeeper', 'Centre-Back'] # WORKING

    # initial condition
    players = []  # the players we choose under restrictions

    csp(df_transfers, players, team, requested_positions, budget, ['Playmaker'])

    players = hill_climb(df_transfers, players, team, budget)

    print_output(players)