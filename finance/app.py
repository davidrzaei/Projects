import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import logging

from helpers import apology, login_required, lookup, usd

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

# Configure logging
logging.basicConfig(level=logging.DEBUG)


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
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Retrieve the user's transactions
    transactions = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]

    # Prepare a list to store the user's holdings
    holdings = []

    total_value = 0

    for transaction in transactions:
        symbol = transaction["symbol"]
        shares = transaction["shares"]
        stock = lookup(symbol)
        total = shares * stock["price"]
        holdings.append({
            "symbol": symbol,
            "name": stock["name"],
            "shares": shares,
            "price": usd(stock["price"]),
            "total": usd(total)
        })
        total_value += total

    # Add the user's cash to the total value
    total_value += cash

    return render_template("index.html", holdings=holdings, cash=usd(cash), total_value=usd(total_value))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Please Enter Stock Symbol")

        stock = lookup(symbol.upper())

        if stock is None:
            return apology("Stock Symbol Not Found")

        # Validate shares input
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("Shares must be a positive number")
        except ValueError:
            return apology("Shares must be a numeric value")

        transaction_value = shares * stock["price"]

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        if user_cash < transaction_value:
            return apology("Not Enough Funding Available")

        uptd_cash = user_cash - transaction_value

        db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, user_id)

        date = datetime.datetime.now()

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], shares, stock["price"], date)

        flash("Shares Acquired")

        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions_db = db.execute("SELECT * FROM transactions WHERE user_id = :id", id=user_id)
    return render_template("history.html", transactions=transactions_db)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

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
    if request.method == "GET":
        return render_template("quote.html")

    else:
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Please Enter Stock Symbol")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Stock Symbol Not Found")

        return render_template("quoted.html", name=stock["symbol"], price=stock["price"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    logging.debug("Entering register route")

    if request.method == "GET":
        logging.debug("GET request for register page")
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        logging.debug(f"POST request: username={username}, password={
                      password}, confirmation={confirmation}")

        if not username:
            logging.error("No username provided")
            return apology("A Username is Required")
        if not password:
            logging.error("No password provided")
            return apology("A Password is Required")
        if not confirmation:
            logging.error("No password confirmation provided")
            return apology("Please Confirm Your Password")
        if password != confirmation:
            logging.error("Passwords do not match")
            return apology("Passwords Are Not Identical")

        # Generate password hash
        hash = generate_password_hash(password)

        try:
            # Insert new user into the database
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except ValueError as e:
            # Check if the error is due to the UNIQUE constraint
            if "UNIQUE constraint failed: users.username" in str(e):
                logging.error("Username is already taken")
                return apology("Username is Already Taken")
            else:
                logging.error(f"Unexpected error: {e}")
                return apology("An unexpected error occurred")

        # Query database for the new user's ID
        rows = db.execute("SELECT id FROM users WHERE username = ?", username)
        if len(rows) != 1:
            logging.error("User registration failed, user not found after insert")
            return apology("User registration failed")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        logging.debug("User registered and logged in successfully")

        # Redirect to home page
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_user = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = :id GROUP BY symbol HAVING SUM(shares) > 0", id=user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in symbols_user])

    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("Please Enter Stock Symbol")

        stock = lookup(symbol.upper())

        if stock is None:
            return apology("Stock Symbol Not Found")

        if shares <= 0:
            return apology("Shares Not Available")

        # Calculate the transaction value for selling
        transaction_value = shares * stock["price"]

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        # Retrieve the user's current shares of the stock
        user_shares = db.execute(
            "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)
        user_shares_real = user_shares[0]["total_shares"]

        if shares > user_shares_real:
            return apology("Not Enough Shares to Sell")

        # Calculate the updated cash balance after selling
        updated_cash = user_cash + transaction_value

        # Update the user's cash balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

        # Record the transaction of selling shares
        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   user_id, symbol, -shares, stock["price"], date)

        flash("Shares Sold Successfully")

        return redirect("/")
