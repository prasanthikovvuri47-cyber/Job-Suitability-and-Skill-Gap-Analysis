import pandas as pd
import numpy as np
import pickle
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import warnings

warnings.filterwarnings('ignore')

def remove_noise(df):
    """
    Step 1: Remove Noise
    Drops null values and removes exact duplicate rows.
    """
    print("  -> Removing noise (nulls and duplicates)...")
    initial_len = len(df)
    df = df.dropna()
    df = df.drop_duplicates()
    print(f"     Dropped {initial_len - len(df)} rows.")
    return df

def clean_text(text):
    """
    Step 2: Text Cleaning
    Lowercases, removes special characters, and strips extra spaces.
    """
    if not isinstance(text, str):
        return ""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters using Regex (keep alphanumeric, space, and comma)
    text = re.sub(r'[^a-z0-9\s,]', '', text)
    # Remove extra spaces
    text = " ".join(text.split())
    return text

def standardize_tokens(text):
    """
    Step 3 & 4: Token Handling and Standardization
    Splits skills by comma, strips them, and enforces standard naming.
    """
    # Split skills by comma and strip spaces
    tokens = [t.strip() for t in text.split(',') if t.strip()]
    
    # Standardization replacements dictionary
    replacements = {
        'ml': 'machine learning',
        'js': 'javascript',
        'ai': 'artificial intelligence'
    }
    
    # Apply replacements
    standardized = [replacements.get(t, t) for t in tokens]
    
    # Rejoin clean tokens
    return ", ".join(standardized)

def preprocess_data(df):
    """
    Main Preprocessing Pipeline
    Combines all preprocessing steps to prepare data for feature engineering.
    """
    print("Preprocessing data explicitly...")
    
    # 1. Remove Noise
    df = remove_noise(df)
    
    # 2. Text Cleaning
    print("  -> Cleaning text strings...")
    df['skills'] = df['skills'].apply(clean_text)
    
    # 3. Token Standardization
    print("  -> Standardizing skill tokens...")
    df['skills'] = df['skills'].apply(standardize_tokens)
    
    return df

def top_k_accuracy(y_true, y_pred_proba, k=3):
    """
    Calculates the proportion of true labels that appear within the top k predictions.
    """
    top_k_preds = np.argsort(y_pred_proba, axis=1)[:, -k:]
    if isinstance(y_true, pd.Series):
        y_true_vals = y_true.values
    else:
        y_true_vals = y_true
        
    correct = sum([1 for i in range(len(y_true_vals)) if y_true_vals[i] in top_k_preds[i]])
    return correct / len(y_true_vals)

def train_and_save_models():
    print("Loading dataset...")
    df = pd.read_csv("career_data.csv")
    
    # ==========================================
    # DATA PREPROCESSING SECTION (CRITICAL)
    # ==========================================
    df = preprocess_data(df)
    
    # ==========================================
    # FEATURE ENGINEERING
    # ==========================================
    print("\nPreparing features...")
    
    # TF-IDF for skills with ngram_range (1,1) only and very limited features
    print("  -> Applying TF-IDF on skills (highly simplified)...")
    tfidf = TfidfVectorizer(max_features=500, stop_words='english', ngram_range=(1,1))
    skills_tfidf = tfidf.fit_transform(df['skills']).toarray()
    
    # Encode education categories
    print("  -> Encoding categorical variables...")
    edu_encoder = LabelEncoder()
    edu_encoded = edu_encoder.fit_transform(df['education']).reshape(-1, 1)
    
    # Experience (numeric)
    exp = df['experience'].values.reshape(-1, 1)
    
    # Combine features horizontally
    X = np.hstack((skills_tfidf, edu_encoded, exp))
    
    # Label Encode Target Variable (job_role)
    target_encoder = LabelEncoder()
    y = target_encoder.fit_transform(df['job_role'])
    
    # Train Test Split (further increase test size for stricter evaluation)
    print("  -> Splitting dataset into training and testing sets (40% test size)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    
    # ==========================================
    # MODEL TRAINING & EVALUATION
    # ==========================================
    
    # Train Logistic Regression (strong regularization C=0.01)
    print("\n[1/2] Training Logistic Regression...")
    lr_model = LogisticRegression(max_iter=1000, class_weight='balanced', C=0.01)
    lr_model.fit(X_train, y_train)
    
    lr_proba = lr_model.predict_proba(X_test)
    lr_top3 = top_k_accuracy(y_test, lr_proba, k=3)
    
    # Train Random Forest (limited depth max_depth=8)
    print("\n[2/2] Training Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', max_depth=8, random_state=42)
    rf_model.fit(X_train, y_train)
    
    rf_proba = rf_model.predict_proba(X_test)
    rf_top3 = top_k_accuracy(y_test, rf_proba, k=3)
    
    # Select Best Model based on Top-3 Match Rate
    best_model = None
    final_accuracy = 0
    if rf_top3 > lr_top3:
        best_model = rf_model
        final_accuracy = rf_top3
        print("\n=> Selected Random Forest as the best model.")
    else:
        best_model = lr_model
        final_accuracy = lr_top3
        print("\n=> Selected Logistic Regression as the best model.")
    
    # Final Output as requested
    print(f"\nTop-3 Accuracy: {final_accuracy:.2f}")
        
    # ==========================================
    # SAVE PIPELINE ARTIFACTS
    # ==========================================
    print("\nSaving models and transformers...")
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
