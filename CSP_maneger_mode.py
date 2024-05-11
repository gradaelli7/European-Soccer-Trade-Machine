#!/usr/bin/env python
#coding:utf-8

def csp(candidates, starting_xi_data, players, team, requested_positions, budget):
    if len(requested_positions) == 0: 
        suggestions(candidates, starting_xi_data, players, team, 3)
    else:
        backtracking(candidates.to_dict(orient='records'), team_starting_xi_positions(starting_xi_data, team), players, team, requested_positions, budget)

def team_starting_xi_positions(starting_xi_data, team):
    df_team_roster = starting_xi_data[starting_xi_data['Squad'] == team]
    df_team_roster = df_team_roster.sort_values(by=['90s'], ascending=False)
    return df_team_roster['sub_position'].tolist()[:11]

def team_positional_needs(candidates, starting_xi_data, team, n):
    df_team_roster = starting_xi_data[starting_xi_data['Squad'] == team]
    df_team_roster = df_team_roster.sort_values(by=['90s'], ascending=False)
    df_starting_xi = df_team_roster[df_team_roster['90s'] >= 10]
    print(df_team_roster.head())

    pos_list = []
    starter_avgs = []
    roster_avgs = []

    for pos in set(team_starting_xi_positions(starting_xi_data, team)):
        pos_list.append(pos)

        df_starting_xi_pos = candidates[candidates['name'].isin(df_starting_xi['Player'])]
        df_starting_xi_pos = df_starting_xi_pos[df_starting_xi_pos['position'] == pos]

        df_team_roster_pos = candidates[candidates['name'].isin(df_team_roster['Player'])]
        df_team_roster_pos = df_team_roster_pos[df_team_roster_pos['position'] == pos]

        starter_avgs.append(df_starting_xi_pos['rating'].mean())
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

def suggestions(candidates, starting_xi_data, players, team, x):
    pos_list = team_positional_needs(candidates, starting_xi_data, team, 1)
    print("No positions specified.")
    print("Recommended position for {}: {}".format(team, pos_list[0]))
    candidates_pos = candidates[candidates['position'] == pos_list[0]]
    print("Top available players:")
    for i in range(x):
        players.append(candidates_pos.iloc[i])

def backtracking(candidates, starting_xi_positions, players, team, requested_positions, budget):

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
                if backtracking(candidates_temp, starting_xi_positions, players, team, requested_positions_updated, budget - player['price']):
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
        print('id:', item['id'],
              'name:', item['name'], 
              'position:', item['position'], 
              'team:', item['team'],
              'price:', item['price'],
              'rating:', item['rating'])

if __name__ == '__main__':
    
    import pandas as pd

    ## load candidates   
    df_transfers = pd.read_csv('data/csp_data.csv')
    # pick useful information
    df_transfers = df_transfers[['id', 'Player', 'sub_position', 'Squad', 'market_value_in_eur', 'target_bucket']]
    # rename columns
    df_transfers.columns=['id', 'name', 'position', 'team', 'price', 'rating']
    # Sort by player rating
    df_transfers = df_transfers.sort_values(by=['rating'], ascending=False)

    ## budget and requeted_position. We can change it to input file later
    # The following is just for testing now
    budget = 100000000
    # requested_positions = ['Centre-Back', 'Centre-Back', 'Attacking Midfield']
    requested_positions = []
    team = 'Cambuur'
    # requested_positions = ['Goalkeeper'] # WORKING
    # requested_positions = ['Goalkeeper', 'Centre-Back'] # WORKING

    df_starting_xi = pd.read_csv('data/starting_11.csv')

    # initial condition
    players = []  # the players we choose under restrictions

    csp(df_transfers, df_starting_xi, players, team, requested_positions, budget)

    # suggestions(df_transfers, df_starting_xi, players, team, 3)

    # team_positional_needs(df_transfers, df_starting_xi, team, 3)

    print_output(players)
    
    # Characteristic - attribute pairings:
    # Free-kick Specialist -> FK
    # Sharp-shooter -> SoT%
    # Playmaker -> PrgDist
