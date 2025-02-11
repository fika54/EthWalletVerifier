import joblib
import pandas as pd

#function to take a dataset and return the class and confidence
def verifWallet(dataSet):
    model = joblib.load("finalModel.pkl")
    resultsproba = model.predict_proba(dataSet)
    results = model.predict(dataSet)

    finalClass = results[0]
    confidence = resultsproba[0].max()

    fr = {
        'class': finalClass,
        'confidence': confidence
    }

    return fr

#model = joblib.load("model.pkl")

#fullList = pd.read_csv('wallets_features_classes_combined.csv')
#fullList = fullList.drop_duplicates()



#illicit = fullList[fullList['class'] == 1]
#licit = fullList[fullList['class'] == 2]
#Unknown = fullList[fullList['class'] == 3]

#testIllicit = illicit.iloc[:20]
#illicit = illicit.iloc[20:]
#testLicit = licit.iloc[:20]
#licit = licit.iloc[20:]

#testSet = [testIllicit, testLicit]
#testSet = pd.concat(testSet)

#YTest = testSet['class']
#Addresses = testSet['address']

#testSet = testSet.drop(['class'], axis=1)
#testSet = testSet.drop(['address'], axis=1)


#resultsproba = model.predict_proba(testSet)
#results = model.predict(testSet)

#tabledResults = pd.DataFrame(
#    {
#        'Address': Addresses,
#        'Prediction': results,
#        'Confidence': resultsproba.max(axis=1),
#        'Real Value': YTest
#   }
#)

#tabledResults['valid'] = tabledResults['Prediction'] == tabledResults['Real Value']

#print(tabledResults)


#from sklearn.metrics import classification_report, confusion_matrix
#print(classification_report(YTest, results))

#print(confusion_matrix(YTest, results))


