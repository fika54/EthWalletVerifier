import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from pathlib import Path

# Function to train an initial Random Forest model
def initialTrain():
    # Load dataset from CSV file
    fullList = pd.read_csv('wallets_features_classes_combined.csv')
    
    # Remove duplicate wallet addresses, keeping the first occurrence
    fullList = fullList.drop_duplicates(subset='address', keep='first')
    
    # Separate illicit (class 1) and licit (class 2) wallet addresses
    illicit = fullList[fullList['class'] == 1]
    licit = fullList[fullList['class'] == 2]
    
    # Combine illicit and licit data into a single dataset
    c = [illicit, licit]
    Set = pd.concat(c)
    
    # Define features (X) and target variable (y)
    y = Set['class']
    X = Set.drop(['class'], axis=1)  # Drop target column
    X = X.drop(['address'], axis=1)  # Drop address column since it's not a feature
    
    # Split dataset into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)
    
    # Initialize Random Forest Classifier with 600 decision trees
    rfc = RandomForestClassifier(n_estimators=600)
    
    # Train the model
    rfc.fit(X_train, y_train)
    
    # Save the trained model to a file using joblib
    joblib.dump(rfc, "finalModel.pkl")
    
    # Make predictions on the test set
    rfc_pred = rfc.predict(X_test)
    
    # Print performance metrics
    print(classification_report(y_test, rfc_pred))
    print(confusion_matrix(y_test, rfc_pred))

# Function to train an alternative model with different data balancing strategy
def alteredTrain():
    # Load dataset from CSV file
    fullList = pd.read_csv('wallets_features_classes_combined.csv')
    
    # Remove duplicate wallet addresses, keeping the first occurrence
    fullList = fullList.drop_duplicates(subset='address', keep='first')
    
    # Separate illicit (class 1), licit (class 2), and unknown (class 3) wallet addresses
    illicit = fullList[fullList['class'] == 1]
    licit = fullList[fullList['class'] == 2]
    unknown = fullList[fullList['class'] == 3]  # Unused in training
    
    # Balance the dataset by sampling licit data to match illicit count + 5000
    licit = licit.sample(n=illicit.shape[0] + 5000)
    
    # Print dataset sizes for verification
    print("illicit", illicit.shape[0])
    print("licit", licit.shape[0])
    
    # Combine illicit and sampled licit data
    c = [illicit, licit]
    Set = pd.concat(c)
    
    # Define features (X) and target variable (y)
    y = Set['class']
    X = Set.drop(['class'], axis=1)
    X = X.drop(['address'], axis=1)
    
    # Select a specific subset of features for training
    X = X[['num_txs_as_sender', 'num_txs_as receiver', 'first_block_appeared_in', 'last_block_appeared_in', 'lifetime_in_blocks', 'total_txs', 'first_sent_block', 'first_received_block']]
    
    # Split dataset into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)
    
    # Initialize Random Forest Classifier with 600 decision trees
    rfc = RandomForestClassifier(n_estimators=600)
    
    # Train the model
    rfc.fit(X_train, y_train)
    
    # Save the trained model to a file using joblib
    joblib.dump(rfc, 'finalModel.pkl')
    
    # Make predictions on the test set
    rfc_pred = rfc.predict(X_test)
    
    # Print performance metrics
    print(classification_report(y_test, rfc_pred))
    print(confusion_matrix(y_test, rfc_pred))

# Run the initial training function
initialTrain()