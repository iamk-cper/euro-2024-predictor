
# EURO 2024 Match Prediction Model Report

## 1. Test and Training Results

- Model accuracy in predicting exact scores / match winners:

  ![Accuracy](assets/accuracy.png)
- Predictions of the percentage chances for each team's place in their EURO 2024 group based on 1000 simulations of the group stage:

  ![Results](assets/results.png)

## 2. Justification for Choosing the Technique/Model

- The Poisson model was chosen because the number of goals scored in a match follows a Poisson distribution.

  ![Goal Distribution](assets/goals-scored-plot.png)
  ![Team Goal Distribution](assets/team-goals-scored-plot.png)
- Additionally, a linear regression model was used to further differentiate between teams with different ELO ratings, to increase the importance of the ELO factor in the context of the predicted result.

  ![ELO and Goals Correlation](assets/elo-goals-correlation.png)

## 3. Input Data Description

- Data cleaning to remove missing values.
- ELO ratings calculated for participants of each match since the 19th century.
- Based on the number of goals scored and conceded, and the ELO difference between opponents, the relative offensive and defensive strength of participants at the time of the match is calculated (more recent matches have greater weight).
- The ELO value is rescaled when passed to the model to prevent ELO from dominating over offensive and defensive strength.
- Data from very old matches, for which ELO and relative strength values are not accurately calculated, are omitted.
- The model uses relative strength, ELO value, and match results.

## 4. Data Splitting Strategy

- Data split into test and training sets.
- From each match, two training values are extracted: ELO difference and own offensive strength and opponent's defensive strength for each participant, based on which the model predicts the number of goals scored (float).
- The model is tested by comparing the actual result with the most probable match result predicted based on the Poisson distribution (using the predicted goals coefficient) and further diversified using the correlation between ELO difference and goal difference in matches.
- k-fold Cross-Validation used for better model performance.

## 5. Results Analysis

- Predictions of team positions in their groups seem relatively realistic for someone familiar with football.
- Score predictions definitely need improvements; current test results are not fully satisfactory, and predicted exact results are also inaccurate, e.g., the 1-1 result appears too often.

## 6. Next Steps

- The final model for predicting tournament results should not be based on test and training data, but on all provided data.
