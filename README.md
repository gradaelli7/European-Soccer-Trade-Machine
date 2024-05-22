# European-Soccer-Trade-Machine

## Project Description
One of the best ways to gain a competitive advantage in professional sports such as soccer is to identify undervalued players that are particularly well suited to the team’s needs. In this project, we will develop a tool for recommending strong transfers in European soccer leagues, based on factors including teams' financial resources, players' market values, positions, and performance statistics (appearances, goals, position-specific stats, etc.). We intend to utilize a machine learning model to determine the characteristics that are most likely to predict a winning trade. We then plan to implement a CSP algorithm involving constraints regarding team positional and financial needs in order to determine optimal potential transfers. This tool would be of value to general managers and front office staff for making transfer decisions based on factors such as positional needs, financial constraints, and season ambitions. 

## Data Preprocessing
Description of Data: For this project, the following data was needed:
1. FBref: Player performance data, including (expected) goals/assists, minutes played, progressive passes/carries, defensive actions, etc.
2. Transfermarkt: financial data including team/player market values, team spending / financial resource allocation
3. List of European transfers

For each of these datasets, we decided to collect data from the 2022/2023 season (i.e. player performance data from 2022/2023, transfermarket valuation from 2022/2023, transfers during Summer 2022 and Winter 2022-23 transfer windows).

In order to prepare the data ahead of the implementation of the ML model, several preprocessing steps were necessary. The following descriptions for each file explain what was done:

1. player_valuations_preprocess.ipynb - Using player, player_valuation, and competition data from "Football Data from Transfermarkt - dataset by dcereijo | data.world", we created a transfermarkt_data csv that contained the current (as of 2022/2023 season) market value of players (in euros) in the following leagues: Serie A (Italy), Bundesliga (Germany), Premier League (England), Ligue 1 (France), La Liga (Spain), Eredivisie (Netherlands), Premier Liga (Russia), Scottish Premiership (Scotland), Liga Nos (Portugal), and Jupiler Pro League (Belgium).

  Note: Along with market value, we also gathered physical data including height, weight, birthplace, and age of the players for potential future analysis.

2. gk_merger.ipynb - Goalkeeper data was scraped and collected from Fbref.com and merged with transfermarket data. Recent transfers prior to the 2022 season were also used in order to prepare dataset for ML model.

3. nongk_data_merger.ipynb - Non-goalkeeper (attackers, midfielders, defenders) data was scraped and collected from Fbref.com and merged with transfermarket data. Recent transfers prior to the 2022 season were also used in order to prepare dataset for ML model.

4. transfers_preprocess.ipynb - Transfer data from the 2022 season was collected for each of the aforementioned leagues. This data is saved under 2022_transfers.csv.

5. fbref_squads.ipynb - Squad data from the 2021-2022 and 2022-2023 seasons was scraped and collected from Fbref.com. The difference in squad statistics between the two seasons was computed in order to measure the target variable for each recently transferred player (found in 2022_transfers.csv). 

## Dataset Descriptions
Here is a brief description of the datasets found under the "data" folder:

1. 2022_transfers.csv - Collection of players from the Premier League, Serie A, Premier Liga, Liga Nos, Eredivisie, Bundesliga, Primera Division, and Ligue 1 during the 2022 Summer and Winter Transfer Windows.

2. competitions.csv - Description data on each of the aforementioned leagues.

3. final_gk_data.csv - Player data, transfermarket data, and target column created in preparation for ML model. Contains only goalkeepers and their respective statistics. Contains only goalkeepers that were traded in the 2022 Summer and Winter transfer windows.

4. final_nongk_data.csv - Player data, transfermarket data, and target column created in preparation for ML model. Contains only non-goalkeepers (attackers, midfielders, forwards) and their respective statistics. Contains only players that were traded in the 2022 Summer and Winter transfer windows. 
 
5. gk_data_2023.csv - Goalkeeper in-game statistics and transfermarket data from the 10 aforementioned leagues during the 2022/2023 season. 

6. merged_data_with_whoscored.csv

7. nongk_data_2023.csv - Non-goalkeeper in-game statistics and transfermarket data from the 10 aforementioned leagues during the 2022/2023 season. 

8. player_data_2023.csv - Player description data from the 10 aforementioned leagues during the 2022/2023 season. This csv is primarily used to help create a unique player identifier code "player_code".

9. player_valuations.csv - Player valuation data on current active professional soccer players around the world.

10. players.csv - Description data on current active professional soccer players around the world.

11. squad_comparisons.csv - Difference in squad in-game statistics between the 2022/2023 and 2021/2022 seasons. Utilized in determining the target column for recently transferred players.

12. squads_2021-2022.csv - Squad in-game statistics for the 2021/2022 season.

13. squads_2022-2023.csv - Squad in-game statistics for the 2022/2023 season.

14. transfermarkt_data.csv - Transfermarket data containing current contract and player valuations.  

15. whoscored_merged.csv

  Note: In Variable_Descriptions.pdf you can find a description for all of the columns in each corresponding csv file.

## Machine Learning Model for Scoring Players
The Python notebook used to score soccer players can be found in the GitHub repo, with the title `euro_transfer_model.ipynb`

### Data Preprocessing and target engineering:

To develop a system for recommending player transfers, we used machine learning techniques to score players. Our target variable was a combination of three factors:

- Plus-Minus: This represents the team's performance with the player on the pitch versus off the pitch.
- Squad Performance Post-Trade: Players traded to teams that performed better after the trade received a bonus.
- Minutes Played: This factor benefits players with high usage.

We used two datasets:

- Transferred Players (2022-2023): Contains the target variable.
- Eligible Players (2023): Players who have not been transferred but are eligible for the coming season.

Our data preparation steps included:

- Filling null or NA values with the column mean to prevent skewing in decision trees.
- Identifying and dropping unimportant categorical variables (e.g., player name).
- Converting important categorical variables (e.g., country of origin, footedness) to numeric values using label encoders.
- Target Calculation: We recalculated the target based on the player's position:

    - Forwards: Given a bonus if their team scored while they were on the pitch.
    - Defenders: Given a demerit if goals were scored against their team while they were on the pitch.
    - Midfielders: A combination of the two.
To normalize the target across positions, we scaled each to a number between 0 and 1 and created bins for classification.
### Exploring Models
In our project, we explored various machine learning models to determine which one provided the best performance in predicting soccer player transfers.
- We started with the Naive Bayes classifier, known for its simplicity and effectiveness in handling categorical data through its probabilistic approach. However, Naive Bayes assumes feature independence, which makes it suboptimal for our problem.
- Next, we implemented a simple Decision Tree, which offers clear interpretability by creating a model that splits data into branches based on feature values. This had impressive results, but we found we were able to improve the results with more advanced models.
- We then implemented a Random Forest model, which is a bagging algorithm wherein a subset of features are selected at random to build a forest or collection of decision trees. Bagging is “bootstrap aggregating,” an ensemble meta-algorithm combining predictions from multiple decision trees through a majority voting mechanism. It can improve accuracy and reduce overfitting. This method leverages the "wisdom of the crowd," making it more robust than a single decision tree. 
- We then tested Gradient Boosted Decision Trees (GBDT), which sequentially builds trees, with each new tree correcting errors made by the previous ones. Gradient boosting employs gradient descent algorithm to minimize errors in sequential models GBDT is powerful for capturing complex patterns but can be computationally intensive. 
- Lastly, we used Extreme Gradient Boosting (XGBoost), an advanced implementation of gradient boosting that optimizes both speed and performance. XGBoost incorporates regularization to prevent overfitting and handles missing data efficiently. Optimized Gradient Boosting algorithm through parallel processing, tree pruning, regularization 

Through this comparison, we identified the model for our soccer transfer predictions.

## Constraint Satisfaction Problem (CSP) / Local Search Algorithm for Choosing Players

The code for this algorithm is in the file `CSP_maneger_mode.py`.

The dataset used in our algorithm for choosing players consisted of the following columns:
- Player names
- Player stats (from FBref)
- Player market values (from Transfermarkt)
- Player rating = sum of predicted bin number and predicted continuous target variable

Our goal with this algorithm is to output a combination of players satisfying the following constraints input by the user/manager, for which the average rating of the players (as determined by the ML model) is maximal:
- User/manager’s team (we don’t want to suggest players already on this team),
- Total transfer budget (the sum of all suggested players’ prices must be below it),
- Up to 5 positions, selected from the following: Defensive Midfield, Centre-Forward, Centre-Back, Right-Back, Left-Back, Attacking Midfield, Right Winger, Right Midfield, Second Striker, Central Midfield, Left Winger.
    - The same position may be repeated multiple times if the user wants multiple players who play that position.
    - The user can also optionally assign attributes to each position, which are associated with certain player statistics. The ones we have included for selection are:
        - Free-Kick Specialist: associated with FK = free-kick goals
        - Sharp-shooter: associated with SoT = shots on target
        - Playmaker: associated with PrgDist = total distance of forward passes
        - Impenetrable Wall: associated with Blocks (of shots and passes)
        - Crossing Specialist: associated with CrsPA = completed crosses into the penalty area
        - Assisting Machine: associated with KP = Key Passes = passes leading directly to a shot
We initially viewed the above as a constraint satisfaction problem (CSP) due to the existence of criteria that a solution must meet. Our initial implementation of the algorithm—at which point we only cared about maximizing average player rating—used the standard CSP backtracking algorithm. When we sorted the data in descending order of player rating, this algorithm gave us a near-optimal solution, always choosing the top-rated players in each position as long as the budget was not too low.

While the initial approach above gives us highly-rated players, it was lacking in several ways:
- The players chosen often did not cover a significant portion of the transfer budget entered. In practice, a manager would enter a larger budget because they are looking for more expensive players.
- The attributes chosen for each position did not influence the results. In practice, a manager would provide an attribute because they are looking for a player who specializes in a certain area of play.

Using the above CSP alone would not be sufficient to find an optimal solution incorporating budget and player attributes, since sorting by rating and then these criteria would be impossible due to the continuity of ratings. Therefore, we added a hill climbing algorithm to which is passed the initial solution found by backtracking, and that makes transitions by swapping one of the players currently in the selection with another player who plays the same position. The algorithm takes as input a version of the original dataset with all player stats normalized using min-max, thus making their ranges all identical (0 to 1). The heuristic includes three weighted components:
- The average player rating. Approximate range = (1.75, 5)
- The proportion of the specified transfer budget used. Range = (0, 1), weight = 1.5
- The maximal average of normalized attributes over all possible assignments of attributes to players only in the positions to which the attributes are associated. Range = (0, 1), weight = 2
    - For example, if the user/manager asked for two players, A and B, assigning them attributes X and Y, respectively...
        - If they assigned A and B different positions, this component would be computed as A['X']+B['Y'].
        - If, however, they assigned A and B the same position, this component would be computed as max(A['X']+B['Y'], A['Y']+B['X']).

In addition, we also allow the user the option of not specifying any positions, in which case they will be suggested players based on the weak links present among their selected team’s common players. To do this, we take the Z-scores of player ratings with respect to all players on the chosen team, restrict the data to include only those players who have played the equivalent of at least 10 games, and then determine the positions of the players whose Z-scores are -1 or less, up to a maximum of five positions (since that is the maximum number of players we allow the user to request). Based on the given team and budget, we then make suggestions for these positions (with the attributes being “None” for them all).
