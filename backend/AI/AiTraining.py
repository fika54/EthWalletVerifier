import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from pathlib import Path


def initialTrain():

    fullList = pd.read_csv('wallets_features_classes_combined.csv')
    fullList = fullList.drop_duplicates(subset='address', keep='first')
    illicit = fullList[fullList['class'] == 1]
    licit = fullList[fullList['class'] == 2]
    unknown = fullList[fullList['class'] == 3]

    #testIllicit = illicit.iloc[:20]
    #illicit = illicit.iloc[20:]
    #testLicit = licit.iloc[:20]
    #licit = licit.iloc[20:]

    #testSet = [testIllicit, testLicit]
    #testSet = pd.concat(testSet)

    #testSet = testSet.drop(['class'], axis=1)
    #testSet = testSet.drop(['address'], axis=1)

    c = [illicit, licit]

    Set = pd.concat(c)

    y = Set['class']
    X = Set.drop(['class'], axis=1)
    X = X.drop(['address'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)


    rfc = RandomForestClassifier(n_estimators=600)
    rfc.fit(X_train, y_train)


    joblib.dump(rfc, "finalModel.pkl")


    rfc_pred = rfc.predict(X_test)

    print(classification_report(y_test, rfc_pred))

    print(confusion_matrix(y_test, rfc_pred))

#       class  precision    recall  f1-score   support

#           1       0.96      0.79      0.87      2760
#           2       0.99      1.00      0.99     50311

#    accuracy                           0.99     53071
#   macro avg       0.98      0.90      0.93     53071
#weighted avg       0.99      0.99      0.99     53071

def alteredTrain():

    fullList = pd.read_csv('wallets_features_classes_combined.csv')
    fullList = fullList.drop_duplicates(subset='address', keep='first')
    illicit = fullList[fullList['class'] == 1]
    licit = fullList[fullList['class'] == 2]
    unknown = fullList[fullList['class'] == 3]

    licit = licit.sample(n=illicit.shape[0]+5000)

    print("illicit", illicit.shape[0])
    print("licit", licit.shape[0])

    c = [illicit, licit]

    Set = pd.concat(c)

    y = Set['class']
    X = Set.drop(['class'], axis=1)
    X = X.drop(['address'], axis=1)
    X = X[['num_txs_as_sender', 'num_txs_as receiver', 'first_block_appeared_in', 'last_block_appeared_in', 'lifetime_in_blocks', 'total_txs', 'first_sent_block', 'first_received_block']]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)


    rfc = RandomForestClassifier(n_estimators=600)
    rfc.fit(X_train, y_train)#


    joblib.dump(rfc, 'finalModel.pkl')


    rfc_pred = rfc.predict(X_test)

    print(classification_report(y_test, rfc_pred))

    print(confusion_matrix(y_test, rfc_pred))


#       class  precision    recall  f1-score   support

#           1       0.87      0.85      0.86      2799
#           2       0.89      0.91      0.90      3908

#    accuracy                           0.88      6707
#   macro avg       0.88      0.88      0.88      6707
#weighted avg       0.88      0.88      0.88      6707

#       class  precision    recall  f1-score   support

#           1       0.77      0.56      0.65      2760
#           2       0.98      0.99      0.98     50311

#    accuracy                           0.97     53071
#   macro avg       0.87      0.78      0.82     53071
#weighted avg       0.97      0.97      0.97     53071


initialTrain()

