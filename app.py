from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)


# Database create/connect
def init_db():
    conn = sqlite3.connect("to_do.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS todo (
            SNO INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            desc TEXT NOT NULL,
            date_created TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


# Home page
@app.route("/")
def hi():
    conn = sqlite3.connect("to_do.db")

    todos = conn.execute(
        "SELECT * FROM todo ORDER BY SNO DESC"
    ).fetchall()

    conn.close()

    return render_template("index.html", todos=todos)


# Add task
@app.route("/add", methods=["POST"])
def add_todo():
    title = request.form["title"]
    desc = request.form["desc"]

    date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("to_do.db")

    conn.execute(
        "INSERT INTO todo (title, desc, date_created) VALUES (?, ?, ?)",
        (title, desc, date_created)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("hi"))


# Delete task
@app.route("/delete/<int:sno>", methods=["POST"])
def delete_todo(sno):
    conn = sqlite3.connect("to_do.db")

    conn.execute(
        "DELETE FROM todo WHERE SNO = ?",
        (sno,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("hi"))


# Run Flask
if __name__ == "__main__":
    app.run(debug=True)

    
