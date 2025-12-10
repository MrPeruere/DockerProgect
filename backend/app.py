from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'database'),
        database=os.getenv('DB_NAME', 'events_db'),
        user=os.getenv('DB_USER', 'admin'),
        password=os.getenv('DB_PASSWORD', 'admin123'),
        cursor_factory=RealDictCursor
    )
    return conn

@app.route('/api/events', methods=['GET'])
def get_events():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM events ORDER BY event_date')
    events = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(events)

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO events (title, description, event_date, location) VALUES (%s, %s, %s, %s) RETURNING *',
        (data['title'], data['description'], data['event_date'], data['location'])
    )
    event = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(event), 201

@app.route('/api/events/<int:event_id>/register', methods=['POST'])
def register_for_event(event_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO registrations (event_id, participant_name, email) VALUES (%s, %s, %s) RETURNING *',
        (event_id, data['participant_name'], data['email'])
    )
    registration = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(registration), 201

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) as count FROM events')
    events_count = cur.fetchone()['count']
    cur.execute('SELECT COUNT(*) as count FROM registrations')
    registrations_count = cur.fetchone()['count']
    cur.close()
    conn.close()
    return jsonify({'events': events_count, 'registrations': registrations_count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)