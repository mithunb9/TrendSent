import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

# Load data from a CSV file
df = pd.read_csv('train.csv', header=None, names=['sentiment', 'text'], encoding='ISO-8859-1')

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    df['text'],
    df['sentiment'],
    test_size=0.2,
    random_state=42,
    stratify=df['sentiment']  # Ensure stratified split
)

# Create a machine learning pipeline with TfidfVectorizer and a more complex classifier like SVM
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', ngram_range=(1, 2))),
    ('clf', SVC(class_weight='balanced', probability=True)),  # Use class_weight='balanced' to handle imbalanced classes
])

# Define a parameter grid to search for the best parameters for both the vectorizer and the classifier
param_grid = {
    'tfidf__max_df': (0.5, 0.75, 1.0),
    'tfidf__max_features': (None, 5000, 10000),
    'clf__C': [0.1, 1, 10],
    'clf__kernel': ['linear', 'rbf']
}

# Set up GridSearchCV to find the best parameters using stratified K-fold cross-validation
grid_search = GridSearchCV(pipeline, param_grid, cv=StratifiedKFold(n_splits=5), n_jobs=-1)

# Train the model
grid_search.fit(X_train, y_train)

# Best parameter set
print("Best parameters set found on development set:")
print(grid_search.best_params_)

# Predict on the test data
predictions = grid_search.predict(X_test)

# Evaluate the model
print(classification_report(y_test, predictions))
print(f"Accuracy: {accuracy_score(y_test, predictions)}")

# Predict the sentiment of a new text
new_texts = ["This is a new text to predict its sentiment."]
new_predictions = grid_search.predict(new_texts)
print(new_predictions)
