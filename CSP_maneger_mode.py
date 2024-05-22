#!/usr/bin/env python
#coding:utf-8

import pandas as pd
import itertools


def csp(candidates, players, team, requested_positions_attributes, budget):
    """Beginning of CSP algorithm for finding a valid combination of players.

    Parameters
    ----------
    candidates : pandas.core.frame.DataFrame
        The dataset containing players from which we will choose.
    players : list
        The list in which to store our combination of players
    team : str
        The team specified by the user/manager.
    requested_positions_attributes : list
        The list of position/attribute pairs specified by the user/manager
    budget : int
        The transfer budget specified by the user/manager.

    Side effects
    ----------
    If no position/attribute pairs were specified, determines the team's weak links among their
    common players and sets the positions to search for to equal these positions. Then runs backtracking.
    """

    if len(requested_positions_attributes) == 0: 
        suggested_positions = team_positional_needs(candidates, team)
        print("No positions specified; suggesting based on following weaknesses:")
        print(suggested_positions)
        backtracking(candidates.to_dict(orient='records'), players, team, suggested_positions, budget)
    else:
        requested_positions = positions(requested_positions_attributes)
        backtracking(candidates.to_dict(orient='records'), players, team, requested_positions, budget)

def backtracking(candidates, players, team, requested_positions, budget):

    """Backtracking algorithm for finding a valid combination of players.

    Parameters
    ----------
    candidates : pandas.core.frame.DataFrame
        The dataset containing players from which we will choose.
    players : list
        The list of players currently in our set of choices.
    team : str
        The team specified by the user/manager.
    requested_positions_attributes : list
        The list of position/attribute pairs we still have yet to choose a player for. (Initially
        the full set specified by the user/manager)
    budget : int
        The transfer budget specified by the user/manager.

    Returns
    ----------
    The first found combination of players satisfying the team, budget, and position
    constraints.
    """

    # If there are no more positions to find players for, we are done"""
    if len(requested_positions) == 0:
        return True
    else:
        candidates_temp = candidates.copy()
        requested_positions_updated = requested_positions.copy()

        while(len(candidates_temp) > 0):
            # Try adding every other player to our choices
            player = candidates.pop(0) # in the candidates list, to be checked
            # If this player satisfies constraints, add them to our choices
            if Is_valid(player, team, requested_positions, budget):
                players.append(player)
                requested_positions_updated.remove(player['position'])
                candidates_temp.remove(player)
                # Next step of recursion
                if backtracking(candidates_temp, players, team, requested_positions_updated, budget - player['price']):
                    return True
                # Backtrack
                players.pop()
                requested_positions_updated.append(player['position'])
                candidates_temp.append(player)
    return False

def Is_valid(player, team, requested_positions, budget):

    """Predicate checking if given player satisfies team, position, and budget constraints.

    Parameters
    ----------
    player : (?)
        The player we are validating.
    team : str
        The team specified by the user/manager.
    requested_positions_attributes : list
        The list of position/attribute pairs we still have yet to choose a player for.
    budget : int
        The remaining unallocated portion of the transfer budget specified by the user/manager.
    
    Returns
    ----------
    Whether or not the player given is a valid addition to the selection.
    """

    # Player's price must be within budget
    if budget < player['price'] :
        return False
    
    # Player's position must be one we are looking for
    if player['position'] not in requested_positions:
        return False

    # Player must not already be on team
    if player['team'] == team:
        return False
         
    return True

def hill_climb(candidates, init_state, team, requested_positions_attributes, budget):

    """Hill-climbing algorithm for improving on the initial CSP solution.

    Parameters
    ----------
    candidates : pandas.core.frame.DataFrame
        The dataset containing players from which we will choose.
    init_state : list
        The combination of players in the current state
    team : str
        The team specified by the user/manager.
    requested_positions_attributes : list
        The list of positions/attributes specified by the user/manager.
    budget : int
        The transfer budget specified by the user/manager.

    Returns
    ----------
    The combination of players satisfying the budget, position, and attribute requirements
    with the maximal heuristic.
    """

    cur_state = init_state
    while True:
        max_attribute_assignment_value, max_attribute_assignment_permutation = max_attribute_assignment(cur_state, requested_positions_attributes)
        # print_output(cur_state, max_attribute_assignment_permutation)
        # print(heur(cur_state, requested_positions_attributes, budget))
        neighbors = generate_neighbors(candidates, cur_state, team, budget)
        best_neighbor = max(neighbors, key=lambda x: heur(x, requested_positions_attributes, budget))
        if heur(best_neighbor, requested_positions_attributes, budget) <= heur(cur_state, requested_positions_attributes, budget):
            return cur_state
        cur_state = best_neighbor

def generate_neighbors(candidates, players, team, budget):

    """Generates all neighbors for the hill-climbing algorithm.

    Parameters
    ----------
    candidates : pandas.core.frame.DataFrame
        The dataset containing players from which we will choose.
    players : list
        The combination of players in the current state
    team : str
        The team specified by the user/manager.
    budget : int
        The transfer budget specified by the user/manager.

    Returns
    ----------
    The list of all states in which a transition has been made by swapping one player
    for another who plays the same position.
    """

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

def heur(players, requested_positions_attributes, budget):

    """Heuristic for hill-climbing algorithm.

    Parameters
    ----------
    players : list
        The combination of players in the current state
    requested_positions_attributes : list
        The list of positions/attributes specified by the user/manager.
    budget : int
        The transfer budget specified by the user/manager.

    Returns
    ----------
    The heuristic for the current state, which uses the formula:

    result = rating_comp + 1.5*budget_comp + 2*attr_comp

    where

    rating_comp = the average player rating,

    budget_comp = the proportion of the transfer budget used, and

    attr_comp = the maximal sum resulting from assigning each player in players
    one attribute associated with their position and summing the min-max-normalized
    values of the corresponding player statistics.
    """

    max_attribute_assignment_value, _ = max_attribute_assignment(players, requested_positions_attributes)

    result = 0.0
    rating_comp = 0.0
    budget_comp = 0.0
    attr_comp = 0.0
    for player in players:
        rating_comp += player['rating'] / len(players)
        budget_comp += 1.5 * proportion_of_budget(player, budget)
    if len(players) != 0:
        attr_comp = 2 * max_attribute_assignment_value / len(players)

    result += rating_comp
    result += budget_comp
    result += attr_comp

    return result

def positions(requested_positions_attributes):

    """Gets just the positions from a list of position/attribute pairs.

    Parameters
    ----------
    requested_positions_attributes : list
        A list of position/attribute pairs.

    Returns
    ----------
    The list of positions only.
    """

    requested_positions = []
    for x in requested_positions_attributes:
        requested_positions.append(x[0])
    return requested_positions

def attributes_at_position(requested_positions_attributes, pos):

    """Gets just the attributes associated with some position from a
    list of position/attribute pairs.

    Parameters
    ----------
    requested_positions_attributes : list
        A list of position/attribute pairs.
    pos : str
        The position whose attributes to extract.

    Returns
    ----------
    The list of attributes associated with the given position.
    """

    requested_attributes = []
    for x in requested_positions_attributes:
        if x[0] == pos:
            requested_attributes.append(x[1])
    return requested_attributes

def max_attribute_assignment(players, requested_positions_attributes):

    """Computes the maximal sum of normalized player statistics corresponding to their
    assigned attributes over all possible assignments of attributes to players.

    Parameters
    ----------
    players : list
        The combination of players in the current state
    requested_positions_attributes : list
        The list of positions/attributes specified by the user/manager.

    Returns
    ----------
    result_value : int
        The aforementioned maximal sum.
    result_permutation: list
        The order of assigning attributes to the position-sorted list of players that
        produces this maximal sum.
    """

    requested_positions = unique_positions(players)
    result_value = 0.0
    result_permutation = []
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
            if cur_position_sum > max_position_sum:
                max_position_sum = cur_position_sum
                cur_position_permutation = permutation
        result_value += max_position_sum
        result_permutation += cur_position_permutation
    return result_value, result_permutation

def total_price(players):

    """Computes the total price of all players in a list.

    Parameters
    ----------
    players : list
        The combination of players in the current state

    Returns
    ----------
    The players' total price.
    """

    result = 0
    for player in players:
        result += player['price']
    return result

def proportion_of_budget(player, budget):

    """Computes the proportion of the budget used by a player.

    Parameters
    ----------
    player : (?)
        The player being considered.
    budget : int
        The transfer budget specified by the user/manager.

    Returns
    ----------
    The player's price divided by the transfer budget.
    """

    return player['price'] / budget

def unique_positions(players):

    """Returns the set of unique positions played by a set of players.

    Parameters
    ----------
    players : list
        The combination of players in the current state

    Returns
    ----------
    The unique positions played by the players.
    """

    result = set()
    for player in players:
        result.add(player['position'])
    return result

def players_at_position(players, pos):

    """Returns the set of players playing a given position.

    Parameters
    ----------
    players : list
        The combination of players in the current state
    pos : str
        The position to search for.

    Returns
    ----------
    The list of players playing the given position.
    """

    result = []
    for player in players:
        if player['position'] == pos:
            result.append(player)
    return result

def team_positional_needs(candidates, team):

    """Algorithm for determining the weak spots on a given team's roster (if the user/manager
    does not enter any positions.)

    Parameters
    ----------
    candidates : pandas.core.frame.DataFrame
        The dataset containing players from which we will choose.
    team : str
        The team specified by the user/manager.

    Returns
    ----------
    The list of positions (possibly including duplicates) where among the players on the given team
    who have played the equivalent of at least 10 games (approximately a fourth of a full season),
    the Z-score (with respect to all players on the team) of the player at that position is -1 or less.
    """

    df_team_roster = candidates[candidates['team'] == team]
    df_common_players = df_team_roster[df_team_roster['games'] >= 10]

    text_cols = df_common_players.select_dtypes(include='object')

    numerical_cols = df_common_players.select_dtypes(include=['float', 'int'])
    normalized_numerical_cols = (numerical_cols - numerical_cols.mean()) / numerical_cols.std()

    df_common_players_norm = pd.concat([normalized_numerical_cols, text_cols], axis=1)

    df_common_weaknesses = df_common_players_norm[df_common_players_norm['rating'] < -1]
    df_common_weaknesses = df_common_weaknesses.sort_values(by=['rating'], ascending=True)

    if len(df_common_weaknesses) == 0:
        # Find the index of the row with the lowest rating
        min_rating_index = df_common_players_norm['rating'].idxmin()

        # Get the position of the row with the lowest rating
        position_lowest_rating = df_common_players_norm.at[min_rating_index, 'position']
        # print("Lowest rating position is:", position_lowest_rating)
        return [position_lowest_rating]

    return df_common_weaknesses['position'].to_list()[:5]

# Unique Non-GK Positions:
# Attacking Midfield (M)
# Central Midfield (M)
# Centre-Back (D)
# Centre-Forward (F)
# Centre Midfield (M)
# Defensive Midfield (M)
# Left Winger (F)
# Left-Back (D)
# Left Midfield (M)
# Right Winger (F)
# Right-Back (D)
# Right Midfield (M)
# Second Striker (F)
    
def print_output(output, max_attribute_assignment_permutation):

    """Prints information about the players in the given state.

    Parameters
    ----------
    output : list
        The combination of players in the state to output
    max_attribute_assignment_permutation : list
        The order in which the position-sorted list of players is assigned attributes
        that results in the maximal sum of normalized player stats

    Returns
    ----------
    The name, position, team, price, rating, and (if applicable) attribute of each player
    in the output list.
    """

    unique_pos_list = unique_positions(players)

    i = 0

    # Print all players at a given position before moving on to the next, since the permutation
    # lists all attributes for one position, then another, and so on
    for position in unique_pos_list:
        for player in output:
            if player['position'] == position:
                if max_attribute_assignment_permutation[i] == 'None':
                    print('name:', player['name'], 
                        'position:', player['position'], 
                        'team:', player['team'],
                        'price:', player['price'],
                        'rating:', round(player['rating'], 3))
                else:
                    print('name:', player['name'], 
                        'position:', player['position'], 
                        'team:', player['team'],
                        'price:', player['price'],
                        'rating:', round(player['rating'], 3),
                        max_attribute_assignment_permutation[i], round(player[max_attribute_assignment_permutation[i]], 3))
                i += 1

if __name__ == '__main__':
    
    import pandas as pd

    ## Load candidates   
    df_transfers = pd.read_csv('new_player_scores.csv')
    # Pick useful information
    df_transfers = df_transfers[['Player', '90s', 'sub_position', 'Squad', 'market_value_in_eur', 'score', 'FK', 'SoT', 'PrgDist', 'Blocks', 'CrsPA', 'KP']]
    # Rename columns
    df_transfers.columns=['name', 'games', 'position', 'team', 'price', 'rating', 'Free-kick Specialist', 'Sharp-shooter', 'Playmaker', 'Impenetrable Wall', 'Crossing Specialist', 'Assisting Machine']

    # Normalize data (with min-max)
    data_to_normalize = df_transfers[['Free-kick Specialist', 'Sharp-shooter', 'Playmaker', 'Impenetrable Wall', 'Crossing Specialist', 'Assisting Machine']]
    data_not_to_normalize = df_transfers[['name', 'games', 'position', 'team', 'price', 'rating']]
    data_normalized = (data_to_normalize - data_to_normalize.min()) / (data_to_normalize.max() - data_to_normalize.min())
    df_transfers_norm = pd.concat([data_not_to_normalize, data_normalized], axis=1)

    ## budget and requeted_position. We can change it to input file later
    # The following is just for testing now
    budget = 100000000
    team = 'Clermont Foot'
    requested_positions_attributes = [['Right-Back', 'Playmaker']]

    # initial condition
    players = []  # the players we choose under restrictions

    csp(df_transfers_norm, players, team, requested_positions_attributes, budget)

    if len(requested_positions_attributes) == 0:
        suggested_positions = team_positional_needs(df_transfers_norm, team)
        requested_positions_attributes = [[position, 'None'] for position in suggested_positions]
        
    players = hill_climb(df_transfers_norm, players, team, requested_positions_attributes, budget)

    _, max_attribute_assignment_permutation = max_attribute_assignment(players, requested_positions_attributes)

    print_output(players, max_attribute_assignment_permutation)