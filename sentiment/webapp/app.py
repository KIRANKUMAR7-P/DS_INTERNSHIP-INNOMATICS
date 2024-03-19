from flask import Flask, render_template, request
from joblib import load
import pandas as pd
import os

app = Flask(__name__)

# Load machine learning models
bow_model = load(r'C:\Users\pamar\Desktop\Ds internship\backend\sentiment\webapp\model\Logistic Regression.pkl')
tfidf_model = load(r'C:\Users\pamar\Desktop\Ds internship\backend\sentiment\webapp\model\Logistic Regression (TF-IDF).pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict_review', methods=['POST'])
def predict_review():
    review = request.form['review']
    algorithm = request.form['algorithm']

    if algorithm == 'bow':
        prediction = bow_model.predict([review])[0]
    elif algorithm == 'tfidf':
        prediction = tfidf_model.predict([review])[0]
    else:
        prediction = 'Invalid algorithm selection'

    return render_template('results.html', review_text=review, review_algorithm=algorithm, review_prediction=prediction)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    algorithm = request.form['algorithm']

    if file.filename.endswith(('csv', 'xlsx')):
        df = pd.read_csv(file) if file.filename.endswith('csv') else pd.read_excel(file)

        if algorithm == 'bow':
            df['Prediction (BoW)'] = bow_model.predict(df['Review'])  # Assuming 'Review' is the column name
        elif algorithm == 'tfidf':
            df['Prediction (TF-IDF)'] = tfidf_model.predict(df['Review'])  # Assuming 'Review' is the column name
        else:
            return "Invalid algorithm selection"

        file_predictions = df.to_dict(orient='records')

        return render_template('results.html', file_predictions=file_predictions, algorithm=algorithm)
    else:
        return "Unsupported file format. Please upload a CSV or Excel file."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
