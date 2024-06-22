import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import PoissonRegressor
from goal_distribution import df2

df3 = df2[['home_score', 'away_score', 'elo_diff', 'home_deffensive_power', 'away_deffensive_power', 'home_offensive_power', 'away_offensive_power']]

# Split the data into training and test sets
train_df, test_df = train_test_split(df3, test_size=0.2, random_state=42)

# Apply the scaler to the feature columns only (excluding target columns)
X_train = train_df.drop(columns=['home_score', 'away_score', 'elo_diff'])
X_test = test_df.drop(columns=['home_score', 'away_score', 'elo_diff'])

# Convert the scaled arrays back to DataFrames
y_train = train_df[['home_score', 'away_score']]

# Function to transform features for model input
def transform_x(df):
    home_df = df[['home_offensive_power', 'away_deffensive_power']].copy()
    home_df.columns = ['offensive_power', 'deffensive_power']

    away_df = df[['away_offensive_power', 'home_deffensive_power']].copy()
    away_df.columns = ['offensive_power', 'deffensive_power']

    new_df = pd.concat([home_df, away_df], ignore_index=True)
    return new_df


# Function to transform targets for model input
def transform_y(df):
    home_df = df[['home_score']].copy()
    home_df.columns = ['team_score']

    away_df = df[['away_score']].copy()
    away_df.columns = ['team_score']

    new_df = pd.concat([home_df, away_df], ignore_index=True)
    return new_df


# Apply transformations
X_train_final = transform_x(X_train)
y_train_final = transform_y(y_train)

# Cross-validation setup
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Initialize model
model = PoissonRegressor()
cv_score = cross_val_score(model, X_train_final, y_train_final, cv=kf, scoring='neg_mean_absolute_error')
print(f'Cross-Validation Score (MAE): {-cv_score.mean()}')

model.fit(X_train_final, y_train_final)


# Function to predict match outcomes
def predict_match(home_off_power, away_off_power, home_def_power, away_def_power):
    # Create feature arrays for both teams
    features_home = np.array([[home_off_power, away_def_power]])
    features_away = np.array([[away_off_power, home_def_power]])

    # Predict goals
    predicted_home_goals = model.predict(features_home)
    predicted_away_goals = model.predict(features_away)

    return predicted_home_goals[0], predicted_away_goals[0]