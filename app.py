from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database Connection
DATABASE_URL = "postgresql://portfolio_6srh_user:cSKL3poBM1FOztdfD6akqQZK1PUBLLL9@dpg-cv3r699u0jms73ecktr0-a/portfolio_6srh"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("Database connection successful!")
except Exception as e:
    print(f"Error connecting to the database: {e}")

@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.json
    
    if not all(key in data for key in ['name', 'email', 'message']):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        cursor.execute("INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)", 
                       (data['name'], data['email'], data['message']))
        conn.commit()
        return jsonify({"message": "Form submitted successfully!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Database error: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
