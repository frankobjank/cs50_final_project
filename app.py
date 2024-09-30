import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    def get_portfolio():
        totals = {"cash": 0, "grand_total": 0}
        portfolio = []

        # Combine query for transaction data and user's cash
        from_sql = db.execute(
            """
            SELECT stock, SUM(shares) FROM transactions
             WHERE user_id = ?
                   GROUP BY stock
            """,
            session.get("user_id")
        )

        # Retrieve user's cash from the db
        totals["cash"] = db.execute("SELECT cash from users WHERE id = ?",
                                    session.get("user_id"))[0]["cash"]

        # Add current cash to the grand total
        totals["grand_total"] += totals["cash"]

        # No stocks owned, exit early
        if len(from_sql) == 0:
            # For display purposes (jinja), set portfolio to None
            return None, totals

        for entry in from_sql:

            # Skip stock if SUM(shares) from transactions is 0 (sold as many as bought)
            if entry.get("SUM(shares)") == 0:
                continue

            stock = {"symbol": "", "shares": 0, "price": 0, "total": 0}

            stock["symbol"] = entry.get("stock")
            stock["shares"] = entry.get("SUM(shares)")

            # Check for null values
            if not stock["symbol"] or not stock["shares"]:
                return "data missing"

            # Could maybe get all prices at once to minimize lookup time?
            stock["price"] = lookup(stock["symbol"])["price"]
            stock["total"] = float(stock["shares"]) * stock["price"]

            # Keep running total of all stocks BEFORE rounding
            totals["grand_total"] += stock["total"]

            # Clean up data for display
            stock["price"] = usd(stock["price"])
            stock["total"] = usd(stock["total"])

            # Add stock dict to portfolio list
            portfolio.append(stock)

        return portfolio, totals

    portfolio, totals = get_portfolio()

    return render_template("index.html", portfolio=portfolio, totals=totals)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide a stock symbol")

        # Try to query the db
        lookup_result = lookup(symbol)
        if not lookup_result:
            return apology("invalid stock symbol")

        # Ensure positive integer
        shares = request.form.get("shares")
        try:
            # Tests if positive and if decimal by converting to int
            if int(shares) < 0:
                return apology("enter a positive number")
        except ValueError:
            return apology("enter a whole number")

        # Convert from string to float
        shares = float(shares)

        # Get user's cash from db - comes in as float
        available_cash = db.execute("SELECT cash FROM users WHERE id = ?",
                                    session.get("user_id"))[0]["cash"]

        # Test if user can afford
        if lookup_result["price"] * shares > available_cash:
            return apology("insufficient funds to complete the transaction")

        # Calc new balance
        available_cash -= lookup_result["price"] * shares

        # Remove money from account
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   available_cash, session.get("user_id"))

        # Update database
        db.execute(
            """
            INSERT INTO transactions
            (type, shares, per_share, cost, time, user_id, stock)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            "buy",  # type
            shares,  # number of shares
            lookup_result["price"],  # cost per share
            shares * lookup_result["price"],  # total cost
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # timestamp from python
            session.get("user_id"),  # user_id
            lookup_result["symbol"]  # stock
        )

        flash("Bought!")

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = db.execute(
        """
        SELECT type, shares, per_share, cost, time, stock FROM transactions
         WHERE user_id = ?
        """,
        session.get("user_id")
    )

    for row in history:

        # Make shares positive for "sell" rows
        row["shares"] = abs(row["shares"])

        # For display: Convert to usd
        row["cost"] = usd(row["cost"])
        row["per_share"] = usd(row["per_share"])

        # For display: Convert to Title
        row["type"] = row["type"].title()

    # Set to None so jinja can skip it if it's empty
    if len(history) == 0:
        history = None

    return render_template("history.html", history=history)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide a stock symbol")

        # Try to query the db
        lookup_result = lookup(symbol)
        if not lookup_result:
            return apology("invalid stock symbol")

        lookup_result["price"] = usd(lookup_result["price"])

        return render_template("quoted.html", result=lookup_result)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password matches confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Attempt to register account, check for dupe username
        try:
            # If not dupe, add row to table
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                request.form.get("username"),
                generate_password_hash(request.form.get("password"))
            )

        # Dupe username
        except ValueError:
            return apology("username taken")

        # Redirect user to login
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    """Change password"""

    if request.method == "POST":

        # Ensure old password was submitted
        if not request.form.get("old_password"):
            return apology("must provide password", 400)

        # Ensure new password was submitted
        elif not request.form.get("new_password"):
            return apology("must provide new password", 400)

        # Ensure new password matches confirmation
        elif request.form.get("new_password") != request.form.get("confirmation"):
            return apology("new password and confirmation must match", 400)

        # Query database for password hash
        db_hash = db.execute("SELECT hash FROM users WHERE id = ?",
                             session.get("user_id"))

        if len(db_hash) == 0:
            return apology("error connecting to database", 500)

        # Ensure old password is correct
        if not check_password_hash(
            db_hash[0]["hash"], request.form.get("old_password")
        ):
            return apology("invalid password", 403)

        # Check for dupe password
        if check_password_hash(db_hash[0]["hash"], request.form.get("new_password")):
            return apology("new password cannot match old password", 400)

        # If not dupe, update password hash in table
        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                   generate_password_hash(request.form.get("new_password")),
                   session.get("user_id"))

        flash("Your password has been changed!")

        # Redirect user to home
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_password.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        # Check for stock symbol
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide a stock symbol")

        # Try to query the db
        lookup_result = lookup(symbol)
        if not lookup_result:
            return apology("invalid stock symbol")

        # Ensure positive integer
        shares_to_sell = request.form.get("shares")
        try:
            # Tests if positive and if decimal by converting to int !(from string)!
            if int(shares_to_sell) < 0:
                return apology("enter a positive number")
        except ValueError:
            return apology("enter a whole number")

        # Get number of shares owned from db
        shares_owned = db.execute(
            """
            SELECT SUM(shares) FROM transactions
             WHERE user_id = ?
               AND stock = ?
            """,
            session.get("user_id"),
            symbol
        )[0]["SUM(shares)"]

        # Convert from strings to floats
        shares_to_sell = float(shares_to_sell)
        shares_owned = float(shares_owned)

        # Test if user owns enough shares
        if shares_to_sell > shares_owned:
            return apology("cannot sell more shares than you own")

        # Sale value
        sale_value = lookup_result["price"] * shares_to_sell

        # Get user's cash from db - comes in as float
        cash = db.execute(
            """SELECT cash FROM users
                WHERE id = ?
            """,
            session.get("user_id")
        )[0]["cash"]

        new_balance = sale_value + cash

        # Add money to account
        db.execute(
            """
            UPDATE users SET cash = ?
             WHERE id = ?
            """,
            new_balance,
            session.get("user_id")
        )

        # Update database
        db.execute(
            """
            INSERT INTO transactions
            (type, shares, per_share, cost, time, user_id, stock)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            "sell",  # type
            -shares_to_sell,  # number of shares !! stored as negative for sell !!
            lookup_result["price"],  # cost per share
            shares_to_sell * lookup_result["price"],  # total cost
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # timestamp from python
            session.get("user_id"),  # user_id
            lookup_result["symbol"]  # stock
        )

        flash(f"Sold!")

        return redirect("/")

    else:

        stocks_list_of_dicts = db.execute(
            """
            SELECT stock FROM transactions
             WHERE user_id = ?
                   GROUP BY stock
            """,
            session.get("user_id")
        )

        # Clean up for display
        stocks = [s["stock"] for s in stocks_list_of_dicts]

        return render_template("sell.html", stocks=stocks)
