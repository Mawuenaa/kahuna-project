# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for
import random
import csv
from collections import Counter
from flask import session
import hashlib
import secrets

# Create a Flask web application
app = Flask(__name__)
from flask import session
import hashlib

app.secret_key = secrets.token_hex(16)  # 16 bytes (128 bits) for a secure key
# Define a route to display the registration page
@app.route('/register', methods=['GET'])
def registration():
    return render_template('registration.html')

# Define a route to handle user registration
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Check if the username is already taken (you can implement this logic)
    # If username is not taken, you can hash the password for security
    

    # Store the username and hashed password in a database or user data file

    # For this example, you can use a simple session variable to store the username
    session['username'] = username

    # Redirect the user to the main game page or any other page you prefer
    return redirect(url_for('index'))

    
# Define the main route for the web applica
# Initialize game variables
current_problem = None
score = 0
attempts = 0
max_attempts = 10
user_data = []
correct_answer = 0  # Initialize with a placeholder value
                                # Add more entries as needed
# Function to generate a random math problem
import time
def generate_problem():
    global current_problem, correct_answer  # Declare correct_answer as global
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(["+", "-", "*", "/"])
    if operator == "/" and num1 % num2 != 0:
        num1 = num2 * random.randint(1, 5)
    current_problem = f"{num1} {operator} {num2}"
    correct_answer = eval(current_problem)  # Assign correct_answer here
    return current_problem, correct_answer

# Function to save user data to a CSV file
def save_user_data(user_data):
    with open('user_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Problem', 'User Answer', 'Correct Answer'])
        for data in user_data:
            writer.writerow([data['problem'], data['user_answer'], data['correct_answer']])

# Function to load user data from a CSV file
def load_user_data(file_name):
    user_data = []
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            problem, user_answer, correct_answer = row
            user_data.append({
                'problem': problem,
                'user_answer': float(user_answer),
                'correct_answer': float(correct_answer)
            })
    return user_data

# Function to analyze user performance
def analyze_user_data(user_data):
    total_attempts = len(user_data)
    correct_attempts = sum(1 for data in user_data if data['user_answer'] == data['correct_answer'])
    success_rate = (correct_attempts / total_attempts) * 100 if total_attempts > 0 else 0

    answer_differences = [abs(data['user_answer'] - data['correct_answer']) for data in user_data]
    average_difference = sum(answer_differences) / total_attempts if total_attempts > 0 else 0

    problems_counter = Counter(data['problem'] for data in user_data)

    return {
        'total_attempts': total_attempts,
        'correct_attempts': correct_attempts,
        'success_rate': success_rate,
        'average_difference': average_difference,
        'problems_counter': problems_counter
    }

# Initialize the first problem
current_problem, correct_answer = generate_problem()



# ...

# Define the main route for the web application
@app.route('/')
def index():
    return render_template('index.html', current_problem=current_problem, score=score, attempts=attempts)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    global current_problem, score, attempts, user_data, correct_answer
    user_answer = float(request.form['user_answer'])
    user_data.append({
        'problem': current_problem,
        'user_answer': user_answer,
        'correct_answer': correct_answer
    })
    if user_answer == correct_answer:
        score += 1
    attempts += 1
    if attempts < max_attempts:
        current_problem, correct_answer = generate_problem()
    else:
        save_user_data(user_data)  # Save user data to a CSV file here
        return redirect(url_for('result'))
    return redirect(url_for('index'))

@app.route('/result')
def result():
    return render_template('result.html', score=score, attempts=attempts)

# Define a route to view user statistics
@app.route('/view_stats')
def view_stats():
    user_data = load_user_data('user_data.csv')
    analysis_results = analyze_user_data(user_data)
    return render_template('stats.html', analysis_results=analysis_results)

@app.route('/')
def default():
    return redirect(url_for('registration'))



if __name__ == '__main__':
    app.run(debug=True)
