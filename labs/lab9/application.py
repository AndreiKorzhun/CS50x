import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Add the user's entry into the database

        # Gets the value entered by the user in the form
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Insert values entered by the user into the database
        db.execute(
            "INSERT INTO birthdays (name, month, day) VALUES (:name, :month, :day)",
            name=name,
            month=month,
            day=day)

        return redirect("/")

    # Method GET
    else:

        # Display the entries in the database on index.html

        # Get all values from the database
        rows = db.execute("SELECT * FROM birthdays")

        return render_template("index.html", rows=rows)


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    db.execute("DELETE FROM birthdays WHERE id = :id", id=id)
    return redirect("/")
