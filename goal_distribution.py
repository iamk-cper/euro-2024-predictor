import matplotlib.pyplot as plt
from relative_power_calculation import df2
import numpy as np
from scipy.stats import poisson
from data_preparation import eurocup_teams
from relative_power_calculation import goal_stats

# Calculate total goals for each match
df2['total_goals'] = df2['home_score'] + df2['away_score']

mu = df2['total_goals'].mean()
k = np.arange(0, df2['total_goals'].max()+1)
poisson_pmf = poisson.pmf(k, mu)

# Plotting the histogram
plt.figure(figsize=(10, 6))
plt.hist(df2['total_goals'], bins=k, density=True, alpha=0.7, label='Actual distribution')
plt.title('Actual vs Poisson Distribution')
plt.plot(k, poisson_pmf, 'r-', alpha=0.7, label='Poisson distribution')
plt.xlabel('Total Goals')
plt.ylabel('Frequency')
plt.xticks(range(int(df2['total_goals'].max()) + 1))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.show()

figure, axis = plt.subplots(6, 4)
figure.subplots_adjust(hspace=2, wspace=2)
counter = 0
plt.title("Histogram of Goals Scored")
for i in range(6):
    for j in range(4):
        team = eurocup_teams[counter]
        stats = goal_stats.loc[team]
        axis[i, j].set_title(f"{team}")
        axis[i, j].hist(stats['scored'])
        axis[i, j].set_xlim(0, 10)
        counter += 1