import numpy as np
from relative_power_calculation import weighted_goals, goal_stats
from data_preparation import eurocup_teams
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Initialize mega as a list of two empty lists
mega = [[], []]

# Iterate over the rows of the goal_stats DataFrame
for idx, row in goal_stats.iterrows():
    if idx in eurocup_teams:
        team = row['team']
        scored_goals = np.array(row['scored'])
        weighted_goal_avg = weighted_goals[team]

        mega[1] += (scored_goals - np.array(len(scored_goals) * [weighted_goal_avg])).tolist()
        mega[0] += row['elo_diff']

X, y = np.array(mega[0]).reshape(-1, 1), np.array(mega[1]).reshape(-1, 1)
reg = LinearRegression()
reg.fit(X, y)
print(reg.score(X, y))
print(reg.coef_, reg.intercept_)

plt.title('Elo Difference vs Goals Scored')
plt.scatter(mega[0], mega[1])
x = np.arange(-500, 1250)
y = x * reg.coef_[0][0] + reg.intercept_[0]
plt.plot(x, y, color='red')
plt.show()
