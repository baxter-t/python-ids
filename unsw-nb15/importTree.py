import numpy as np
import pandas as pd
import pydotplus

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score
from sklearn import tree, svm
from joblib import dump, load
from sklearn.externals.six import StringIO
from IPython.display import Image

data = pd.read_csv("UNSW_NB15_training-set_processed.csv", sep=",", header=0)

print("Dataset Length:", len(data))
print("Dataset Shape:", data.shape)

X = data.values[:, 1:43]
Y = data.values[:, 44]

xTrain, xTest, yTrain, yTest = train_test_split(X, Y, test_size=0.3, random_state=100)

clf = load("trained.joblib")


print(clf)

yPred = clf.predict(xTest)

dot_data = StringIO()

export_graphviz(
    clf, out_file=dot_data, filled=True, rounded=True, special_characters=True
)

graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.create_png())

graph.write_png("output.png")

print("Outputting Model")
dump(clf, "trained.joblib")


print(
    "Accuracy score on train data:",
    accuracy_score(y_true=yTrain, y_pred=clf.predict(xTrain)),
)
print("Accuracy score on test data:", accuracy_score(y_true=yTest, y_pred=yPred))
