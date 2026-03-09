from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = "users.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            city TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return jsonify({"message": "Flask User Management API is running"})


@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()

    user_list = [dict(user) for user in users]
    return jsonify(user_list)


@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    city = data.get("city")

    if not name or not email or not phone or not city:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (name, email, phone, city) VALUES (?, ?, ?, ?)",
        (name, email, phone, city)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "User added successfully"}), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    city = data.get("city")

    if not name or not email or not phone or not city:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    if user is None:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    conn.execute(
        "UPDATE users SET name = ?, email = ?, phone = ?, city = ? WHERE id = ?",
        (name, email, phone, city, user_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "User updated successfully"})


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    if user is None:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "User deleted successfully"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)