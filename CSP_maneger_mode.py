#!/usr/bin/env python
#coding:utf-8


def backtracking(row, candidates, requested_positions, players, budget):
    # if find_all_players(requested_positions, players):
    #     return True

    if len(requested_positions) == 0:
        return True

    else:
        candidates_temp = candidates.copy()
        while(len(candidates_temp) > 0):
            # print(requested_positions)
            player = candidates.pop(0) # in the candidates list, to be checked
            if Is_valid(player, requested_positions):
                players.append(player)
                requested_positions_updated = requested_positions.copy()
                requested_positions_updated.remove(player['position'])
                if backtracking(row + 1, candidates[1:], requested_positions_updated, players, budget - player['price']):
                    return True
                # print("Popping")
                players.pop()               
    return False

def Is_valid(player, requested_positions): # Done psudo code check validation
    # check position match
    #if player.position not in request_players.postion:
    #    return False
    # print(player['name'])

    # the constraint
    # financial constraints
    if budget < player['price'] : # financial constraint failed
        # print("Budget insufficient")
        return False
    
    # Position constraints
    # if requested_positions[0] != player['position']:
    if player['position'] not in requested_positions:
        # print("Not looking for this position")
        return False
    
    # Nationality constraints # TODO
    #if (Not nationality_contraint): 
    #    return False
    
    # all other constraints # TODO
    #if (Not other_contraint): 
    #    return False
         
    # print("Player is valid")
    return True
    

def find_all_players(requested_positions, players): # done psudo code finish condition\
    # check if find all positions
    requested_positions_temp = requested_positions.copy()
    for player in players:
        if player['position'] in requested_positions_temp:
            requested_positions_temp.remove(player['position'])
        else:
            return False
    
    if len(requested_positions_temp) == 0:
        return True

    return False
    
def print_output(output):
    for item in output:
        print('id:', item['id'],
              'name:', item['name'], 
              'position:', item['position'], 
              'price:', item['price'], 
              'nationality:', item['nationality'])

if __name__ == '__main__':
    
    import pandas as pd

    ## load candidates   
    df = pd.read_csv('data/transfermarkt_data.csv')
    # pick useful information
    df = df[['player_id', 'name', 'sub_position', 'market_value_in_eur', 'country_of_birth']]
    # rename columns
    df.columns=['id', 'name', 'position', 'price', 'nationality']
    # change format from dataframe to list of dictionary
    candidates = candidates = df.to_dict(orient='records')

    ## budget and requeted_position. We can change it to input file later
    # The following is just for testing now
    budget = 100000000
    requested_positions = ['Goalkeeper', 'Centre-Back', 'Centre-Back', 'Attacking Midfield']
    # requested_positions = ['Goalkeeper'] # WORKING
    # requested_positions = ['Goalkeeper', 'Centre-Back'] # WORKING



    # initial condition
    players = []  # the players we choose under restrictions
    row = 0

    backtracking(row, candidates, requested_positions, players, budget)

    print_output(players)
    