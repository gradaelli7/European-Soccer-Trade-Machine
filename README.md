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

2. data_merger.ipynb - 

3. transfers_preprocess.ipynb - 
