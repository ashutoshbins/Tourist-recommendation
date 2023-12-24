# Import necessary libraries
from flask import Flask, render_template, request
import pickle
import pandas as pd
import random

# Load the saved files
df = pd.read_csv('D:\Projects\Tourist Recommendation with NLM\Data.csv')

def get_random_names(description, num_names=3):
    description_lower = description.lower().strip()
    matching_rows = df[df['P1'].str.lower().str.strip()== description_lower]
    
    if len(matching_rows) == 0:
        return [f"No names found with the description: {description}"]

    selected_names = random.sample(matching_rows['Place'].tolist(), min(num_names, len(matching_rows)))
    return selected_names

with open('D:\Projects\Tourist Recommendation with NLM\cv.pkl', 'rb') as file:
    cv = pickle.load(file)

with open('D:\Projects\Tourist Recommendation with NLM\model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('D:\Projects\Tourist Recommendation with NLM\encoder.pkl', 'rb') as file:
    encoder= pickle.load(file)

# Initialize Flask app
app = Flask(__name__)

# Define route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define route for handling the form submission
@app.route('/submit_note', methods=['POST'])
def predict():
    # Get input from the HTML form
    inp = request.form['note']

    # Transform the input using the loaded CountVectorizer
    inp = [inp]
    inn = cv.transform(inp).toarray()

    # Make prediction using the loaded model
    result = encoder.inverse_transform(model.predict(inn))
    result = result[0]
    
    # Get random names based on the predicted category (case-insensitive)
    names =[result.capitalize()]+get_random_names(result, num_names=7)
    # Render the result on the result.html page

    return render_template('result.html', result=names)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
