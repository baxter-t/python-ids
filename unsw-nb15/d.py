import numpy as np
import pandas as pd
import pydotplus

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score
from sklearn import tree, svm
from joblib import dump, load
from IPython.display import Image

import pickle
import csv
import json


# Attack Type Mappings
ANALYSIS = 0
BACKDOOR = 1
DOS = 2
EXPLOITS = 3
FUZZERS = 4
GENERIC = 5
NORMAL = 6
RECONNAISSANCE = 7
SHELLCODE = 8
WORMS = 9
ALL = 10

ATTACK_TYPES = [
    ANALYSIS,
    BACKDOOR,
    DOS,
    EXPLOITS,
    FUZZERS,
    GENERIC,
    NORMAL,
    RECONNAISSANCE,
    SHELLCODE,
    WORMS,
    ALL
]

ATTACK_TYPES_NAMES = {
    0: "ANALYSIS",
    1: "BACKDOOR",
    2: "DOS",
    3: "EXPLOITS",
    4: "FUZZERS",
    5: "GENERIC",
    6: "NORMAL",
    7: "RECONNAISSANCE",
    8: "SHELLCODE",
    9: "WORMS",
    10: "ALL"
}


def train_and_output(df, attack_type=None, min_depth=1, max_depth=10):

    # Filter for normal OR attack type
    if attack_type == None:
        attack_type = 10
    else:
        df = df[(df["attack_cat"] == attack_type) | (df["attack_cat"] == NORMAL)]

    outputFileName = "accuracy-output-metrics-{}.csv".format(
        ATTACK_TYPES_NAMES.get(attack_type, "ALL")
    )
    with open(outputFileName, "w") as outputFile:
        writer = csv.writer(outputFile, delimiter=",")
        writer.writerow(
            [
                "DEPTH",
                "TEST",
                "FP TEST",
                "TP TEST",
                "FN TEST",
                "TN TEST",
                "TRAIN",
                "FP TRAIN",
                "TP TRAIN",
                "FN TRAIN",
                "TN TRAIN",
            ]
        )

        for DEPTH in range(min_depth, max_depth):

            X = df.values[:, 1:43]
            Y = df.values[:, 44]

            xTrain, xTest, yTrain, yTest = train_test_split(
                X, Y, test_size=0.3, random_state=100
            )

            clf = DecisionTreeClassifier(criterion="entropy", max_depth=DEPTH)

            clf.fit(xTrain, yTrain)

            # Create DOT data
            dot_data = tree.export_graphviz(
                clf, out_file=None, feature_names=df.columns[1:43]
            )
            # Draw graph
            graph = pydotplus.graph_from_dot_data(dot_data)
            # Show graph
            Image(graph.create_png())
            # Create PNG
            graph.write_png("{}_{}".format(ATTACK_TYPES_NAMES[attack_type], DEPTH))

            yPredTest = clf.predict(xTest)
            yPredTrain = clf.predict(xTrain)

            fpTest, tpTest, fnTest, tnTest = gen_fptpfntn(yTest, yPredTest)
            fpTrain, tpTrain, fnTrain, tnTrain = gen_fptpfntn(yTrain, yPredTrain)

            writer.writerow(
                [
                    DEPTH,
                    accuracy_score(y_true=yTest, y_pred=yPredTest),
                    fpTest,
                    tpTest,
                    fnTest,
                    tnTest,
                    accuracy_score(y_true=yTrain, y_pred=yPredTrain),
                    fpTrain,
                    tpTrain,
                    fnTrain,
                    tnTrain,
                ]
            )

            print("---------------------------------------------------------")
            print(
                "DEPTH: {},  fp: {} tp: {} fn: {} tn: {}".format(
                    DEPTH, fpTest, tpTest, fnTest, tnTest
                )
            )

            print(
                "Features used for: {}, Depth of: {}".format(
                    ATTACK_TYPES_NAMES[attack_type], DEPTH
                )
            )
            print("Training Acc: {}, Testing Acc: {}".format(
                    accuracy_score(y_true=yTrain, y_pred=yPredTrain),
                    accuracy_score(y_true=yTest, y_pred=yPredTest)
            ))
            print("---------------------------------------------------------")

            for i, x in enumerate(clf.feature_importances_):
                if x != 0:
                    print("    {}: {}".format(df.columns[i + 1], x))

            print("")


def gen_fptpfntn(actual, pred):
    fp = 0
    tp = 0
    fn = 0
    tn = 0
    num = len(actual)
    actualPos = 0
    actualNeg = 0

    for i in range(num):
        if actual[i] and pred[i]:
            tp += 1
            actualPos += 1
        elif not actual[i] and pred[i]:
            fp += 1
            actualNeg += 1
        elif actual[i] and not pred[i]:
            fn += 1
            actualPos += 1
        elif not actual[i] and not pred[i]:
            tn += 1
            actualNeg += 1

    if actualPos == 0 or actualNeg == 0:
        return 0, 0, 0, 0

    return fp / actualPos, tp / actualPos, fn / actualNeg, tn / actualNeg


df = pd.read_csv("UNSW_NB15_training-set_processed.csv", sep=",", header=0)

# for aType in ATTACK_TYPES:
#     if aType != NORMAL:
#         train_and_output(df, aType, min_depth=4, max_depth=5)

train_and_output(df, attack_type=DOS, min_depth=3, max_depth=16)
