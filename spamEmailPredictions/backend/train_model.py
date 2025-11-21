import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

# Define paths
# Assuming script is run from backend/ directory or we use absolute paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '../mail_data.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')

def train():
    print(f"Looking for dataset at: {DATA_PATH}")
    if os.path.exists(DATA_PATH):
        print(f"Dataset found.")
        raw_data = pd.read_csv(DATA_PATH)
    else:
        print("Dataset not found. Using dummy data for demonstration.")
        # Create dummy data
        data = {
            'Category': ['ham', 'spam', 'ham', 'spam', 'ham'] * 20,
            'Message': [
                'Hello, how are you?',
                'Win a free lottery now!',
                'Meeting at 3 PM',
                'Click here to claim your prize',
                'Can we talk later?'
            ] * 20
        }
        raw_data = pd.DataFrame(data)

    # Pre-processing
    mail_data = raw_data.where((pd.notnull(raw_data)), '')
    
    # Label Encoding
    mail_data.loc[mail_data['Category'] == 'spam', 'Category'] = 0
    mail_data.loc[mail_data['Category'] == 'ham', 'Category'] = 1
    
    X = mail_data['Message']
    Y = mail_data['Category']
    
    # Train Test Split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=3)
    
    # Feature Extraction
    print("Extracting features...")
    feature_extraction = TfidfVectorizer(min_df=1, stop_words='english', lowercase=True)
    X_train_features = feature_extraction.fit_transform(X_train)
    X_test_features = feature_extraction.transform(X_test)
    
    Y_train = Y_train.astype('int')
    Y_test = Y_test.astype('int')
    
    # Model Training
    print("Training model...")
    model = LogisticRegression()
    model.fit(X_train_features, Y_train)
    
    # Evaluation
    prediction_on_training_data = model.predict(X_train_features)
    accuracy_on_training_data = accuracy_score(Y_train, prediction_on_training_data)
    print(f"Accuracy on training data: {accuracy_on_training_data}")
    
    # Save model and vectorizer
    print("Saving artifacts...")
    joblib.dump(model, MODEL_PATH)
    joblib.dump(feature_extraction, VECTORIZER_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print(f"Vectorizer saved to {VECTORIZER_PATH}")

if __name__ == "__main__":
    train()
