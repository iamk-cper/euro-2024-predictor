import numpy as np
import pandas as pd
from data_preparation import df, confederation_clasification, confederation_tournaments, eurocup_teams
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def actual_result(loc, aw):
    if loc < aw:
        wa = 1
        wl = 0
    elif loc > aw:
        wa = 0
        wl = 1
    elif loc == aw:
        wa = 0.5
        wl = 0.5
    return [wl, wa]

def expected_result(loc, aw):
    dr = loc - aw
    we = (1 / (10**(-dr / 400) + 1))
    return [np.round(we, 3), 1 - np.round(we, 3)]

def calculate_elo(elo_l, elo_v, local_goals, away_goals, tournament):
    k = k_value(tournament)
    wl, wv = actual_result(local_goals, away_goals)
    wel, wev = expected_result(elo_l, elo_v)

    elo_ln = elo_l + k * (wl - wel)
    elo_vn = elo_v + k * (wv - wev)

    return elo_ln, elo_vn, wel, wev


def k_value(tournament):
    k = 5
    if tournament == 'Friendly':
        k = 10
    elif tournament in confederation_clasification:
        k = 20
    elif tournament == 'UEFA Euro qualification' or tournament == 'FIFA World Cup qualification':
        k = 25
    elif tournament == tournament in confederation_tournaments:
        k = 40
    elif tournament == 'UEFA Euro' or tournament == 'FIFA World Cup':
        k = 50
    return k


current_elo = {}

for idx, row in df.iterrows():
    local = row['home_team']
    away = row['away_team']
    local_goals = row['home_score']
    away_goals = row['away_score']
    tournament = row['tournament']
    match_date = pd.to_datetime(row['date'])

    if local not in current_elo.keys():
        current_elo[local] = 1300

    if away not in current_elo.keys():
        current_elo[away] = 1300

    elo_l = current_elo[local]
    elo_v = current_elo[away]

    elo_ln, elo_vn, wel, wev = calculate_elo(elo_l, elo_v, local_goals, away_goals, tournament)

    current_elo[local] = elo_ln
    current_elo[away] = elo_vn

    df.loc[idx, 'Elo_h_after'] = elo_ln
    df.loc[idx, 'Elo_a_after'] = elo_vn
    df.loc[idx, 'elo_diff'] = elo_l - elo_v
    df.loc[idx, 'Elo_h_before'] = elo_l
    df.loc[idx, 'Elo_a_before'] = elo_v
    df.loc[idx, 'probH'] = wel
    df.loc[idx, 'probA'] = wev

elos = pd.concat([df[['date', 'home_team', 'Elo_h_after']].rename(columns={'home_team': 'Team', 'Elo_h_after': 'Elo'}),
                  df[['date', 'away_team', 'Elo_a_after']].rename(columns={'away_team': 'Team', 'Elo_a_after': 'Elo'})])
elos.sort_values(by='date', ascending=False, inplace=True)
elos.drop_duplicates('Team', inplace=True)
elos.sort_values(by='Elo', ascending=False, inplace=True)
elos.reset_index(drop=True, inplace=True)
elos['position'] = elos.index + 1


def plot_top_elo(elos, n=10):
    """
    Plots the top n teams by Elo rating in a horizontal bar chart.

    Parameters:
    elos (pd.DataFrame): DataFrame containing 'Team' and 'Elo' columns.
    n (int): Number of top teams to display.
    """
    # Sort elos DataFrame by Elo rating in descending order
    elos.sort_values(by='Elo', ascending=False, inplace=True)

    # Select only the top n teams
    top_teams = elos.head(n)

    # Create a color map
    cmap = plt.get_cmap('viridis')
    norm = mcolors.Normalize(vmin=min(top_teams['Elo']), vmax=max(top_teams['Elo']))
    colors = cmap(norm(top_teams['Elo']))

    # Plotting
    plt.figure(figsize=(12, 8))
    bars = plt.barh(top_teams['Team'], top_teams['Elo'], color=colors)

    # Add text annotations
    for bar in bars:
        plt.text(
            bar.get_width() + 5,
            bar.get_y() + bar.get_height() / 2,
            f'{bar.get_width():.0f}',
            ha='left',
            va='center',
            fontsize=10
        )

    # Highlighting the top team
    bars[0].set_edgecolor('black')
    bars[0].set_linewidth(2)

    # Customizing the plot
    plt.xlabel('Elo Rating')
    plt.title('Top Teams by Elo Rating')
    plt.gca().invert_yaxis()  # Invert y-axis to display the highest Elo at the top
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # Show plot
    plt.tight_layout()
    plt.show()


elos_ranking_euro = elos[elos.Team.isin(eurocup_teams)].copy()
print(plot_top_elo(elos_ranking_euro, 24))