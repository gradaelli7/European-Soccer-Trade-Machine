from State import State
from queue import PriorityQueue
import itertools

#!/usr/bin/env python
#coding:utf-8

def ast(candidates, requested_positions, budget):
    init_state = State([], requested_positions, budget)
    queue = PriorityQueue()
    counter = itertools.count() # For breaking ties    
    queue.put((init_state.heuristic(), next(counter), init_state))

    frontier = set()
    frontier.add(hash(init_state))
    visited = set()

    while not queue.empty():
        heur, _, cur_state = queue.get()
        print(cur_state.player_names)
        print(cur_state.requested_positions)
        print(heur)
        frontier.remove(hash(cur_state))

        if len(cur_state.requested_positions) == 0:
            return cur_state.players

        elif hash(cur_state) not in visited:
            candidates_temp = candidates[candidates['position'].isin(cur_state.requested_positions)]
            candidates_temp = candidates_temp[candidates_temp['price'] < cur_state.budget]
            # print(candidates_temp.head())
            for i in range(candidates_temp.shape[0]):
                player = candidates_temp.iloc[i]
                if player['name'] not in cur_state.player_names:
                    requested_positions_updated = cur_state.requested_positions.copy()
                    requested_positions_updated.remove(player['position'])
                    new_state = State(cur_state.players + [player], requested_positions_updated, cur_state.budget - player['price'])
                    if hash(new_state) not in frontier and hash(new_state) not in visited:
                        queue.put((new_state.depth() + new_state.heuristic(), next(counter), new_state))
                        
                        frontier.add(hash(new_state))
            visited.add(hash(cur_state))

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
    df_transfers = df_transfers[['id', 'Player', 'sub_position', 'Squad', 'market_value_in_eur', 'target_bucket', 'FK', 'SoT%', 'PrgDist']]
    # rename columns
    df_transfers.columns=['id', 'name', 'position', 'team', 'price', 'rating', 'Free-kick Specialist', 'Sharp-shooter', 'Playmaker']

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

    # suggestions(df_transfers, df_common_players, players, team, 3)

    # team_positional_needs(df_transfers, df_common_players, team, 3)

    # print_output(players)
    print_output(ast(df_transfers, requested_positions, budget))
