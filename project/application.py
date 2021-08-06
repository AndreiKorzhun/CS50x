from flask import Flask, render_template, redirect, request, session, flash, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3


# Configure app
app = Flask(__name__)


def connect_db():
    """ Connect to database """

    connect = sqlite3.connect("project.db")
    connect.row_factory = sqlite3.Row
    print("Successfully Connected to SQLite")
    return connect


# Create database
db = connect_db()
sql = db.cursor()

# Create tables
sql.execute("""CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT,
               email TEXT,
               password TEXT)
            """)
sql.execute("""CREATE TABLE IF NOT EXISTS tasks (
               task_id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER,
               task TEXT,
               status BIT default('false'),
               FOREIGN KEY(user_id) REFERENCES users(id))
            """)
db.commit()
print("SQLite table created")
db.close()

# Configure sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    """ Main page """

    # User isn't logged in
    if not session.get("user_id"):
        return redirect("/login")

    with connect_db() as db:
        sql = db.cursor()
        # Get all user tasks that haven't been completed
        sql.execute(
            "SELECT * FROM tasks \
            WHERE user_id = ? AND status='false' \
            ORDER BY task DESC",
            [session["user_id"]])
        current_tasks = sql.fetchall()

        # Get all user tasks that have been completed
        sql.execute(
            "SELECT * FROM tasks \
            WHERE user_id = ? AND status='true' \
            ORDER BY task DESC",
            [session["user_id"]])
        completed_tasks = sql.fetchall()

    return render_template("index.html", current_tasks=current_tasks,
                               completed_tasks=completed_tasks)


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    try:
        with connect_db() as db:
            sql = db.cursor()
            # Change the status of the task to "completed"
            sql.execute("UPDATE tasks SET status = 'true' WHERE task_id = ?", [task_id])
            db.commit()
    except:
        print("Error in update operation")
        db.rollback()
    finally:
        db.close()
        return redirect("/")


@app.route("/incomplete/<int:task_id>", methods=["POST"])
def incomplete(task_id):
    try:
        with connect_db() as db:
            sql = db.cursor()
            # Change the status of the task to "incompleted"
            sql.execute("UPDATE tasks SET status = 'false' WHERE task_id = ?", [task_id])
            db.commit()
    except:
        print("Error in update operation")
        db.rollback()
    finally:
        db.close()
        return redirect("/")


@app.route("/add", methods=["GET", "POST"])
def add():
    """ Add task """

    # POST
    if request.method == "POST":
        task = request.form.get("task")

        try:
            with connect_db() as db:
                sql = db.cursor()
                # Insert the task in the database that the user entered in "input"
                sql.execute("INSERT INTO tasks(user_id, task) VALUES (?, ?)",
                            (session["user_id"], task[0].upper() + task[1:]))
                db.commit()

        except:
            print("Error in insert operation")
            db.rollback()
        finally:
            db.close()
            return redirect("/")

    # GET
    return render_template("add.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # POST
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        with connect_db() as db:
            sql = db.cursor()
            # Query database for email
            sql.execute("SELECT * FROM users WHERE email = ?", [email])
            user = sql.fetchall()

            # Ensure username exists and password is correct
            if len(user) == 1 and \
                    check_password_hash(user[0]["password"], password):

                # Remember which user has logged in
                session["user_id"] = user[0]["id"]

                return redirect("/")
            else:
                flash("Email Address or Password entered incorrectly", "error")

    # GET
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # POST
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            with connect_db() as db:
                sql = db.cursor()
                # Query database for email
                sql.execute("SELECT email FROM users WHERE email = ?", [email])

                # Make sure email doesn't exist in the database
                if sql.fetchone() is None:
                    # Insert the new user into table users
                    sql.execute(
                        "INSERT INTO users(username, email, password) VALUES (?, ?, ?)",
                        (name, email, generate_password_hash(password)))
                    db.commit()

                    # User id
                    sql.execute("SELECT id FROM users WHERE email = ?", [email])
                    user_id = sql.fetchone()

                    # Remember which user register
                    session["user_id"] = user_id[0]

                    return redirect("/")
                else:
                    flash("Email Address already exists", "error")

        except:
            print("Error in insert operation")
            db.rollback()
        finally:
            db.close()

    # GET
    return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    session["user_id"] = None
    return redirect("/")


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    """ Delete task """

    try:
        with connect_db() as db:
            sql = db.cursor()
            # Remove task from database
            sql.execute("DELETE FROM tasks WHERE task_id = ?", [task_id])
            db.commit()
    except:
        print("Error in delete operation")
        db.rollback()
    finally:
        db.close()
        return redirect("/")


if __name__ == "__main__":
    app.run()