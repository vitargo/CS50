import base64
import os

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError, abort
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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user = session.get("user_id")

    shares = db.execute(
        "SELECT DISTINCT shares_id, shares.name  FROM purchase INNER JOIN shares ON purchase.shares_id=shares.id WHERE user_id=:user",
        user=user)

    print(shares)
    total_price = float(0)
    result = ""
    for i in shares:
        print(i)
        sum = db.execute("SELECT SUM(amount) FROM purchase WHERE user_id=:user and shares_id =:id",
                         user=user, id=i.get("shares_id"))
        amount = sum[0].get("SUM(amount)")
        print(amount)
        if amount != 0:

            name = i.get("name")
            lookup_result = lookup(name)
            if lookup_result is None:
                return apology("symbol not exist", 400)
            else:
                try:
                    price = float(lookup_result.get("price"))
                except:
                    return apology("price not set", 400)
                company = lookup_result.get("name")
                all_shares_price = price * float(amount)
                total_price += all_shares_price
                str = '<tr>'
                str += '<td>{}</td>'.format(name)
                str += '<td>{}</td>'.format(company)
                str += '<td>{}</td>'.format(amount)
                str += '<td>{}</td>'.format(usd(price))
                str += '<td>{}</td>'.format(usd(all_shares_price))
                str += '</tr>'
                result += str
                print(result)
    cash = db.execute("SELECT cash FROM users WHERE id = :user",
                      user=user)
    total_price += float(cash[0].get("cash"))
    return render_template("index.html", data=result, cash=usd(cash[0].get("cash")), total=usd(total_price))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == 'GET':
        return render_template("buy.html")

    if request.method == 'POST':
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        elif not request.form.get("shares"):
            return apology("must provide shares", 400)
        try:
            int(request.form.get("shares"))
            float(request.form.get("shares"))
        except:
            return apology("must provide shares", 400)
        if int(request.form.get("shares")) <= 0:
            return apology("shares must be a positive", 400)
        symbol = request.form.get("symbol")
        print(symbol)
        amount = request.form.get("shares")
        print(amount)
        result = lookup(symbol)
        print(result)
        if result is None:
            return apology("symbol not exist", 400)
        try:
            price = float(result.get("price"))
        except:
            return apology("price not set", 400)
        shares = db.execute("SELECT id FROM shares WHERE name = :symbol",
                            symbol=symbol)
        if len(shares) == 0:
            ns = db.execute("INSERT INTO shares (name) VALUES(:symbol)",
                            symbol=symbol)
            print(ns)
        shares = db.execute("SELECT id FROM shares WHERE name = :symbol",
                            symbol=symbol)
        print(shares[0])

        total_price = price * float(amount)
        print(total_price)
        user = session.get("user_id")
        print(user)
        dat = datetime.now()
        today = dat.strftime("%d/%m/%Y %H:%M:%S")

        cash = db.execute("SELECT cash FROM users WHERE id = :user",
                          user=user)
        print(cash)
        up_cash = float(cash[0].get("cash")) - float(total_price)
        if up_cash < 0:
            return apology("not enough money on your account", 400)
        purchase = db.execute(
            "INSERT INTO purchase (user_id, shares_id, date, amount, price_per_share) VALUES (:user, :shares, :date, :amount, :price)",
            user=user, shares=shares[0].get("id"), date=today, amount=amount, price=price)
        print(purchase)
        update = db.execute("UPDATE users SET cash = :up_cash WHERE id = :user",
                            user=user, up_cash=up_cash)
        return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.values.get("username")
    coincidence = db.execute("SELECT id FROM users WHERE username = :username",
                             username=username)
    if len(coincidence) == 0:
        print("true")
        return jsonify(True)
    else:
        print("false")
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user = session.get("user_id")
    purchase = db.execute(
        "SELECT shares.name, date, amount, price_per_share FROM purchase INNER JOIN shares ON purchase.shares_id=shares.id WHERE user_id=:user",
        user=user)
    result = ""
    for i in purchase:
        name = i.get("name")
        amount = i.get("amount")
        print(amount)
        price = i.get("price_per_share")
        total_price = float(abs(amount)) * float(price)
        date = i.get("date")
        str = '<tr>'
        str += '<td>{}</td>'.format(name)
        str += '<td>{}</td>'.format(amount)
        str += '<td>{}</td>'.format(usd(total_price))
        str += '<td>{}</td>'.format(date)
        str += '</tr>'
        result += str

    return render_template("history.html", data=result)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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
    if request.method == 'GET':
        return render_template("quote.html")

    if request.method == 'POST':
        symbol = request.form.get("symbol")
        print(symbol)
        result = lookup(symbol)
        if result is None:
            return apology("symbol not exist", 400)
        else:
            data = "A share of " + result.get("name") + "(" + result.get("symbol") + ")" + " cost " + usd(
                result.get("price"))
            return render_template("quoted.html", data=data)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    if request.method == 'POST':
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide confirm password", 400)

        username = request.form.get("username")
        print(username)
        password = request.form.get("password")
        print(password)
        confirmation = request.form.get("confirmation")
        print(confirmation)

        if password != confirmation:
            return apology("provided password and confirmed password are not the same", 400)

        coincidence = db.execute("SELECT id FROM users WHERE username = :username",
                                 username=request.form.get("username"))
        print(coincidence)

        if len(coincidence) > 0:
            return apology("user with the same name already exist", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                   username=username, hash=generate_password_hash(password))
        return redirect("/login")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user = session.get("user_id")
    if request.method == 'GET':
        shares = db.execute(
            "SELECT DISTINCT shares_id, shares.name, SUM(amount) FROM purchase INNER JOIN shares ON purchase.shares_id=shares.id WHERE user_id=:user;",
            user=user)
        result = ""
        for i in shares:
            name = i.get("name")
            st = "<option value =\"" + name + "\">" + name + "</option>"
            result += st
            print(result)
        return render_template("sell.html", data=result)

    if request.method == 'POST':
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        elif not request.form.get("shares"):
            return apology("must provide shares", 400)
        try:
            int(request.form.get("shares"))
            float(request.form.get("shares"))
        except:
            return apology("must provide shares", 400)
        if int(request.form.get("shares")) <= 0:
            return apology("amount must be a positive", 400)
        symbol = request.form.get("symbol")
        sum = db.execute(
            "SELECT SUM(amount), shares.name, shares.id FROM purchase INNER JOIN shares ON shares_id = shares.id WHERE user_id=:user and shares.name =:name",
            user=user, name=symbol)
        print(sum)
        if len(sum) > 0:
            try:
                user_sum = int(sum[0].get("SUM(amount)"))
            except:
                return apology("sum not set", 400)
            try:
                amount = int(request.form.get("shares"))
            except:
                return apology("shares not set", 400)
            symbol = sum[0].get("name")
            symbol_id = sum[0].get("id")
            print(amount)
            if user_sum == 0 or user_sum < amount:
                return apology("you have not enough stocks", 400)

            result = lookup(symbol)
            print(result)
            if result is None:
                return apology("symbol not exist", 400)
            try:
                price = float(result.get("price"))
            except:
                return apology("price not set", 400)
            total_price = price * float(amount)
            print(total_price)
            dat = datetime.now()
            today = dat.strftime("%d/%m/%Y %H:%M:%S")
            print(today)

            cash = db.execute("SELECT cash FROM users WHERE id = :user",
                              user=user)
            print(cash)
            up_cash = float(cash[0].get("cash")) + total_price
            purchase = db.execute(
                "INSERT INTO purchase (user_id, shares_id, date, amount, price_per_share) VALUES (:user, :shares, :date, :amount, :price)",
                user=user, shares=symbol_id, date=today, amount=-abs(amount), price=price)

            update = db.execute("UPDATE users SET cash = :up_cash WHERE id = :user",
                                user=user, up_cash=up_cash)
    return redirect("/")


@app.route("/changepass", methods=["GET", "POST"])
def changepass(let=None):
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("new_password"):
            return apology("must provide new password", 400)
        elif not request.form.get("confirm_new_password"):
            return apology("must provide password", 400)

        username = request.form.get("username");

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)
        new_password = request.form.get("new_password");
        confirm_new_password = request.form.get("confirm_new_password");
        if new_password != confirm_new_password:
            return apology("provided password and confirmed password are not the same", 400)

        db.execute("UPDATE users SET hash =:hash WHERE username = :username;",
                   username=username, hash=generate_password_hash(new_password))
        return redirect("/login")
    else:
        return render_template("change.html")


@app.route("/checkcredo", methods=["GET"])
def checkcredo():
    """Return true if username available, else false, in JSON format"""
    print("checkcredo")
    auth = request.headers.get("Authorization", None)
    print(auth)
    if not auth:
        abort(401, "Authorization header is expected")

    parts = auth.split()

    token = parts[1]
    print(token)
    decode = base64.b64decode(token).decode("utf-8")
    print(decode)
    credo = decode.split(":")
    print(credo)
    rows = db.execute("SELECT * FROM users WHERE username = :username",
                      username=credo[0])

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0]["hash"], credo[1]):
        return jsonify(False)
    else:
        return jsonify(True)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
