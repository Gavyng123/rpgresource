from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from sqlite3 import Error
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/save-data', methods=['POST'])
def save_data():
    try:
        data = request.get_json()
        conn = sqlite3.connect('./../database/sqlite_database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO inventory (itemName, itemQuantity) VALUES (?, ?)", (data['itemName'], data['itemQuantity']))
        conn.commit()
        return jsonify(message='OK', id=cur.lastrowid)  # Return the ID of the inserted item
    except Exception as e:
        app.logger.error(f"Error saving data: {e}")
        return jsonify(error=str(e)), 400

@app.route('/save-spell', methods=['POST'])
def save_spell():
    try:
        data = request.get_json()
        conn = sqlite3.connect('./../database/sqlite_database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO spells (spellName, spellLevel, spellDescription) VALUES (?, ?, ?)", (data['spellName'], data['spellLevel'], data['spellDescription']))
        conn.commit()
        return jsonify(message='OK', id=cur.lastrowid)  # Return the ID of the inserted item
    except Exception as e:
        app.logger.error(f"Error saving data: {e}")
        return jsonify(error=str(e)), 400

@app.route('/get-data', methods=['GET'])
def get_data():
    try:
        conn = sqlite3.connect('./../database/sqlite_database.db')
        cur = conn.cursor()
        cur.execute("SELECT id, itemName, itemQuantity FROM inventory")
        rows = cur.fetchall()

        # Create a dictionary for each row
        data = [{'id': row[0], 'itemName': row[1], 'itemQuantity': row[2]} for row in rows]

        return jsonify(data)
    except Exception as e:
        app.logger.error(f"Error getting data: {e}")
        return jsonify(error=str(e)), 400

@app.route('/delete-data/<int:id>', methods=['DELETE'])
def delete_data(id):
    try:
        conn = sqlite3.connect('./../database/sqlite_database.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM inventory WHERE id = ?", (id,))
        conn.commit()
        return jsonify(message='OK')
    except Exception as e:
        app.logger.error(f"Error deleting data: {e}")
        return jsonify(error=str(e)), 400

def create_table():
    conn = sqlite3.connect('./../database/sqlite_database.db')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            itemName TEXT NOT NULL,
            itemQuantity INTEGER NOT NULL
        )
    """)
    conn.commit()


if __name__ == '__main__':
    create_table()
    app.run(port=5000)