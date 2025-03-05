from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please configure your database.")

# Database Connection
try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
except psycopg2.OperationalError as e:
    print(f"Database connection error: {e}")
    conn, cursor = None, None

@app.route('/submit-form', methods=['POST'])
def submit_form():
    if not conn or not cursor:
        return jsonify({"error": "Database connection not available"}), 500

    data = request.json
    try:
        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (data['name'], data['email'], data['message'])
        )
        conn.commit()
        return jsonify({"message": "Form submitted successfully!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Check if the server is running."""
    return jsonify({"status": "OK"}), 200

@app.teardown_appcontext
def close_connection(exception):
    """Close database connection when the app shuts down."""
    if cursor:
        cursor.close()
    if conn:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
