import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import warnings

warnings.filterwarnings('ignore')

def train_and_save_models():
    print("Loading dataset...")
    df = pd.read_csv("career_data.csv")
    
    # Preprocessing
    print("Preprocessing data...")
    # Fill any NaNs (just in case, though generator has none)
    df.fillna('', inplace=True)
    
    # TF-IDF for skills
    tfidf = TfidfVectorizer(max_features=500, stop_words='english')
    skills_tfidf = tfidf.fit_transform(df['skills']).toarray()
    
    # Encode education
    edu_encoder = LabelEncoder()
    edu_encoded = edu_encoder.fit_transform(df['education']).reshape(-1, 1)
    
    # Experience
    exp = df['experience'].values.reshape(-1, 1)
    
    # Combine features
    X = np.hstack((skills_tfidf, edu_encoded, exp))
    
    # Target
    target_encoder = LabelEncoder()
    y = target_encoder.fit_transform(df['job_role'])
    
    # Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Logistic Regression
    print("Training Logistic Regression...")
    lr_model = LogisticRegression(max_iter=1000, class_weight='balanced')
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)
    lr_acc = accuracy_score(y_test, lr_pred)
    print(f"Logistic Regression Accuracy: {lr_acc:.4f}")
    
    # Train Random Forest
    print("Training Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_acc = accuracy_score(y_test, rf_pred)
    print(f"Random Forest Accuracy: {rf_acc:.4f}")
    
    # Select Best Model
    best_model = None
    if rf_acc > lr_acc:
        best_model = rf_model
        print("Selected Random Forest as the best model.")
    else:
        best_model = lr_model
        print("Selected Logistic Regression as the best model.")
        
    # Save objects
    print("Saving models and transformers...")
    with open("best_model.pkl", "wb") as f:
        pickle.dump(best_model, f)
        
    with open("tfidf_vectorizer.pkl", "wb") as f:
        pickle.dump(tfidf, f)
        
    with open("edu_encoder.pkl", "wb") as f:
        pickle.dump(edu_encoder, f)
        
    with open("target_encoder.pkl", "wb") as f:
        pickle.dump(target_encoder, f)
        
    print("Model training completed successfully.")

if __name__ == "__main__":
    train_and_save_models()
