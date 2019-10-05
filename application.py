import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from datetime import datetime, date

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

# custom filter
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

    #get all info and group by symbol
    rows = db.execute("SELECT * FROM users,transactions WHERE users.id = Transactions.user_ID GROUP BY Transactions.Symbol")

    #get just the symbols

    stock_symbols = db.execute("SELECT Symbol FROM transactions WHERE user_ID = :user_id GROUP BY Symbol", user_id = session["user_id"])

    portfolio = []
    for stock in stock_symbols:

        stock_info = lookup(stock['Symbol'])


        db.execute("SELECT price_per_share FROM transactions WHERE user_ID = :user_id"  , user_id = session["user_id"])

        #get cash remaining
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])

        #get number of shares
        sum_shares = db.execute("SELECT Symbol, SUM(Num_shares) FROM Transactions WHERE user_ID = :user_id AND Symbol = :Symbol",
        user_id = session["user_id"], Symbol = stock['Symbol'][:])



        stock_information = {}

        stock_information['name'] = stock_info['name']
        stock_information['symbol'] = stock_info['symbol']
        stock_information['price'] = usd(stock_info['price'])
        stock_information['shares'] = sum_shares[0]['SUM(Num_shares)']
        stock_information['total'] = stock_information['shares'] * stock_info['price']
        #Use this entry for calculating remaining cash and total portfolio value
        stock_information['totall'] = stock_information['shares'] * stock_info['price']
        stock_information['total'] = usd(stock_information['total'])

        portfolio.append(stock_information)

    #not sure the below does anything anymore
    for stock in rows:
        sum_shares = db.execute("SELECT Symbol, SUM(Num_shares) FROM Transactions WHERE user_ID = :user_id AND Symbol = :Symbol",
        user_id = session["user_id"], Symbol = stock['Symbol'][:])


    if stock_symbols == []:
        #get cash remaining
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])
        return render_template("index.html", portfolio = portfolio, cash = cash[0]['cash'], sum_total=cash[0]['cash'])

    else:

        #get cash remaining
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])

        #set total to zero
        sum_total = 0

        _stock_information = stock_information

        #_stock_information['total'] = int(stock_information['shares'] * stock_info['price'])
        #calculate sum total of potfolio
        for i in range(len(portfolio)):
            sum_total += portfolio[i]['totall']
        sum_total += cash[0]['cash']



        return render_template("index.html", portfolio = portfolio, cash = cash[0]['cash'], sum_total=usd(sum_total))

    """Show portfolio of stocks

                <th>Stocks Owned</th>
                <th>Number of Shares</th>
                <th>Current Price of Each Stock</th>
                <th>Total Value of Each Holding</th>


                <th>Cash Remaining</th>
                <th>Total Value of Portfolio</th> (cash + stocks)

    """
    #return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("choose a symbol", 400)


        symbol=lookup(request.form.get("symbol"))

        #check if symbol is valid
        if not symbol:
            return apology("No such symbol", 400)

        information = lookup(symbol['symbol'])

        #print(information["symbol"])


        if not request.form.get("shares"):
            return apology("insert number of shares", 400)


        #check if num shares is whole digit
        if not request.form.get("shares").isdigit():
            return apology("Sorry. Number of shares must be whole positive integer", 400)

        shares = int(request.form.get("shares"))


        if int(request.form.get("shares")) < 1:
            return apology("Sorry. Number of shares must be whole positive integer", 400)

        if shares < 1:
            return apology("Number of shares must be a positive int", 400)


        # Query database for username
        #rows = db.execute("SELECT * FROM users WHERE username = :username",
                          #username=request.form.get("username"))


        #user_id = db.session.get(id)

        #userid = db.execute("SELECT id from users WHERE id = users[id]")

        row = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])

        #=session.get("user_id"))

        price = int(information["price"])

        _price = usd(price)


        total_price = price * shares

        _total_price = usd(total_price)

        #total_price = total_price)

        if int(row[0]["cash"]) < total_price:
            return apology("Not enough cash, sorry", 403)

        if int(row[0]["cash"]) > total_price:
            db.execute("INSERT INTO Transactions ( price_per_share, Total_price, user_ID, Symbol, Num_shares, Date_Time ) \
            VALUES (:price_per_share, :Total_price, :user_ID, :Symbol, :Num_shares, :Date_Time)",

            price_per_share=_price,
            Total_price = _total_price,
            user_ID=session["user_id"],
            Symbol=symbol['symbol'],
            Num_shares=int(request.form.get("shares")),
            Date_Time= datetime.now())
            db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])# if user has enough cash

         # if user can, then ("INSERT into cash FROM users WHERE id = 1")

        # is purchase succesful, then redirect to homepage
        return redirect("/")


        #return render_template("buy.html", information=information)


        #rows = db.execute("SELECT * FROM users[username]") # Query database for username

        #db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", \
        #username=request.form.get("username"), hash=hash)


        # can user afford the stock
       # ("SELECT cash FROM users WHERE id = 1") # if dealign wiht user id =1 form can see if afford or not

        # if user can, then ("INSERT into cash FROM users WHERE id = 1")
        #("UPDATE users SET cash = cash - 50 WHERE id = 1")

        #symbol=request.form.get("symbol")

        #information = lookup(symbol)




    #"""Buy shares of stock"""
    #return apology("TODO")


@app.route("/check", methods=["GET"])
def check():

    username = request.args.get("username")

    usernames = db.execute("SELECT username FROM users WHERE username = :username", username = username)

    if len(username) >= 1 and usernames == None:
        return jsonify(True)
    else:
        return jsonify(False)



@app.route("/history")
@login_required
def history():


    #get all info in transactions by the user
    stock_history = db.execute("SELECT Symbol, Num_Shares, price_per_share, Date_Time FROM Transactions WHERE user_ID = :user_id ORDER BY symbol" , user_id = session["user_id"])

    return render_template("history.html", portfolio = stock_history)

    """
    for each row make clear whether stock:
    1:bought or sold
    2: stock symbol'
    3: purchae or sale price
    4:num shares bought or sold
    5: date and time whcih transaction occured

    Show history of transactions"""


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
    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("choose a symbol", 400)


        symbol=lookup(request.form.get("symbol"))

        #check if symbol is valid
        if not symbol:
            return apology("Sybmol invalid; choose a symbol", 400)


        information = lookup(symbol['symbol'])

        #convert price into us format
        information['price'] = usd( information['price'])

       # price = information["price"]

        #price = usd(price)

        return render_template("quoted.html", information=information,)

        # return redirect("/quoted")


    #else:
        #return render_template("quote.html")





@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    """
Complete the implementation of register in such a way that it allows a user to register for an account via a form.
Require that a user input a username, implemented as a text field whose name is username.
Render an apology if the user’s input is blank or the username already exists.
Require that a user input a password, implemented as a text field whose name is password, and then that same password again,
implemented as a text field whose name is confirmation. Render an apology if either input is blank or the passwords do not match.
Submit the user’s input via POST to /register.
INSERT the new user into users, storing a hash of the user’s password, not the password itself. Hash the user’s password with generate_password_hash.
Odds are you’ll want to create a new template (e.g., register.html) that’s quite similar to login.html.
Once you’ve implemented register correctly, you should be able to register for an account and log in (since login and logout already work)! And you should be able to see your rows via phpLiteAdmin or sqlite3.
    """
 # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        rows = db.execute("SELECT * FROM users[username]") # Query database for username

        if not request.form.get("username"):
            return apology("choose a user name", 400)

        for name in rows:
            if request.form.get("username") == name:
                return apology("username exists choose a new one", 400)

        if not request.form.get("password"):
             return apology("make a password", 400)

        if not request.form.get("confirmation"):
             return apology("confirm password", 400)

        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords dont match", 400)


        #name = request.form.get("username")
        hash =  generate_password_hash(request.form.get("password"),  "sha256")


        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", \
        username=request.form.get("username"), hash=hash)
        session.get("user_id")
        return redirect("/login")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        hash =  generate_password_hash(request.form.get("password"), "sha256")
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", \
        username=request.form.get("username"), hash=hash)
        # INSERT INTO "users" ("id","username","hash") VALUES (NULL,'jordan','')
        session.get("user_id")
        return render_template("register.html")


    session.get("user_id")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

        #if get to page from Get
    if request.method == "GET":
        return render_template("sell.html")

        #if posting from page
    if request.method == "POST":

        #require user input stock symbol and render apolyg if user fails ro select stock or doesnt own any of the stock.
        if not request.form.get("symbol"):   #if user fails to choose a symbol
            return apology("choose a symbol", 403)

        #get symbol posted by user
        symbol = lookup(request.form.get("symbol"))

        #check if user inputed an actual stock; maybe dont need this

        if symbol == None:
            return apology("No such symbol", 403)

        #get info on the stock user is selling with lookup
        stock_information = lookup(symbol['symbol'])



        #check if user has stock in portolio
        stock_symbols = db.execute("SELECT Symbol FROM transactions WHERE user_ID = :user_id AND symbol = :symbol;",
        user_id = session["user_id"], symbol=symbol['symbol'])

        if stock_symbols == None:
            return apology("Sorry, you dont own that stock. choose again", 403)


        #create flag to check if stock is owned set initial to false
        #flag = False

        #iterate through dict list of stock symbols and switch flag if symbol in dict list.
        #for stock in stock_symbols:
            #if stock[0]['Symbol'] == symbol:
                #flag = True

        #if user doesnt own the stock then flag is still false and render apology
        #if flag == False:
            #return apology("Sorry, you dont own that stock. choose again", 403)

        #get info on the stock user is selling with lookup
        stock_information = lookup(symbol['symbol'])


        #check if user inputed an actual stock; maybe dont need this

        if stock_information == None:
            return apology("No such symbol", 403)

        #check that user inputed number of shares
        if not request.form.get("shares"):
            return apology("insert number of shares", 403)

        #check that user inputed positive integer
        shares = int(request.form.get("shares"))
        if shares < 1:
            return apology("Number of shares must be a positive int", 403)

        #check user owns that many shares:


        #get number of shares owned of stock
        num_shares = db.execute("SELECT SUM(Num_shares) FROM Transactions WHERE user_ID = :user_id AND Symbol = :Symbol;",
        user_id = session["user_id"], Symbol=symbol['symbol'])

        if num_shares == None:
            return apology("You dont own that stock", 403)


        #checks if user has enough shares to sell.
        if shares > num_shares[0]['SUM(Num_shares)']:
            return apology("You dont have that many shares to sell", 403)


        #check the price of the stock
        price = int(stock_information["price"])

        total_price = price * shares

        #update data table to log the transaction and update cash

        db.execute("INSERT INTO Transactions ( price_per_share, Total_price, user_ID, Symbol, Num_shares, Date_Time ) \
            VALUES (:price_per_share, :Total_price, :user_ID, :Symbol, :Num_shares, :Date_Time)",

            price_per_share=price,
            Total_price = total_price,
            user_ID=session["user_id"],
            Symbol=symbol['symbol'],
            Num_shares= -(int(request.form.get("shares"))),
            Date_Time= datetime.now())
        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])


        #if purachse succesful, then redirect to homepage
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
