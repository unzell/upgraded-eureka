import os
import sqlite3
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///notes.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def make():
    if request.method == "POST":

        name = request.form.get("name")
        if not name:
            return redirect("/")

        note = request.form.get("note")
        if not note:
            return redirect("/")

        db.execute("INSERT INTO notes (name, note) VALUES(?, ?)", name, note)

        return redirect("/")


    else:

        notes = db.execute("SELECT * FROM notes")
    return render_template("make.html", notes = notes)


@app.route('/delete_row/<int:row_id>', methods=['DELETE'])
def delete_row(row_id):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Notes WHERE id = ?", (row_id,))
    conn.commit()
    conn.close()

@app.route('/delete', methods=['POST'])
def delete():
    print("Delete route hit")  # Debugging line
    data = request.get_json()
    print(data)  # Debugging line
    id = data['id']
    print(f"ID to delete: {id}")  # Debugging line
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM Notes WHERE id = ?", (id,))
        conn.commit()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))
    finally:
        conn.close()

if __name__ == '__main__':
    app.run()
