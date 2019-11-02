#jordan Lieber application for handlign legal matters.

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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///gcapp.db")



@app.route("/")
@login_required
def index():
    return render_template("index.html")




@app.route("/check", methods=["GET"])
def check():

    username = request.args.get("username")

    usernames = db.execute("SELECT username FROM users WHERE username = :username", username=username)

    if not usernames and username:
        print("what the heck")
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():

    # get all info in transactions by the user
    stock_history = db.execute(
        "SELECT Symbol, Num_Shares, price_per_share, Date_Time FROM Transactions WHERE user_ID = :user_id ORDER BY symbol",
         user_id=session["user_id"])

    return render_template("history.html", portfolio=stock_history)



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




@app.route("/register", methods=["GET", "POST"])
def register():

 # User reached route via POST (as by submitting a form via POST)
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        rows = db.execute("SELECT username FROM users")  # Query database for username

        # check username entered
        if not request.form.get("username"):
            return apology("choose a user name", 400)

        username = request.form.get("username")

        if check() == jsonify(False):
            return apology("sorry username unavialble; choose a user name", 400)

        usernames = db.execute("SELECT username FROM users WHERE username = :username", username=username)

        print(usernames)
        # check if username taken
        if usernames:
            return apology("sorry username unavialble; choose a user name", 400)

        for name in rows:
            if request.form.get("username") == name:
                return apology("username exists choose a new one", 400)

        if not request.form.get("password"):
            return apology("make a password", 400)

        if not request.form.get("confirmation"):
            return apology("confirm password", 400)

        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords dont match", 400)

        hash = generate_password_hash(request.form.get("password"),  "sha256")

        username = request.form.get("username")
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                   username=username, hash=hash)
        session.get("user_id")

        return redirect("/login")


@app.route("/litform", methods=["GET", "POST"])
@login_required
def lit_form():

    if request.method == "GET":


        return render_template("litform.html")


    if request.method == "POST":
        db.execute("INSERT INTO Litigations ( Entry_ID, Client, Case_Name, Court, Docket_No, Parties, Outside_Counsel_Defendant_Attorney,\
                        Opposing_Counsel_Plaintiff_Attorney, Description, Case_Status, Upcoming_Deadlines, Notes, Date_Entry, User_ID)\
                        VALUES(:Entry_ID, :Client, :Case_Name, :Court, :Docket_No, :Parties, :Outside_Counsel_Defendant_Attorney,\
                        :Opposing_Counsel_Plaintiff_Attorney, :Description, :Case_Status, :Upcoming_Deadlines, :Notes, :Date_Entry, :User_ID)",

                        Entry_ID = request.form.get("shares"),
                        Client = request.form.get("client"),
                        Case_Name = request.form.get("case_name"),
                        Court = request.form.get("court"),
                        Docket_No = request.form.get("Docket_No"),
                        Parties = request.form.get("Parties"),
                        Outside_Counsel_Defendant_Attorney = request.form.get("Outside_Counsel_Defendant_Attorney"),
                        Opposing_Counsel_Plaintiff_Attorney = request.form.get("Opposing_Counsel_Plaintiff_Attorney"),
                        Description = request.form.get("Description"),
                        Case_Status = request.form.get("Case_Status"),
                        Upcoming_Deadlines = request.form.get("Upcoming_Deadlines"),
                        Notes = request.form.get("Notes"),
                        Date_Entry = datetime.now(),
                        User_ID = session["user_id"])


        return redirect("/litsheet")



"""Entry_ID,
Client
Case_Name
Court
Docket_No
Parties
Outside_Counsel_Defendant_Attorney
Opposing_Counsel_Plaintiff_Attorney
Description
Case_Status
Upcoming_Deadlines
Notes
Date_Entry
User_ID
custom_file

"""


@app.route("/litsheet")
@login_required
def lit_sheet():

    matters = db.execute("SELECT * FROM Litigations")

    #print(matters)

    litigation_matters = []

    for matter in matters:

       litigation_matters.append(matter)


    return render_template("litsheet.html", litigation_matters = litigation_matters, matters = matters)


@app.route("/litsearch", methods=["GET", "POST"])
@login_required
def lit_search():

    #:get clinet chosen from user  maybe also matter or the like.

    client = request.form.get("client")

    Case_Name = request.form.get("matter")

    #if getting to webpage:
    if request.method == "GET":

        #query database for data related to the chosen client
        clients = db.execute("SELECT Client FROM Litigations") # could also select by user id

        matters = db.execute("SELECT Case_Name FROM Litigations")


        return render_template("litsearch.html", clients = clients, matters = matters)

    if request.method == "POST":

        if request.form.get("client") and request.form.get("matter"):
            return apology("you can choose to search by client or matter but not both. Choose one", 400)

         #if chose to search by client
        if request.form.get("client"):

            litigation_info = db.execute("SELECT * FROM Litigations WHERE client = :client", client = client)

            litigation_information = []

            for  info in litigation_info:
                litigation_information.append(info)

            return render_template("litsearchresults.html", litigation_information = litigation_information, litigation_info = litigation_info)

          #if chose to search by matter
        if request.form.get("matter"):

            litigation_info = db.execute("SELECT * FROM Litigations WHERE Case_Name = :Case_Name", Case_Name = Case_Name)

            litigation_information = []

            for  info in litigation_info:
                litigation_information.append(info)

            return render_template("litsearchresults.html", litigation_information = litigation_information, litigation_info = litigation_info)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
