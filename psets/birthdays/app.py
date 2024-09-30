import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

# global variable for editing an entry?
selected_id = None


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/add_entry", methods=["POST"])
def add_entry():
    name = request.form.get("name")
    month = request.form.get("month")
    day = request.form.get("day")

    if name and month and day:
        db.execute(
            """
            INSERT INTO birthdays
            (name, month, day)VALUES (?, ?, ?)
            """,
            name,
            month,
            day
        )

    return redirect("/")


@app.route("/open_entry", methods=["GET", "POST"])
def open_entry():
    if request.method == "POST":
        selected_id = request.form.get("id")
        return redirect("/open_entry")

    return render_template("index.html", birthdays=db.execute("SELECT * FROM birthdays"), selected_id=selected_id)



@app.route("/update_entry", methods=["POST"])
def update_entry():

    update_id = request.form.get("id")
    name = request.form.get("name")
    month = request.form.get("month")
    day = request.form.get("day")

    if update_id and name and month and day:
        db.execute(
            """
            UPDATE birthdays
            SET name = ?, month = ?, day = ?
            WHERE id = ?
            """,
            name,
            month,
            day,
            update_id
        )

    return redirect("/")


@app.route("/remove_entry", methods=["POST"])
def remove_entry():

    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM birthdays WHERE id = ?", id)

    return redirect("/")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", birthdays=db.execute("SELECT * FROM birthdays"))

