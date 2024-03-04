# app.py
from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    test_string = request.form['test_string']
    regex_pattern = request.form['regex_pattern']
    matches = re.findall(regex_pattern, test_string)
    

    return render_template(
        'results.html',
        test_string=test_string,
        regex_pattern=regex_pattern,
        matches=matches,
        
    )

@app.route('/validate-email', methods=['POST'])
def validate_email():
    email = request.form['email']
    regex_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    is_valid = re.match(regex_pattern, email) is not None
    result_message = "Valid email address." if is_valid else "Invalid email address."
    return jsonify({'email': email, 'is_valid': is_valid, 'result_message': result_message})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
