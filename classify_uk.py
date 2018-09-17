from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LinearRegression, Lasso
import pickle
from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn import metrics
from sklearn import preprocessing


with open('uk_players_stats.pkl', 'rb') as p:
    players = pickle.load(p)
with open('uk_players_positions.pkl', 'rb') as p:
    pos = pickle.load(p)
with open('uk_players_avg_ratings.pkl', 'rb') as p:
    ratings = pickle.load(p)


# TRANSFORM LABELS 'POSITIONS' INTO NUMERIC
le = preprocessing.LabelEncoder()
y = le.fit_transform(pos)
print("LABEL DECODING")
for i in range(0, 16, 1):
    print(str(i) + '\t' + str(le.inverse_transform([i])))

v = DictVectorizer(sparse=False)
X = v.fit_transform(players)

# CLASSIFY FOR POSITION
classifiers = [MultinomialNB()] #,
               # LinearSVC(),
               # LogisticRegression()]

for clf in classifiers:
    clf.fit(X, y)
    predicted = cross_val_predict(clf, X, y, cv=10)
    print(str(metrics.classification_report(y, predicted)))


# REGRESSION FOR MATCH RATING
y = ratings
regression = [LinearRegression(),
              Lasso()]

for clf in regression:
    score = cross_val_score(clf, X, y, cv=10)
    print(score)
