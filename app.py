from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Database Connection
conn = psycopg2.connect("postgres://your_database_url")
cursor = conn.cursor()

@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.json
    cursor.execute("INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)", 
                   (data['name'], data['email'], data['message']))
    conn.commit()
    return jsonify({"message": "Form submitted successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
