#!/usr/bin/env python
#coding:utf-8


def backtracking(candidates, requested_positions, players, budget):

    if len(requested_positions) == 0:
        return True

    else:
        candidates_temp = candidates.copy()
        requested_positions_updated = requested_positions.copy()
        while(len(candidates_temp) > 0):
            player = candidates.pop(0) # in the candidates list, to be checked
            if Is_valid(player, requested_positions):
                players.append(player)
                requested_positions_updated.remove(player['position'])
                candidates_temp.remove(player)
                if backtracking(candidates_temp, requested_positions_updated, players, budget - player['price']):
                    return True
                players.pop()
                requested_positions_updated.append(player['position'])
                candidates_temp.append(player)
    return False

def Is_valid(player, requested_positions): # Done psudo code check validation

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
              'price:', item['price'])

if __name__ == '__main__':
    
    import pandas as pd

    ## load candidates   
    df_transfers = pd.read_csv('data/csp_data.csv')
    # pick useful information
    df_transfers = df_transfers[['id', 'Player', 'sub_position', 'market_value_in_eur']]
    # rename columns
    df_transfers.columns=['id', 'name', 'position', 'price']
    # change format from dataframe to list of dictionary
    candidates = candidates = df_transfers.to_dict(orient='records')

    ## budget and requeted_position. We can change it to input file later
    # The following is just for testing now
    budget = 100000000
    requested_positions = ['Centre-Back', 'Centre-Back', 'Attacking Midfield']
    # requested_positions = ['Goalkeeper'] # WORKING
    # requested_positions = ['Goalkeeper', 'Centre-Back'] # WORKING

    df_starting_xi = pd.read_csv('data/starting_11.csv')
    


    # initial condition
    players = []  # the players we choose under restrictions

    backtracking(candidates, requested_positions, players, budget)

    print_output(players)
    