import os
from tempfile import mkdtemp

from cs50 import SQL
# from flask_sqlalchemy import SQLAlchemy
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from flask_session import Session
from werkzeug.exceptions import (HTTPException, InternalServerError,
                                 default_exceptions)
from werkzeug.security import check_password_hash, generate_password_hash

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
    """Show portfolio of stocks"""
    sql_query = db.execute(
        "SELECT symbol, SUM(amount), time FROM purchases WHERE buyerId=:id GROUP BY symbol;",
        id=session["user_id"])

    rows = list()
    total = 0
    for line in sql_query:
        symbol = lookup(line['symbol'])
        line['value'] = symbol['price']
        line['shares'] = line.pop('SUM(amount)')
        rows.append(line)
        total += symbol['price'] * line['shares']

    user = db.execute(
        "SELECT cash FROM users WHERE id=:id;",
        id=session["user_id"])
    
    return render_template('index.html', rows=rows, total=total, balance=float(user[0]['cash']))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # if user reached via POST
    if request.method == 'POST':
        # get symbol and amount of shares
        symbol = lookup(request.form.get('symbol'))
        shares = int(request.form.get('shares'))

        # error checking
        if not symbol:
            return apology("Invalid symbol")
        if not shares or shares < 1:
            return apology("Invalid amount") 
        
        # transaction to ensure no race condition
        # db.execute("BEGIN TRANSACTION;")
        print('transaction begun')

        balances = db.execute(
            "SELECT cash FROM users WHERE id = :id;",
            id=session["user_id"])

        balance = balances[0]['cash']

        value = shares * symbol['price']

        # check that user has enough balance
        if balance < value:
            # db.execute("ROLLBACK;")
            return apology("Not enough balance.")

        # update balance
        balance -= value
        db.execute(
            "UPDATE users SET cash = :balance WHERE id = :id;",
            balance=balance,
            id=session["user_id"])

        db.execute(
            "INSERT INTO purchases ('buyerId','symbol','value','amount','time') VALUES (:buyer_id,:symbol,:value,:amount,datetime('now', 'localtime'));",
            buyer_id=session["user_id"],
            symbol=symbol['symbol'],
            value=value,
            amount=shares)

        # db.execute("COMMIT;")

        return redirect(url_for('index'))

    return render_template('buy.html')


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


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
        rows = db.execute("SELECT * FROM users WHERE username = :username;",
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
    """Get stock quote."""
    if request.method == 'POST':
        quote_val = lookup(request.form.get('q'))
        return render_template('quote.html', quote_val=quote_val)

    return render_template('quote.html', quote_val=None)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # if user reached via POST 
    if request.method == 'POST':
        # check if he provided a username
        if not request.form.get('username'):
            return apology("You must provide a username")
        # check if he provided a password and a confirmation
        if not request.form.get('password') or not request.form.get('confirmation'):
            return apology("You must provide a password")
        # check if password and confirmation match
        if not request.form.get('password') == request.form.get('confirmation'):
            flash("Your passwords don't match")
            return redirect(url_for('register'))
            
        # query the database for the same username
        existing_user = db.execute("SELECT username FROM users WHERE username = :username;",
                                    username=request.form.get('username'))

        # if username does not exist in the database
        if len(existing_user) == 0:
            # add a new user with the information from the form
            db.execute(
                "INSERT INTO users ('username','hash') VALUES (:username,:hash);",
                username=request.form.get('username'),
                hash=generate_password_hash(request.form.get('password')) )
            
            user_id = db.execute(
                "SELECT id FROM users WHERE username = :username;",
                username=request.form.get('username'))
            session["user_id"] = user_id[0]["id"]
            return redirect(url_for('index'))

        else:
            flash("That username is already taken")
            return redirect(url_for('register'))

    # if user reached via GET, render the template
    return render_template('register.html')



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        shares = int(request.form.get('shares'))

        if not symbol:
            return apology('invalid symbol')    
        if not shares:
            return apology('invalid number')

        available_shares = db.execute(
            "SELECT SUM(amount) FROM purchases WHERE buyerId=:id AND symbol=:symbol GROUP BY symbol;",
            id=session["user_id"],
            symbol=symbol)

        if len(available_shares) > 0 and shares > available_shares[0]['SUM(amount)']:
            return apology("You don't have enough shares")

        curr_value = lookup(symbol)['price']

        db.execute(
            "INSERT INTO purchases ('buyerId','symbol','value','amount','time') VALUES (:id,:symbol,:value,:amount,datetime('now', 'localtime'));",
            id=session["user_id"],
            symbol=symbol,
            value=(-curr_value),
            amount=(-shares))

        db.execute(
            "UPDATE users SET cash = cash + :price WHERE Id = :id;",
            id=session["user_id"],
            price=(curr_value * shares))

        return redirect(url_for('index'))

    symbols = db.execute(
        "SELECT symbol FROM purchases WHERE buyerId=:id GROUP BY symbol;",
        id=session["user_id"])

    return render_template('sell.html', symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
