from math import radians, sin, cos, sqrt, atan2
import pickle
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
import os

svm_classifier = None
tfidf_vectorizer = None

def haversine_distance(lat1, lon1, lat2, lon2):

    # Radius of the Earth in km
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance

def closestHospital(connection,accident_latitude,accident_longitude):
    try:
        cursor=connection.cursor()

        query="""
        SELECT * 
        FROM API_HOSPITAL 
        """

        cursor.execute(query)
        hospitals = cursor.fetchall()

        closest_hospital = None
        min_distance = float('inf')

        # Iterate over hospitals and calculate the distance
        for hospital in hospitals:
            hospital_id, hospital_name, hospital_lat, hospital_lon,addr,city,state,pincode,contact = hospital
            # Convert Decimal to float
            hospital_lat = float(hospital_lat)
            hospital_lon = float(hospital_lon)
            # Calculate haversine distance
            distance = haversine_distance(accident_latitude, accident_longitude, hospital_lat, hospital_lon)
            if distance<min_distance:
                closest_hospital=hospital
        
        return {
            'id':hospital[0],
            'name':hospital[1],
            'lat':hospital[2],
            'long':hospital[3],
            'address':hospital[4],
            'city':hospital[5],
            'state':hospital[6],
            'pincode':hospital[7],
            'contact':hospital[8]
        }

            

    except:
        print("An error occured")


def load_model():
    global svm_classifier, tfidf_vectorizer
    # Define base directory for model files
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file

    # Build the full path for the model and vectorizer
    svm_classifier_path = os.path.join(base_dir, 'assets', 'svm_classifier.pkl')
    tfidf_vectorizer_path = os.path.join(base_dir, 'assets', 'tfidf_vectorizer.pkl')
    
    # Load the SVM classifier
    with open(svm_classifier_path, 'rb') as f:
        svm_classifier = pickle.load(f)
    
    # Load the TF-IDF vectorizer
    with open(tfidf_vectorizer_path, 'rb') as f:
        tfidf_vectorizer = pickle.load(f)
    
    print("Model and Vectorizer loaded successfully.")
def predict_department(report):
    # Ensure that the model and vectorizer are loaded
    if svm_classifier is None or tfidf_vectorizer is None:
        load_model()  # Load the model if not already loaded
    
    # Transform the input report using the loaded vectorizer
    report_tfidf = tfidf_vectorizer.transform([report])
    
    # Make a prediction using the loaded SVM classifier
    prediction = svm_classifier.predict(report_tfidf)
    
    # Get the prediction probability (confidence)
    probabilities = svm_classifier.predict_proba(report_tfidf)
    confidence = probabilities.max()  # Highest probability (confidence)
    
    return prediction[0], confidence