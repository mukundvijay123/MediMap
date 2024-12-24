#SVM
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

# Load the dataset
data = pd.read_csv("synthetic_accident_reports.csv")

# Split the dataset into features (X) and labels (y)
X = data["report"]
y = data["department"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text data into TF-IDF features
tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Train an SVM classifier
svm_classifier = SVC(kernel="linear", probability=True, random_state=42)
svm_classifier.fit(X_train_tfidf, y_train)

# Predict the department for the test set
y_pred = svm_classifier.predict(X_test_tfidf)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Function to predict the department for a new report
def predict_department(report):
    report_tfidf = tfidf_vectorizer.transform([report])
    prediction = svm_classifier.predict(report_tfidf)
    probabilities = svm_classifier.predict_proba(report_tfidf)
    return prediction[0], probabilities.max()

# Example usage
new_report = "Patient reports high creatinine levels"
predicted_department, confidence = predict_department(new_report)
print(f"The predicted department for the report is: {predicted_department} (Confidence: {confidence:.2f})")
