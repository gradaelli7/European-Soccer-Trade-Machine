#!/usr/bin/env python
#coding:utf-8


def backtracking(row, candidates, requested_positions, players, budget):
    if find_all_players(requested_positions, players):
        return True

    else:
        for i in range(row, len(candidates)):
            player = candidates[row]
            if Is_valid(player):
                players.append(player)
                if backtracking(row + 1, candidates[1:], requested_positions[1:], players, budget - player['price']):
                    return True
                players.pop()               
    return False

def Is_valid(player): # Done psudo code check validation
    # check position match
    #if player.position not in request_players.postion:
    #    return False

    # the constraint
    # financial constraints
    if budget < player['price'] : # financial constraint failed
        return False
    
    # Position constraints
    if requested_positions[0] != player['position']:
        return False
    
    # Nationality constraints # TODO
    #if (Not nationality_contraint): 
    #    return False
    
    # all other constraints # TODO
    #if (Not other_contraint): 
    #    return False
         
    return True
    

def find_all_players(requested_positions, players): # done psudo code finish condition
    # check if find all positions
    if requested_positions == players.positions:
        return True
    
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
    budget = 10000000
    requested_positions = ['Goalkeeper', 'Centre-Back', 'Centre-Back', 'Attacking Midfield']


    # initial condition
    players = []
    row = 0
    

    backtracking(row, candidates, requested_positions, players)

    print_output(players)
    