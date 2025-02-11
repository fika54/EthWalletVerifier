Before Using this project please ensure you have the right dependencies installed.

Run the following commands:

python -m venv venv

(Run only the relevant command)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows


pip install -r requirements.txt

Then access the dataset below.

You can access the dataset here (It is the csv file labelled wallets_features_classes_combined.csv):
https://drive.google.com/drive/folders/1MRPXz79Lu_JGLlJ21MDfML44dKN9R08l

Courtesty of:
Youssef Elmougy and Ling Liu. 2023. Demystifying Fraudulent Transactions and Illicit Nodes in the Bitcoin Network for Financial 
Forensics. In Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD ’23), August 6–10, 2023
, Long Beach, CA, USA. ACM, New York, NY, USA, 16 pages. https://doi.org/10.1145/3580305.3599803

make sure to import the file to the root directory for the model to train properly.

Once the file is there, run the AiTraining.py script in AI and it will train a model and store it in a .pkl file.

then the application should run properly