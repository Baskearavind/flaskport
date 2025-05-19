import os
from datetime import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB connection URI from environment variable
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise ValueError("No MONGO_URI found. Please set it in your .env file.")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['portfolio_db']  # Database name
contacts_collection = db['contacts']  # Collection for contact messages

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    # Load projects data from JSON file
    import json
    with open('data/projects.json') as f:
        projects_data = json.load(f)
    return render_template('projects.html', projects=projects_data)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    success = False
    error = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            error = "Please fill in all the fields."
        else:
            contact_doc = {
                "name": name,
                "email": email,
                "message": message,
                "timestamp": datetime.utcnow()
            }
            try:
                contacts_collection.insert_one(contact_doc)
                success = True
            except Exception as e:
                error = f"An error occurred while saving your message: {e}"

    return render_template('contact.html', success=success, error=error)

# Optional: inject current year in templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

if __name__ == '__main__':
    app.run(debug=True)
