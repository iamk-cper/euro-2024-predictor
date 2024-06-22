from data_preparation import df, eurocup_teams
import pandas as pd
from elo_calculation import k_value, elo_l, elo_v
import matplotlib.pyplot as plt

# Function to calculate time-based weight linearly
def calculate_weight(date, current_date, tournament, start_weight=1.0, end_weight=0, years=30):
    k = 1 - k_value(tournament) / 100
    days_diff = (current_date - date).days
    total_days = years * 365
    weight = start_weight - (start_weight - end_weight) * (days_diff / total_days) * k
    return max(weight, end_weight)


df2 = df[df['date'] >= '1994-06-13']
goal_stats = pd.DataFrame(columns=[
    'team',
    'total_weighted_goals',
    'total_weighted_matches',
    'total_weighted_goals_against',
    'scored',
    'elo_diff'
])
current_date = pd.to_datetime('today')

for idx, row in df2.iterrows():
    local = row['home_team']
    away = row['away_team']
    local_goals = row['home_score']
    away_goals = row['away_score']
    tournament = row['tournament']
    home_elo = row['Elo_h_before']
    away_elo = row['Elo_a_before']
    match_date = pd.to_datetime(row['date'])
    elo_diff = row['elo_diff']

    weight = calculate_weight(match_date, current_date, tournament)

    if local not in goal_stats.index:
        goal_stats.loc[local] = [local,
                                 local_goals * weight * away_elo / 1300,
                                 weight,
                                 away_goals * weight * home_elo / 1300,
                                 [local_goals],
                                 [elo_diff]]
    else:
        goal_stats.at[local, 'total_weighted_goals'] += local_goals * weight * away_elo / home_elo
        goal_stats.at[local, 'total_weighted_matches'] += weight
        goal_stats.at[local, 'total_weighted_goals_against'] += away_goals * weight * home_elo / away_elo
        goal_stats.at[local, 'scored'].append(local_goals)
        goal_stats.at[local, 'elo_diff'].append(elo_diff)

    if away not in goal_stats.index:
        goal_stats.loc[away] = [away,
                                away_goals * weight * home_elo / away_elo,
                                weight,
                                local_goals * weight * away_elo / home_elo,
                                [away_goals],
                                [elo_diff]]
    else:
        goal_stats.at[away, 'total_weighted_goals'] += away_goals * weight * home_elo / away_elo
        goal_stats.at[away, 'total_weighted_matches'] += weight
        goal_stats.at[away, 'total_weighted_goals_against'] += local_goals * weight * away_elo / home_elo
        goal_stats.at[away, 'scored'].append(away_goals)
        goal_stats.at[away, 'elo_diff'].append(elo_diff)

    df2.loc[idx, 'away_deffensive_power'] = goal_stats.at[away, 'total_weighted_goals_against'] / goal_stats.at[
        away, 'total_weighted_matches']
    df2.loc[idx, 'home_deffensive_power'] = goal_stats.at[local, 'total_weighted_goals_against'] / goal_stats.at[
        local, 'total_weighted_matches']
    df2.loc[idx, 'away_offensive_power'] = goal_stats.at[away, 'total_weighted_goals'] / goal_stats.at[
        away, 'total_weighted_matches']
    df2.loc[idx, 'home_offensive_power'] = goal_stats.at[local, 'total_weighted_goals'] / goal_stats.at[
        local, 'total_weighted_matches']

weighted_goals = {}
weighted_goals_against = {}

for team in eurocup_teams:
    if team in goal_stats.index:
        stats = goal_stats.loc[team]
        weighted_goals[team] = stats['total_weighted_goals'] / stats['total_weighted_matches']
        weighted_goals_against[team] = stats['total_weighted_goals_against'] / stats['total_weighted_matches']

# Create dataframes
weighted_goals_df = pd.DataFrame(list(weighted_goals.items()), columns=['Team', 'Weighted Avg Goals'])
weighted_goals_against_df = pd.DataFrame(list(weighted_goals_against.items()),
                                         columns=['Team', 'Weighted Avg Goals Against'])

# Sort dataframes
weighted_goals_df = weighted_goals_df.sort_values(by='Weighted Avg Goals', ascending=False)
weighted_goals_against_df = weighted_goals_against_df.sort_values(by='Weighted Avg Goals Against', ascending=False)

# Plotting
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 12))

# Plot weighted average goals
axes[0].barh(weighted_goals_df['Team'], weighted_goals_df['Weighted Avg Goals'], color='blue')
axes[0].set_xlabel('Weighted Avg Goals')
axes[0].set_title('Weighted Average Goals Scored per Team')
axes[0].invert_yaxis()

# Plot weighted average goals against
axes[1].barh(weighted_goals_against_df['Team'], weighted_goals_against_df['Weighted Avg Goals Against'],
             color='red')
axes[1].set_xlabel('Weighted Avg Goals Against')
axes[1].set_title('Weighted Average Goals Against per Team')
axes[1].invert_yaxis()


for team in eurocup_teams:
    if team in goal_stats.index:
        print(f"Team: {team}, Weighted Avg Goals: {weighted_goals[team]}, Weighted Avg Lost Goals: {weighted_goals_against[team]}")


plt.tight_layout()
plt.show()

df2.loc[idx, 'elo_diff'] = elo_l - elo_v