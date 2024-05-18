import streamlit as st
import pandas as pd
from CSP_maneger_mode import *
import locale


# Initialize session state
if 'player_count' not in st.session_state:
    st.session_state.player_count = 0

# Initialize lists to store player selections
if 'player_positions' not in st.session_state:
    st.session_state.player_positions = {}
if 'player_traits' not in st.session_state:
    st.session_state.player_traits = {}

def main():

    # Load CSV files and other required data
    df_transfers = pd.read_csv('new_player_scores.csv')
    df_common_players = pd.read_csv('data/starting_11.csv')

    # pick useful information
    df_transfers = df_transfers[['Player', '90s', 'sub_position', 'Squad', 'market_value_in_eur', 'score', 'FK', 'SoT', 'PrgDist', 'Blocks', 'CrsPA', 'KP']]
    # rename columns
    df_transfers.columns=['name', 'games', 'position', 'team', 'price', 'rating', 'Free-kick Specialist', 'Sharp-shooter', 'Playmaker', 'Impenetrable Wall', 'Crossing Specialist', 'Assisting Machine']

    # Set wide mode for the entire page
    st.set_page_config(layout="wide")

    # Divide layout into two columns
    colF, colS, colT= st.columns([1, 3, 1])
    with colS:
        # Set title of the app
        st.title("European Soccer Transfer Machine")


    # Divide layout into two columns
    colA, colB,colC= st.columns([1, 11, 1])

    with colB:
        # Add introduction section
        st.write("Welcome to the European Soccer Transfer Machine! Your go-to resource for making informed transfer decisions in the highly competitive world of professional soccer. Our platform offers a comprehensive toolset designed to assist general managers and front office staff in navigating the complexities of player trades across various European leagues.")

        st.subheader("Here's what you need to do:")
        st.markdown("- **Select Your Team:** Begin by choosing your team of interest from a wide array of European leagues, including the Premier League, Serie A, La Liga, and more. First, pick the league in which your desired team competes, then select the team itself.")
        st.markdown("- **Set Your Budget:** Determine your team's financial resources by entering a transfer budget in Euros. This budget will serve as the foundation for your transfer decisions, ensuring that you stay within your financial constraints while pursuing strategic player acquisitions.")
        st.markdown("- **Specify Player Positions and Traits (Optional):** Tailor your search further by specifying player positions and traits that align with your team's needs and strategic objectives. You can input up to five position-player trait pairings to refine your transfer targets. \n\n"
                    "IMPORTANT: If you do not specify player positions or leave the Position dropdown as 'Select Position', you will be provided with transfer recommendations based on current position weaknesses determined by our algorithm.")
        st.markdown("- **Enter and Evaluate:** Once you've provided all necessary information, click the 'Enter' button to proceed. Our platform will process your inputs and generate recommendations based on factors such as positional needs, financial constraints, and season ambitions.")

        st.write("By leveraging our tool's advanced capabilities, including machine learning algorithms and constraint satisfaction programming (CSP) techniques, you'll gain valuable insights into potential transfers that can enhance your team's competitiveness and success on the field.")

    # Divide layout into two columns
    col1, col2, col3, col4= st.columns([1,3, 3,1])

    # Select Your Team subsection
    with col2:
        # Select Your Team subsection
        st.header("Select Your Team")

        # Select League dropdown
        selected_league = st.selectbox("Select League", ["Select a League", "Premier League", 
                                                        "Serie A", "La Liga", "Ligue 1", 
                                                        "Bundesliga", "Eredivisie", "Liga Nos", 
                                                        "Jupiler Pro League", "Premier Liga", 
                                                        "Scottish Premiership"])

        if selected_league != "Select a League":
            # Dictionary of teams for each league
            teams = {
                "Premier League": ['Arsenal', 'Aston Villa', 'Bournemouth', 'Brighton', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham', 'Leeds United', 'Leicester City', 'Liverpool', 'Manchester City', 'Manchester Utd', 'Newcastle Utd', "Nott'ham Forest", 'Southampton', 'Tottenham', 'West Ham', 'Wolves'],
                "Serie A": ['Atalanta', 'Bologna', 'Cremonese', 'Empoli', 'Fiorentina', 'Hellas Verona', 'Inter', 'Juventus', 'Lazio', 'Lecce', 'Milan', 'Monza', 'Napoli', 'Roma', 'Salernitana', 'Sampdoria', 'Sassuolo', 'Spezia', 'Torino', 'Udinese'],
                "La Liga": ['Almería', 'Athletic Club', 'Atlético Madrid', 'Barcelona', 'Betis', 'Cádiz', 'Celta Vigo', 'Espanyol', 'Getafe', 'Girona', 'Mallorca', 'Osasuna', 'Rayo Vallecano', 'Real Madrid', 'Real Sociedad', 'Sevilla', 'Valencia', 'Valladolid', 'Villarreal', 'Elche'],
                "Ligue 1": ['Ajaccio', 'Angers', 'Auxerre', 'Brest', 'Clermont Foot', 'Lens', 'Lille', 'Lorient', 'Lyon', 'Marseille', 'Metz', 'Monaco', 'Montpellier', 'Nantes', 'Nice', 'Paris S-G', 'Rennes', 'Reims', 'Strasbourg', 'Troyes'],
                "Bundesliga": ['Augsburg', 'Bayern Munich', 'Bochum', 'Dortmund', 'Eintracht Frankfurt', 'Freiburg', 'Hertha BSC', 'Hoffenheim', 'Köln', 'Mainz 05', 'RB Leipzig', "M'Gladbach", 'Schalke 04', 'Stuttgart', 'Union Berlin', 'Wolfsburg', 'Werder Bremen'],
                "Eredivisie": ['Ajax', 'AZ Alkmaar', 'Cambuur', 'Emmen', 'Excelsior', 'Feyenoord', 'Fortuna Sittard', 'Go Ahead Eagles', 'Groningen', 'Heerenveen', 'NEC Nijmegen', 'PSV Eindhoven', 'RKC Waalwijk', 'Sparta Rotterdam', 'Utrecht', 'Vitesse', 'Volendam', 'Willem II', 'Zwolle'],
                "Liga Nos": ['Arouca', 'Belenenses', 'Benfica', 'Boavista', 'Braga', 'Estoril', 'Famalicão', 'Gil Vicente', 'Marítimo', 'Moreirense', 'Paços de Ferreira', 'Portimonense', 'Porto', 'Rio Ave', 'Santa Clara', 'Sporting CP', 'Tondela', 'Vizela', 'Vitória Guimarães', 'Vitória SC'],
                "Jupiler Pro League": ['Anderlecht', 'Antwerp', 'Beerschot VA', 'Cercle Brugge', 'Charleroi', 'Club Brugge', 'Eupen', 'Genk', 'Gent', 'Kortrijk', 'Mechelen', 'Oostende', 'RSC Anderlecht', 'Sint-Truiden', 'Sporting Charleroi', 'Standard Liège', 'STVV', 'Waasland-Beveren', 'Zulte Waregem'],
                "Premier Liga": ['Akhmat Grozny', 'Arsenal Tula', 'CSKA Moscow', 'Dinamo Moscow', 'Dynamo Moscow', 'FC Krasnodar', 'Khimki', 'Lokomotiv Moscow', 'Rubin Kazan', 'Rostov', 'SKA-Khabarovsk', 'Spartak Moscow', 'Ufa', 'Ural', 'Veles Moscow', 'Zenit St. Petersburg'],
                "Scottish Premiership": ['Aberdeen', 'Celtic', 'Dundee', 'Dundee Utd', 'Hamilton', 'Hearts', 'Hibernian', 'Livingston', 'Motherwell', 'Partick', 'Rangers', 'Ross County', 'St Johnstone', 'St Mirren']
            }

            # Select team dropdown based on selected league
            selected_team = st.selectbox(f"Select Team for {selected_league}", ["Select a Team"] + sorted(teams[selected_league]))

            # Budget textbox
            transfer_budget = st.number_input("Transfer Budget (in Euros):", min_value=0, step=1)

            # Format the transfer budget with commas and euro symbol
            formatted_budget = f"€{transfer_budget:,}"

            # Display the formatted transfer budget
            st.write(f"Budget: {formatted_budget}")

           # Player positions
            positions = [
                'Select Position','Defensive Midfield', 'Centre-Forward', 'Centre-Back', 'Right-Back', 'Left-Back',
                'Attacking Midfield', 'Right Winger', 'Right Midfield', 'Second Striker',
                'Central Midfield', 'Left Winger', 'Left Midfield'
            ]
            traits = {
                'Select Position': ['None'],
                'Defensive Midfield': ['None', 'Playmaker', 'Impenetrable Wall'],
                'Centre-Forward': ['None','Free-kick Specialist', 'Sharp-shooter'],
                'Centre-Back': ['None', 'Impenetrable Wall'],
                'Right-Back': ['None','Free-kick Specialist', 'Crossing Specialist', 'Assisting Machine'],
                'Left-Back': ['None','Free-kick Specialist', 'Crossing Specialist', 'Assisting Machine'],
                'Attacking Midfield': ['None','Free-kick Specialist', 'Playmaker', 'Assisting Machine'],
                'Right Winger': ['None','Free-kick Specialist', 'Crossing Specialist', 'Assisting Machine'],
                'Right Midfield': ['None','Free-kick Specialist', 'Crossing Specialist', 'Assisting Machine'],
                'Second Striker': ['None','Free-kick Specialist', 'Sharp-shooter'],
                'Central Midfield': ['None','Free-kick Specialist', 'Playmaker', 'Assisting Machine'],
                'Left Winger': ['None','Free-kick Specialist', 'Crossing Specialist', 'Assisting Machine'],
                'Left Midfield': ['None','Free-kick Specialist', 'Crossing Specialist', 'Assisting Machine']
                }
 
            if selected_team != 'Select A Team' and transfer_budget > 0:

                st.header("Player Positions")

                # Layout with columns
                colAdd, colRem = st.columns([2, 1])

                # Add Player Button
                with colAdd:
                    if st.session_state.player_count < 5:
                        if st.button("+ Add Player"):
                            st.session_state.player_count += 1

                # Remove Player Button
                with colRem:
                    if st.session_state.player_count > 0:
                        if st.button("- Remove Player"):
                            if st.session_state.player_count > 0:
                                st.session_state.player_positions.pop(st.session_state.player_count, None)
                                st.session_state.player_traits.pop(st.session_state.player_count, None)
                                st.session_state.player_count -= 1

                # Display player selection boxes
                for i in range(st.session_state.player_count):
                    player_position = st.selectbox(f"Player {i+1} Position:", positions, key=f"position_{i+1}")
                    player_trait = st.selectbox(f"Player {i+1} Trait:", traits[player_position], key=f"trait_{i+1}")
                    if player_position and player_trait and player_position != 'Select Position': 
                        st.session_state.player_positions[i+1] = player_position
                        st.session_state.player_traits[i+1] = player_trait

                if st.button("Find Transfer Suggestions"):

                    requested_positions = list(st.session_state.player_positions.values())
                    print(requested_positions)
                    requested_traits = list(st.session_state.player_traits.values())
                    
                    # Combine the two lists into a list of lists
                    pos_att = [[pos, trait] for pos, trait in zip(requested_positions, requested_traits)]

                    
                    data_to_normalize = df_transfers[['Free-kick Specialist', 'Sharp-shooter', 'Playmaker', 'Impenetrable Wall', 'Crossing Specialist', 'Assisting Machine']]
                    data_not_to_normalize = df_transfers[['name', 'games', 'position', 'team', 'price', 'rating']]
                    data_normalized = (data_to_normalize - data_to_normalize.min()) / (data_to_normalize.max() - data_to_normalize.min())
                    df_transfers_norm = pd.concat([data_not_to_normalize, data_normalized], axis=1)

                    players = []
                    try:
                        csp(df_transfers_norm, players, selected_team, pos_att, transfer_budget)

                        if len(pos_att) == 0:
                            suggested_positions = team_positional_needs(df_transfers_norm, selected_team)
                            pos_att = [[position, 'None'] for position in suggested_positions]
                            players = hill_climb(df_transfers_norm, players, selected_team, pos_att, transfer_budget)
                    
                        else:
                            players = hill_climb(df_transfers_norm, players, selected_team, pos_att, transfer_budget)

                        with col3:
                            st.header("Transfer Recommendations")
                            # Placeholder for output
                            for item in players:
                                st.write('name:', item['name'], 
                                    'position:', item['position'], 
                                    'team:', item['team'],
                                    'price:', item['price'],
                                    'rating:', item['rating'])
                    except (IndexError, ValueError):
                        with col3:
                            st.header("Transfer Recommendations")
                            st.write("Your transfer budget is too low! Modify your player requests or increase your budget.")
                    
                    

if __name__ == "__main__":
    main()