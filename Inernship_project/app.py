from flask import Flask, render_template, request, redirect, url_for
import datetime
import csv

app = Flask(__name__)


@app.route('/')
def home():
    # Generate the current date and time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Pass the dynamic content to the template
    return render_template('index.html', current_time=current_time)


def submit_form():
    if request.method == 'POST':
        # Get the data submitted in the form
        name = request.form.get('name')
        email = request.form.get('email')

        # Redirect to the response page with query parameters
        return redirect(url_for('response', name=name, email=email))


# Define a route for the response page
@app.route('/response')
def response():
    # Get the submitted data from query parameters
    name = request.args.get('name')
    email = request.args.get('email')

    # Render the response template with the submitted data
    return render_template('response.html', name=name, email=email)


# Define the path to the text file for storing form submissions
SUBMISSIONS_FILE = 'submissions.txt'


# Existing routes...

# Define a route to handle form submissions
@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Get the data submitted in the form
        name = request.form.get('name')
        email = request.form.get('email')

        # Store the form data in the text file
        with open(SUBMISSIONS_FILE, 'a', newline='') as file:
            writer = csv.writer(file, delimiter='\t')  # Use tab as the delimiter
            writer.writerow([name, email])

        # Redirect to a page that displays a success message
        return redirect(url_for('submission_success'))


# Define a route to display a success message
@app.route('/success')
def submission_success():
    return render_template('success.html')


# Define a route to display stored form submissions
@app.route('/submissions')
def display_submissions():
    submissions = []
    with open(SUBMISSIONS_FILE, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            submissions.append({'name': row[0], 'email': row[1]})

    return render_template('submissions.html', submissions=submissions)


if __name__ == '__main__':
    app.run(debug=True)
