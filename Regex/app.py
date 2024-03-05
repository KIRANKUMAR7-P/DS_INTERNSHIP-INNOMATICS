# app.py
import re
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Retrieve form data
        test_string = request.form.get("test_string", "")
        regex_pattern = request.form.get("regex", "")

        # Perform regex search
        matches = list(re.finditer(regex_pattern, test_string))

        # Convert matches to strings
        matches = [match.group() for match in matches]

        # Render template with results
        return render_template("index.html", test_string=test_string, regex=regex_pattern, matches=matches)
    else:
        # Render the form template
        return render_template("index.html")

# Define route for email validation form
@app.route("/validate_email", methods=["GET", "POST"])
def validate_email():
    if request.method == 'POST':
        emails = request.form.getlist('email')
        validation_results = []
        for email in emails:
            is_valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
            validation_results.append((email, 'Valid' if is_valid else 'Invalid'))
        return render_template('validate_email.html', validation_results=validation_results)
    return render_template('validate_email.html')

if __name__ == "__main__":
    app.run(debug=True)
