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
