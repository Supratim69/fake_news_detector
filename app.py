from flask import Flask, request, jsonify
import pickle

with open('naive_bayes_model.pkl', 'rb') as f:
    model, vectorizer = pickle.load(f)

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    title = data.get('title', '')
    text = data.get('text', '')

    if not title or not text:
        return jsonify({'error': 'Both title and text fields are required'}), 400

    combined_text = f"{title} {text}"

    combined_text_tfidf = vectorizer.transform([combined_text])

    prediction = model.predict(combined_text_tfidf)[0]
    result = 'Fake News' if prediction == 1 else 'Real News'

    # Return the result as JSON
    return jsonify({'prediction': result})


if __name__ == '__main__':
    app.run(debug=True)
