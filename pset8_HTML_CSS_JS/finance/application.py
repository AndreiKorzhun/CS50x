import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    current_stocks = db.execute("SELECT symbol FROM purchases WHERE user_id = :id GROUP BY symbol",
                                id=user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
    total = cash[0]["cash"]
    if current_stocks != []:
        storages = list()
        for symbol in current_stocks:
            stock_data = lookup(symbol["symbol"])
            current_price = stock_data["price"]
            stock_info = dict()
            shares_info = db.execute("SELECT SUM(shares) AS shares_sum FROM purchases WHERE user_id = :id\
                                    GROUP BY symbol HAVING symbol = :symbol",
                                     id=user_id, symbol=symbol["symbol"])
            current_shares = shares_info[0]["shares_sum"]
            if current_shares > 0:
                stock_info["symbol"] = symbol["symbol"]
                stock_info["name"] = stock_data["name"]
                stock_info["price"] = usd(current_price)
                stock_info["shares"] = current_shares
                cost = current_price * current_shares
                total += cost
                stock_info["total"] = usd(cost)
                storages.append(stock_info)
        return render_template("index.html", storages=storages, cash=usd(cash[0]["cash"]), total=usd(total))
    else:
        return render_template("index.html", cash=usd(cash[0]["cash"]), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # id user session
    user_id = session["user_id"]

    # User reached route via GET
    if request.method == "GET":
        return render_template("buy.html")

    # User reached route via POST
    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Make sure the character is entered correctly
        if not symbol:
            return apology("incorrect symbol")

        # Checks if a company with this symbol exists
        quote = lookup(symbol)
        if not quote:
            return apology("symbol doesn't exist")

        # Shares must be positive integers
        if shares.isdigit() == False:
            return apology("enter the number")
        else:
            if int(shares) < 1:
                return redirect("/")

        # Share price
        price = quote["price"]

        # How much cash the user currently
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)[0]['cash']

        # Calculate total price based on number of shares and stock's current price
        total_price = int(shares) * price

        # Not enough money to buy shares
        if cash < total_price:
            return apology("insufficient funds")

        # Inserts purchase information into the database
        db.execute("INSERT INTO purchases(user_id, symbol, name, shares, price, data) VALUES (:user_id, :symbol, :name, :shares, :price, :data)",
                   user_id=user_id,
                   symbol=symbol,
                   name=quote["name"],
                   shares=int(shares),
                   price=price,
                   data=datetime.now())

        # updates cash after purchase
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=cash-total_price, id=user_id)
        return redirect("/")


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    purchases = db.execute("SELECT * FROM purchases WHERE user_id = :id", id=user_id)
    for stock in purchases:
        stock["price"] = usd(stock["price"])
    return render_template("history.html", purchases=purchases)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    # User reached route via GET
    if request.method == "GET":
        return render_template("quote.html")

    # User reached route via POST
    else:
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("must provide symbol")
        return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])


@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via GET
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username and password ere submitted
        if not username or not password or not confirmation:
            return apology("must provide username and password")

        # Ensure Password and Confirm match
        elif password != confirmation:
            return apology("Password and Confirm password do not match")

        # Query database for username
        rows = db.execute("SELECT username FROM users WHERE username = :username",
                          username=username)

        # Ensure username exists
        if len(rows) != 0:
            return apology("Username exists")

        # Insert the new user into table users
        db.execute("INSERT INTO users(username, hash) VALUES (:username, :hash)",
                   username=username,
                   hash=generate_password_hash(password))

        return redirect("/login")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # id user session
    user_id = session["user_id"]

    # User reached route via GET
    if request.method == "GET":

        # Shares owned by the user
        current_stocks = db.execute(
            "SELECT symbol FROM purchases WHERE user_id = :id GROUP BY symbol HAVING SUM(shares) > 0", id=user_id)
        return render_template("sell.html", current_stocks=current_stocks)

    # User reached route via POST
    else:

        # Assign inputs to variables
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Choose symbol
        if not symbol:
            return apology("choose symbol")

        # Ensure user entered a positive integer for number of shares
        if int(shares) <= 0:
            return apology("number of shares must be a positive integer")

        # Query database for user's purchases
        stock = db.execute("SELECT SUM(shares) as shares FROM purchases WHERE user_id = :id AND symbol = :symbol",
                           id=user_id, symbol=symbol)

        # Ensure user has enough shares for selected symbol
        if stock[0]["shares"] < int(shares):
            return apology("not enough shares")

        # Query database to insert transaction
        db.execute("INSERT INTO purchases (user_id, symbol, name, shares, price, data) VALUES (:id, :symbol, :name, :shares, :price, :data)",
                   id=user_id,
                   symbol=symbol,
                   name=lookup(symbol)["name"],
                   shares=int(shares) * (-1),
                   price=lookup(symbol)["price"],
                   data=datetime.now())

        # Calculate total price based on number of shares and stock's current price
        total_price = lookup(symbol)["price"] * int(shares)

        # How much cash the user currently
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)[0]["cash"]

        # Query database to update user's cash balance
        db.execute("UPDATE users SET cash = :cash WHERE id = :id",
                   id=user_id,
                   cash=cash + total_price)

        # Redirect user to homepage
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
