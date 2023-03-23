import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
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
        
    rows=db.execute("""
        SELECT symbol,SUM(shares) as total_shares
        FROM transactions where user_id=:user_id 
        GROUP BY symbol 
        HAVING total_shares > 0
        """,
        user_id=session["user_id"] )
    holdings=[]
    total_price=0
    for row in rows:
        stock = lookup(row["symbol"])
        holdings.append({
            "symbol" : stock["symbol"],
            "name"   : stock["name"],
            "price"  : usd(stock["price"]),
            "shares" : row["total_shares"],
            "total"  : stock["price"] * row["total_shares"]
        })
        total_price+=stock["price"] * row["total_shares"]
    rows=db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"] )
    cash=rows[0]["cash"]
    total_price += cash
    return render_template("index.html",holdings=holdings,cash=usd(cash),total_price=usd(total_price))
    

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    
    if request.method == "POST":
        symbol=request.form.get("symbol").upper()
        if symbol is None:
            return apology("Must enter symbol field" , 403)
        shares=int(request.form.get("shares"))
        if shares < 1:
            return apology("Must Provide positive value of shares" , 403)
        stock=lookup(symbol)
        if stock is None:
            return apology("Invalid symbol" , 400)
        rows=db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"] )
        cash=rows[0]["cash"]
        updated_cash = cash - shares * stock['price']
        if updated_cash < 0:
            return apology("You can't afford")
        db.execute("UPDATE users SET cash=:updated_cash where id=:id",updated_cash=updated_cash,id=session["user_id"])
        db.execute("""
            INSERT INTO transactions(user_id,symbol,name,shares,price)
            VALUES(:user_id,:symbol,:name,:shares,:price)
            """,
            user_id=session["user_id"],
            symbol=stock['symbol'],
            name=stock['name'], 
            shares=shares,
            price=stock['price']  )
        flash("Brought!")   
        return redirect("/")
        
    else:   
        return render_template("buy.html")
        

@app.route("/history")
@login_required
def history():
    rows=db.execute("""
        SELECT * from transactions
        where user_id=:user_id
        """,
        user_id=session["user_id"] )
    
    holdings=[]
    
    for row in rows:
        holdings.append({
            "symbol" : row["symbol"],
            "price"  : usd(row["price"]),
            "shares" : row["shares"],
            "transacted"  : row["transacted"]
        })
    
    return render_template("history.html",holdings=holdings)



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
    if request.method == "POST":
        if request.form.get("symbol") is  None:
            return apology("Must provide symbol")
        symbol=request.form.get("symbol").upper()
        stock=lookup(symbol)
        if stock is None:
            return apology("Invalid symbol" , 400)
        return render_template("quoted.html" , stockname={
            'name' : stock['name'],
            'symbol' : stock['symbol'],
            'price' : usd(stock['price'])
        })
  
    else:
        return render_template("quote.html")


@app.route("/changePassword", methods=["GET", "POST"])
def change_password():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        
        # Ensure old password was submitted
        if not request.form.get("old"):
            return apology("must provide old password", 403)
            
        
        
        
        # Ensure old passwords was submitted
        if not request.form.get("new"):
            return apology("must provide new password", 403)
        if not request.form.get("RetypeNew"):
            return apology("must Retype new password", 403)
        
        # Ensure new passwords are same
        if  request.form.get("new") != request.form.get("RetypeNew"):
            return apology("New passwords are not  same",403)
            
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("old")):
            return apology("invalid username and/or password", 403)
        else:
            db.execute("UPDATE users SET hash = :hash_password WHERE username = :username",
            username=request.form.get("username"),
            hash_password=generate_password_hash(request.form.get("new")))
        return redirect("/")
    else:
        return render_template("password.html")
        
        
        
        
@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        elif  request.form.get("password") != request.form.get("confirmation"):
            return apology("password not be same",403)
       
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        
        if len(rows) == 1:
            db.execute("INSERT INTO users(username,hash) VALUES (:username,:hash_password)" ,
            username=request.form.get("username") ,
            hash_password=generate_password_hash(request.form.get("password")))
        flash("Successfully create a account!")
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol=request.form.get("symbol").upper()
        if symbol is None:
            return apology("Must enter symbol field" , 403)
        shares=int(request.form.get("shares"))
        if shares < 1:
            return apology("Must Provide number of shares" , 403)
        stock=lookup(symbol)
        if stock is None:
            return apology("Invalid symbol" , 400)
        row=db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"] )
        cash=row[0]["cash"]
        updated_cash = cash + shares * stock['price']
        
        db.execute("UPDATE users SET cash=:updated_cash where id=:id",updated_cash=updated_cash,id=session["user_id"])
        
        
        db.execute("""
            INSERT INTO transactions(user_id,symbol,name,shares,price)
            VALUES(:user_id,:symbol,:name,:shares,:price)
            """,
            user_id=session["user_id"],
            symbol=stock['symbol'],
            name=stock['name'], 
            shares= -1 * shares,
            price=stock['price']  )
        flash("Sold!")   
        return redirect("/")
        
    else:    
        return render_template("sell.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
