from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Хранилище событий (в реальном проекте используйте БД)
events = []
registrations = []

@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(events)

@app.route('/api/events', methods=['POST'])
def create_event():
    event = request.json
    event['id'] = len(events) + 1
    event['created_at'] = datetime.now().isoformat()
    events.append(event)
    return jsonify(event), 201

@app.route('/api/events/<int:event_id>/register', methods=['POST'])
def register_for_event(event_id):
    registration = request.json
    registration['event_id'] = event_id
    registration['id'] = len(registrations) + 1
    registration['registered_at'] = datetime.now().isoformat()
    registrations.append(registration)
    return jsonify(registration), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)