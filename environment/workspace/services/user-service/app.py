"""User Service - Manages user accounts and authentication."""
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# In-memory user store
users = {}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "user-service"}), 200

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """Get all users."""
    return jsonify({"users": list(users.values())}), 200

@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID."""
    if user_id in users:
        return jsonify(users[user_id]), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json()
    user_id = data.get('id')
    users[user_id] = data
    return jsonify(data), 201

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)