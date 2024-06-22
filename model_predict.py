import numpy as np
from relative_power_calculation import weighted_goals, weighted_goals_against
import matplotlib.pyplot as plt
import seaborn as sns
from elo_calculation import elos_ranking_euro
from goals_elo_correlation import reg
from scipy.stats import poisson
from model_train import predict_match
import pandas as pd
from data_preparation import matches_df

# Function to predict the exact score based on team names
def predict_match_xG(home_team, away_team):
    home_elo = get_elo_value(home_team)
    away_elo = get_elo_value(away_team)
    elo_diff = home_elo - away_elo
    home_off_power = weighted_goals.get(home_team, 1.0)  # Default value if team not found
    away_off_power = weighted_goals.get(away_team, 1.0)
    home_def_power = weighted_goals_against.get(home_team, 1.0)
    away_def_power = weighted_goals_against.get(away_team, 1.0)

    home_pred, away_pred = predict_match(home_off_power, away_off_power, home_def_power, away_def_power)

    home_pred = home_pred + reg.predict(np.array([elo_diff]).reshape(-1, 1))
    away_pred = away_pred - reg.predict(np.array([elo_diff]).reshape(-1, 1))
    return home_pred[0][0], away_pred[0][0]

def get_elo_value(team_name):
    # Check if the team exists in the DataFrame
    if team_name in elos_ranking_euro['Team'].values:
        # Retrieve the Elo value for the given team
        elo_value = elos_ranking_euro.loc[elos_ranking_euro['Team'] == team_name, 'Elo'].values[0]
        return elo_value

# Example usage
home_team = 'Spain'
away_team = 'Georgia'

home_pred, away_pred = predict_match_xG(home_team, away_team)

print(f'Predicted score for {home_team} vs {away_team}: {home_pred} - {away_pred}')


# Function to sample scores from Poisson distribution
def sample_poiss(l, n):
    max_goals = 100
    p = [poisson.pmf(x, l) for x in range(max_goals)]
    return np.random.choice(range(max_goals), n, p=p)

# Function to generate heatmap using sampled scores with exact counts
def generate_heatmap_sampling(home_team, away_team, xG_home, xG_away, n_samples=10000):
    max_goals = 6
    home_goals_samples = sample_poiss(xG_home, n_samples)
    away_goals_samples = sample_poiss(xG_away, n_samples)

    joint_prob_matrix = np.zeros((max_goals + 1, max_goals + 1))

    for hg, ag in zip(home_goals_samples, away_goals_samples):
        if hg <= max_goals and ag <= max_goals:
            joint_prob_matrix[hg, ag] += 1

    plt.figure(figsize=(10, 8))
    sns.heatmap(joint_prob_matrix, annot=True, cmap="Blues", fmt=".0f",
                xticklabels=range(max_goals + 1), yticklabels=range(max_goals + 1))
    plt.xlabel(f'Goals by {away_team}')
    plt.ylabel(f'Goals by {home_team}')
    plt.title(f'Heatmap of Predicted Scores (Sampling) for {home_team} vs {away_team}')
    plt.show()


xG_home, xG_away = predict_match_xG('Spain', 'Georgia')
print(xG_home, xG_away)
generate_heatmap_sampling('Spain', 'Georgia', xG_home, xG_away)


def predict_score(home_team, away_team):
    xG_home, xG_away = predict_match_xG(home_team, away_team)
    home_goals = np.round(sample_poiss(xG_home, 1))
    away_goals = np.round(sample_poiss(xG_away, 1))
    return home_goals[0], away_goals[0]


# Simulate group stage function
def simulate_group_stage_with_tracking(matches_df):
    groups = matches_df['Grupo'].unique()
    results = {group: {} for group in groups}

    for group in groups:
        group_matches = matches_df[matches_df['Grupo'] == group]

        for _, match in group_matches.iterrows():
            home_team = match['Home_Team']
            away_team = match['Away_Team']
            home_goals, away_goals = predict_score(home_team, away_team)

            if home_team not in results[group]:
                results[group][home_team] = {'points': 0, 'goals_for': 0, 'goals_against': 0}
            if away_team not in results[group]:
                results[group][away_team] = {'points': 0, 'goals_for': 0, 'goals_against': 0}

            results[group][home_team]['goals_for'] += home_goals
            results[group][home_team]['goals_against'] += away_goals
            results[group][away_team]['goals_for'] += away_goals
            results[group][away_team]['goals_against'] += home_goals

            if home_goals > away_goals:
                results[group][home_team]['points'] += 3
            elif home_goals < away_goals:
                results[group][away_team]['points'] += 3
            else:
                results[group][home_team]['points'] += 1
                results[group][away_team]['points'] += 1

    return results


# Initialize data structures to hold placement counts
placement_counts = {group: {} for group in matches_df['Grupo'].unique()}

# Simulate 10 iterations and collect data
iterations = 10
all_results = []

for i in range(iterations):
    result = simulate_group_stage_with_tracking(matches_df)
    all_results.append(result)

    for group, teams in result.items():
        group_standing = []
        for team, stats in teams.items():
            group_standing.append({
                'Team': team,
                'Points': stats['points'],
                'Goals_For': stats['goals_for'],
                'Goals_Against': stats['goals_against'],
                'Goal_Difference': stats['goals_for'] - stats['goals_against']
            })
        group_standing = sorted(group_standing, key=lambda x: (x['Points'], x['Goal_Difference']), reverse=True)

        for position, team_data in enumerate(group_standing):
            team = team_data['Team']
            if team not in placement_counts[group]:
                placement_counts[group][team] = [0, 0, 0, 0]
            placement_counts[group][team][position] += 1

# Convert counts to percentages
placement_percentages = {group: {} for group in placement_counts.keys()}

for group, teams in placement_counts.items():
    for team, counts in teams.items():
        total_simulations = sum(counts)
        placement_percentages[group][team] = [count / total_simulations * 100 for count in counts]

# Display results of all iterations and final placement percentages
final_standings = []

for iteration, result in enumerate(all_results):
    iteration_standings = []
    for group, teams in result.items():
        group_standing = []
        for team, stats in teams.items():
            group_standing.append({
                'Team': team,
                'Points': stats['points'],
                'Goals_For': stats['goals_for'],
                'Goals_Against': stats['goals_against'],
                'Goal_Difference': stats['goals_for'] - stats['goals_against']
            })
        group_standing = sorted(group_standing, key=lambda x: (x['Points'], x['Goal_Difference']), reverse=True)
        iteration_standings.append(pd.DataFrame(group_standing))
    final_standings.append(iteration_standings)

# Print results of all iterations
for i, standings in enumerate(final_standings):
    for j, group_standing in enumerate(standings):
        group_name = f"Group {matches_df['Grupo'].unique()[j]} Standings after Iteration {i + 1}"
        # print(group_name)
        # print(group_standing)
        # print("\n")

# Prepare placement percentages for display
placement_percentages_df = []

for group, teams in placement_percentages.items():
    for team, percentages in teams.items():
        placement_percentages_df.append({
            'Group': group,
            'Team': team,
            '1st Place %': percentages[0],
            '2nd Place %': percentages[1],
            '3rd Place %': percentages[2],
            '4th Place %': percentages[3]
        })

placement_percentages_df = pd.DataFrame(placement_percentages_df)

# Display separate tables for each group, sorted by percentages
groups = placement_percentages_df['Group'].unique()

for group in groups:
    group_df = placement_percentages_df[placement_percentages_df['Group'] == group]
    group_df = group_df.sort_values(by=['1st Place %', '2nd Place %', '3rd Place %'], ascending=False).reset_index(
        drop=True)
    print(f"Placement Percentages for Group {group}")
    print(group_df)
    print("\n")