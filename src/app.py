import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import logging
from sklearn.exceptions import NotFittedError

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)


try:
    with open('../naive_bayes_model.pkl', 'rb') as f:
        model, vectorizer = pickle.load(f)
except (FileNotFoundError, pickle.UnpicklingError) as e:
    model = None
    vectorizer = None
    logging.error(f"Error loading model and vectorizer: {e}")

# Define a helper function to validate input
def validate_input(data):
    if not isinstance(data, dict):
        return False, "Input data should be in JSON format"

    title = data.get('title')
    text = data.get('text')

    if not title or not isinstance(title, str):
        return False, "Title field is required and should be a string"
    if not text or not isinstance(text, str):
        return False, "Text field is required and should be a string"

    return True, None

@app.route('/predict', methods=['POST'])
def predict():
    # Check if the model and vectorizer are loaded
    if model is None or vectorizer is None:
        return jsonify({'error': 'Model or vectorizer not loaded properly. Please check server logs.'}), 500

    data = request.get_json()

    # Validate the input data
    is_valid, error_message = validate_input(data)
    if not is_valid:
        return jsonify({'error': error_message}), 400

    title = data.get('title', '')
    text = data.get('text', '')

    # Combine title and text for prediction
    combined_text = f"{title} {text}"

    try:
        # Transform the combined text using the vectorizer
        combined_text_tfidf = vectorizer.transform([combined_text])

        # Predict using the model
        prediction = model.predict(combined_text_tfidf)[0]
        result = 'Fake News' if prediction == 1 else 'Real News'

        # Return the result as JSON
        return jsonify({'prediction': result})

    except NotFittedError:
        logging.error("The model or vectorizer is not fitted. Please check model training.")
        return jsonify({'error': 'Model or vectorizer not fitted properly. Please contact support.'}), 500
    except Exception as e:
        # Handle unexpected errors during prediction
        logging.error(f"An error occurred during prediction: {e}")
        return jsonify({'error': 'An internal error occurred during prediction.'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
