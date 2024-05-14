#!/usr/bin/env python
#coding:utf-8

def csp(candidates, common_players_data, players, team, requested_positions, budget, attributes):
    if len(requested_positions) == 0: 
        suggestions(candidates, common_players_data, players, team, 3)
    else:
        # print("Before sorting")
        # print(candidates.head())
        # candidates = candidates.sort_values(by=['rating']+attributes, ascending=False)
        # print("After sorting")
        # print(candidates.head())
        backtracking(candidates.to_dict(orient='records'), team_common_players_positions(common_players_data, team), players, team, requested_positions, budget)

def hill_climb(candidates, init_state, team, budget):
    cur_state = init_state
    while True:
        print(heur(cur_state))
        neighbors = generate_neighbors(candidates, cur_state, team, budget)
        best_neighbor = max(neighbors, key=heur)
        if heur(best_neighbor) <= heur(cur_state):
            return cur_state
        cur_state = best_neighbor

def heur(players):
    result = 0.0
    for player in players:
        result += player['rating'] / len(players)
    # result -= total_price(players) / 50000000
    return result

def total_price(players):
    result = 0
    for player in players:
        result += player['price']
    return result

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

def team_positional_needs(candidates, common_players_data, team, n):
    df_team_roster = common_players_data[common_players_data['Squad'] == team]
    df_team_roster = df_team_roster.sort_values(by=['90s'], ascending=False)
    df_common_players = df_team_roster[df_team_roster['90s'] >= 10]
    print(df_team_roster.head())

    pos_list = []
    starter_avgs = []
    roster_avgs = []

    for pos in set(team_common_players_positions(common_players_data, team)):
        pos_list.append(pos)

        df_common_players_pos = candidates[candidates['name'].isin(df_common_players['Player'])]
        df_common_players_pos = df_common_players_pos[df_common_players_pos['position'] == pos]

        df_team_roster_pos = candidates[candidates['name'].isin(df_team_roster['Player'])]
        df_team_roster_pos = df_team_roster_pos[df_team_roster_pos['position'] == pos]

        starter_avgs.append(df_common_players_pos['rating'].mean())
        roster_avgs.append(df_team_roster_pos['rating'].mean())

    # print(pos_list)
    # print(starter_avgs)
    # print(roster_avgs)

    pos_comparison_dict = {'Position': pos_list, 'Avg starter rating': starter_avgs, 'Avg roster rating': roster_avgs}

    # Creating a DataFrame from the dictionary
    pos_comparison = pd.DataFrame(pos_comparison_dict).sort_values(by=['Avg starter rating', 'Avg roster rating'], ascending=True)
    
    print(pos_comparison)

    return pos_comparison['Position'].to_list()[:n]

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

def suggestions(candidates, common_players_data, players, team, x):
    pos_list = team_positional_needs(candidates, common_players_data, team, 1)
    print("No positions specified.")
    print("Recommended position for {}: {}".format(team, pos_list[0]))
    candidates_pos = candidates[candidates['position'] == pos_list[0]]
    print("Top available players:")
    for i in range(x):
        players.append(candidates_pos.iloc[i])

def backtracking(candidates, common_players_positions, players, team, requested_positions, budget):

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
                if backtracking(candidates_temp, common_players_positions, players, team, requested_positions_updated, budget - player['price']):
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
    
    # all other constraints # TODO
    #if (Not other_contraint): 
    #    return False
         
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
    df_transfers = df_transfers[['Player', 'sub_position', 'Squad', 'market_value_in_eur', 'score', 'FK', 'SoT%', 'PrgDist']]
    # rename columns
    df_transfers.columns=['name', 'position', 'team', 'price', 'rating', 'Free-kick Specialist', 'Sharp-shooter', 'Playmaker']

    ## budget and requeted_position. We can change it to input file later
    # The following is just for testing now
    budget = 100000000
    requested_positions = ['Centre-Back', 'Centre-Back', 'Attacking Midfield']
    # requested_positions = []
    team = 'Cambuur'
    # requested_positions = ['Goalkeeper'] # WORKING
    # requested_positions = ['Goalkeeper', 'Centre-Back'] # WORKING

    df_common_players = pd.read_csv('data/starting_11.csv')

    # initial condition
    players = []  # the players we choose under restrictions

    csp(df_transfers, df_common_players, players, team, requested_positions, budget, ['Playmaker'])

    players = hill_climb(df_transfers, players, team, budget)

    # suggestions(df_transfers, df_common_players, players, team, 3)

    # team_positional_needs(df_transfers, df_common_players, team, 3)

    print_output(players)
