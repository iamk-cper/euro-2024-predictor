import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Reading the CSV file using the absolute path and converting 'NA' to NaN
file_path = './data/results.csv'
try:
    df = pd.read_csv(file_path, sep=',', na_values='NA')
    print("File read successfully.")
except Exception as e:
    print(f"Error reading the file: {e}")

# Dropping matches without final result
df = df.dropna(subset=['home_score', 'away_score'])
# Dropping useless columns (we will not use neutral for now too, but left for future improvements)
df = df.drop(columns=['city', 'country'])
df['away_deffensive_power'] = 1
df['home_deffensive_power'] = 1
df['away_offensive_power'] = 1
df['home_offensive_power'] = 1


matches_data = [
    # Grupo A
    {"Grupo": "A", "Home_Team": "Germany", "Away_Team": "Scotland"},
    {"Grupo": "A", "Home_Team": "Hungary", "Away_Team": "Switzerland"},
    {"Grupo": "A", "Home_Team": "Germany", "Away_Team": "Hungary"},
    {"Grupo": "A", "Home_Team": "Scotland", "Away_Team": "Switzerland"},
    {"Grupo": "A", "Home_Team": "Switzerland", "Away_Team": "Germany"},
    {"Grupo": "A", "Home_Team": "Scotland", "Away_Team": "Hungary"},
    # Grupo B
    {"Grupo": "B", "Home_Team": "Spain", "Away_Team": "Croatia"},
    {"Grupo": "B", "Home_Team": "Italy", "Away_Team": "Albania"},
    {"Grupo": "B", "Home_Team": "Croatia", "Away_Team": "Albania"},
    {"Grupo": "B", "Home_Team": "Spain", "Away_Team": "Italy"},
    {"Grupo": "B", "Home_Team": "Albania", "Away_Team": "Spain"},
    {"Grupo": "B", "Home_Team": "Croatia", "Away_Team": "Italy"},
    # Grupo C
    {"Grupo": "C", "Home_Team": "Slovenia", "Away_Team": "Denmark"},
    {"Grupo": "C", "Home_Team": "Serbia", "Away_Team": "England"},
    {"Grupo": "C", "Home_Team": "Slovenia", "Away_Team": "Serbia"},
    {"Grupo": "C", "Home_Team": "Denmark", "Away_Team": "England"},
    {"Grupo": "C", "Home_Team": "England", "Away_Team": "Slovenia"},
    {"Grupo": "C", "Home_Team": "Denmark", "Away_Team": "Serbia"},
    # Grupo D
    {"Grupo": "D", "Home_Team": "Poland", "Away_Team": "Netherlands"},
    {"Grupo": "D", "Home_Team": "Austria", "Away_Team": "France"},
    {"Grupo": "D", "Home_Team": "Poland", "Away_Team": "Austria"},
    {"Grupo": "D", "Home_Team": "Netherlands", "Away_Team": "France"},
    {"Grupo": "D", "Home_Team": "Netherlands", "Away_Team": "Austria"},
    {"Grupo": "D", "Home_Team": "France", "Away_Team": "Poland"},
    # Grupo E
    {"Grupo": "E", "Home_Team": "Romania", "Away_Team": "Ukraine"},
    {"Grupo": "E", "Home_Team": "Belgium", "Away_Team": "Slovakia"},
    {"Grupo": "E", "Home_Team": "Slovakia", "Away_Team": "Ukraine"},
    {"Grupo": "E", "Home_Team": "Belgium", "Away_Team": "Romania"},
    {"Grupo": "E", "Home_Team": "Slovakia", "Away_Team": "Romania"},
    {"Grupo": "E", "Home_Team": "Ukraine", "Away_Team": "Belgium"},
    # Grupo F
    {"Grupo": "F", "Home_Team": "Turkey", "Away_Team": "Georgia"},
    {"Grupo": "F", "Home_Team": "Portugal", "Away_Team": "Czech Republic"},
    {"Grupo": "F", "Home_Team": "Georgia", "Away_Team": "Czech Republic"},
    {"Grupo": "F", "Home_Team": "Turkey", "Away_Team": "Portugal"},
    {"Grupo": "F", "Home_Team": "Georgia", "Away_Team": "Portugal"},
    {"Grupo": "F", "Home_Team": "Czech Republic", "Away_Team": "Turkey"},
]

# Create a dataframe
matches_df = pd.DataFrame(matches_data)


confederation_tournaments = ['AFC Asian Cup', 'African Cup of Nations', 'Copa América', 'CONCACAF Championship', 'Oceania Nations Cup']
confederation_clasification = ['African Cup of Nations qualification', 'FC Asian Cup qualification', 'UEFA Nations League']

eurocup_teams = [
    "Albania", "Scotland", "Hungary", "Romania",
    "Germany", "Slovakia", "England", "Czech Republic",
    "Austria", "Slovenia", "Italy", "Serbia",
    "Belgium", "Spain", "Netherlands", "Switzerland",
    "Croatia", "France", "Poland", "Turkey",
    "Denmark", "Georgia", "Portugal", "Ukraine"
]
