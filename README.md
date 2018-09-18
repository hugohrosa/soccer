This is a small project to illustrate potential uses of Machine Learning (ML) techniques applied to football.
Dataset: https://www.kaggle.com/shubhmamp/english-premier-league-match-data

ASSUMPTIONS:

- only stats for players that started in more than 5 matches were considered;
- stats from players that came in to the match via substitution were NOT considered;

EXTRA STATS:

When possible, extra stats were created regarding the players, namely:
- the "per game" ratio regarding things such as goals, assists, passes, etc.
- the "successs rate" of a few stats, such as: "goal per shot rate", "accurate pass per total pass rate" and "number of assists per accurate pass" rate 

# POSITION CLASSIFIER

The dataset consists of 1134 entries of a player's stats in a football match and aims to classify the position it played, out of the 15 available positions. The idea is that certain players are fitter to play in certain positions, based on their stats: a defender will have more tackles, a midfielder more passes and a striker more goals.

    LABEL DECODING
    0	['AMC']; 
    1	['AML']; 
    2	['AMR']; 
    3	['DC']; 
    4	['DL']; 
    5	['DMC']; 
    6	['DML']; 
    7	['DMR']; 
    8	['DR']; 
    9	['FW']; 
    10	['FWL']; 
    11	['FWR']: 
    12	['GK']; 
    13	['MC']; 
    14	['ML']: 
    15	['MR']

             precision    recall  f1-score   support

          0       0.21      0.21      0.21        85
          1       0.09      0.08      0.09        61
          2       0.12      0.05      0.07        63
          3       0.72      0.58      0.64       149
          4       0.37      0.19      0.25        77
          5       0.28      0.26      0.27       101
          6       0.30      0.25      0.27        12
          7       0.07      0.47      0.12        17
          8       0.27      0.25      0.26        77
          9       0.82      0.69      0.75       121
         10       0.04      0.03      0.04        29
         11       0.10      0.50      0.17        32
         12       1.00      0.98      0.99        62
         13       0.47      0.26      0.33       152
         14       0.05      0.06      0.05        48
         15       0.07      0.04      0.05        48
        --------------------------------------------
        avg       0.41      0.34      0.36      1134


A quick analysis of the results, considering the MultinomialNB() as the best performing classifier (based on a better Precision), shows that the classifier is very good at classifying DC, FWC and GK. This is easily explained by the presence of certain stats such as goals (FWC), tackles (DC) and saves (GK) that will rarely be found in other positions, therefore making these classes the more distinguishable for a standard classifier such as MNB.

In other positions it can be almost totally ineffective (ML, MR, FWL, DMR) as their stats will blend with stats common to other positions.

While overall results are insufficient, this is a brief example of how a basic non-optimized classifier, using insufficient data (1134 samples with 44 statistics from players) would perform at finding the best position for a player based on its stats. More detailed data and a more robust experiment (GridSearchCV for parameter optimization) is required to further similar practical applications.

# RATING REGRESSION

The dataset consists of 1134 entries of players stat's and their average rating for a minimum of 5 games played. The idea is to have a regression algorithm attempt to predict a players rating based on his stats.

A quick analysis of the Linear Regression solution shows that that the average variance of the predicted rating to the real rating is quite small (ratings are from 0 to 10 and the RMSE is aprox. -0.075). In the scope of this task, this is a quite acceptable error to have has the rating would be accurate to the first decimal point.

    average neg_mean_squared_error: -0.0749781285391
