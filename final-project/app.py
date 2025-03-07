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


# Configure logging
logging.basicConfig(level=logging.DEBUG)

todos = []

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        todo = request.form.get("todo")
        if todo:
            todos.append(todo)
    return render_template("index.html", todos=todos)


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
        confirmation = request.form.get("confirm_password")

        logging.debug(f"POST request: username={username}, password={password}, confirmation={confirmation}")

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
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
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
