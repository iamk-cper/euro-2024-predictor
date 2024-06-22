from model_train import predict_match, test_df
import numpy as np
from scipy.stats import poisson
from goals_elo_correlation import reg

# Function to check accuracy of predictions
def accuracy_check(df):
    matches_number = 0
    exact_result = 0
    correct_outcome = 0
    for idx, row in df.iterrows():
        matches_number += 1

        elo_diff = row['elo_diff']
        home_off_power = row['home_offensive_power']
        away_off_power = row['away_offensive_power']
        home_def_power = row['home_deffensive_power']
        away_def_power = row['away_deffensive_power']
        home_score = row['home_score']
        away_score = row['away_score']

        home_pred, away_pred = predict_match(home_off_power, away_off_power, home_def_power, away_def_power)

        home_pred = home_pred + reg.predict(np.array([elo_diff]).reshape(-1, 1))[0]
        away_pred = away_pred - reg.predict(np.array([elo_diff]).reshape(-1, 1))[0]

        # Predict the most likely score using the Poisson distribution
        max_goals = 10
        home_goals_prob = [poisson.pmf(i, home_pred) for i in range(max_goals + 1)]
        away_goals_prob = [poisson.pmf(i, away_pred) for i in range(max_goals + 1)]

        most_likely_home_goals = np.argmax(home_goals_prob)
        most_likely_away_goals = np.argmax(away_goals_prob)

        print(most_likely_home_goals, '-', most_likely_away_goals, ' where should be ', home_score, '-', away_score)

        if home_score == most_likely_home_goals and away_score == most_likely_away_goals:
            exact_result += 1

        if home_score > away_score:
            result = 1.0
        elif home_score < away_score:
            result = 0.0
        else:
            result = 0.5

        if home_pred > away_pred:
            prediction = 1.0
        elif home_pred < away_pred:
            prediction = 0.0
        else:
            prediction = 0.5

        if result == prediction:
            correct_outcome += 1

    print('Accuracy of exact scores: ', exact_result / matches_number)
    print('Accuracy of correct outcome: ', correct_outcome / matches_number)


# Check accuracy on the test set
accuracy_check(test_df)