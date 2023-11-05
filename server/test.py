from joblib import load

# Load the model from the file
model_filename = 'sentiment_analysis_model.joblib'
trained_model = load(model_filename)

# Clear positive and negative examples to test the model
test_texts = [
"Google Pixel 2023 liveblog: Live updates on the Pixel 8 reveal ith Apple, Samsung, Microsoft and Amazon already having had their fall announcement events this year, Google's hardware keynote is ostensibly the last major launch of 2023. The company has more or less told us what it's going to be unveiling today, teasing u "
]

# Predict sentiments for the test texts
predictions = trained_model.predict(test_texts)

# Output the predictions
for text, prediction in zip(test_texts, predictions):
    print(f"Text: {text}\nPredicted Sentiment: {prediction}\n")
