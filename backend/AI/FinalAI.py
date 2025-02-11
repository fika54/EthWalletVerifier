import joblib
import pandas as pd

# Function to take a dataset and return the predicted class and confidence level
def verifWallet(dataSet):
    """
    Verifies the wallet by running the dataset through the trained model.
    
    :param dataSet: pandas DataFrame: The dataset to be evaluated.
    :return: dict: A dictionary with the predicted class and confidence score.
    """
    # Load the trained model from the file
    model = joblib.load("finalModel.pkl")

    # Get the probabilities for each class (in case of multi-class classification)
    resultsproba = model.predict_proba(dataSet)
    
    # Get the predicted class for each row in the dataset
    results = model.predict(dataSet)

    # Get the final predicted class for the first row of the dataset
    finalClass = results[0]

    # Get the maximum confidence score from the predicted probabilities
    confidence = resultsproba[0].max()

    # Store the results in a dictionary
    fr = {
        'class': finalClass,        # The predicted class (e.g., 0 or 1)
        'confidence': confidence    # The confidence level for the prediction (e.g., 0.85)
    }

    return fr  # Return the result dictionary   