import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")

# check if everything was submitted
@app.route("/form", methods=["POST"])
def post_form():
    if not request.form.get("name") or not request.form.get("email") \
            or not request.form.get("position") \
            or not request.form.get("qaulity") or not request.form.get("practice"):
        return render_template("error.html", message="You didnt fill out everything")
    # comments and stuff
    file = open("survey.csv", "a")
    writer = csv.writer(file)
    writer.writerow((request.form.get("name"), request.form.get("email"),
                     request.form.get("position"), request.form.get("qaulity"), request.form.get("practice")))
    file.close()
    return redirect("/sheet")


"""
Complete the implementation of post_form in such a way that it
validates a form’s submission, alerting users with a message via error.html if they have not provided values
for one or more fields, just in case your JavaScript code let something through (or was disabled),
writes the form’s values to a new row in survey.csv using csv.writer or csv.DictWriter, and
redirects the user to /sheet.
"""


@app.route("/sheet", methods=["GET"])
def get_sheet():
    file = open("survey.csv", "r")  # open the survey
    reader = csv.reader(file)
    clients = list(reader)
    return render_template("sheet.html", clients=clients)


"""
Complete the implementation of get_sheet in such a way that it
reads past submissions from survey.csv using csv.reader or csv.DictReader and
displays those submissions in an HTML table via a new template.
Style that table using Bootstrap so that it looks nicer than it would with raw HTML alone.
Optionally enhance the table with JavaScript, as via DataTables.
"""