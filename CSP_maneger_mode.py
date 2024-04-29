#!/usr/bin/env python
#coding:utf-8
import pandas as pd





def backtracking(row, candidates, requested_positions, players, budget):
    if find_all_players(requested_positions, players):
        return True

    else:
        for i in range(row, len(candidates)):
            player = candidates[row].player
            if Is_valid(player):
                players.append(player)
                if backtracking(row + 1, candidates[1:], requested_positions[1:], players, budget - player.price):
                    return True
                
    return False

def Is_valid(player): # Done psudo code check validation
    # check position match
    #if player.position not in request_players.postion:
    #    return False

    # the constraint
    # financial constraints
    if (Not financial_contraint): # financial constraint failed
        return False
    
    # Position constraints
    if (Not Position_contraint):
        return False
    
    # Nationality constraints
    if (Not nationality_contraint): 
        return False
    
    # all other constraints
    if (Not other_contraint): 
        return False
         
    return True
    

def find_all_players(requested_positions, players): # done psudo code finish condition
    # check if find all positions
    if requested_positions == players.positions:
        return True

if __name__ == '__main__':
    

    candidates = pd.read_csv('available_players.csv') 
    candidates = candidates(['name', 'position', 'price'])
    requested_positions = pd.read_csv('requested_players.csv')
    requested_positions = requested_positions(['position'])
    

    players = []
    row = 0
    budget = input_buget

    backtracking(row, candidates, requested_positions, players)

    print(players)
    