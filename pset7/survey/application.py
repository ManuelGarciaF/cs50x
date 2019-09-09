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


@app.route("/form", methods=["POST"])
def post_form():
    name = request.form.get("name")
    email = request.form.get("email")
    gender = request.form.get("gender")
    soda = request.form.get("soda")
    if not name or not email or not gender or not soda:
        return render_template("error.html", message="You must complete all fields")
    with open('survey.csv', 'a') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'email', 'gender', 'soda'])
        writer.writerow({'name': name, 'email': email, 'gender': gender, 'soda': soda})
    return redirect('/sheet')


@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open('survey.csv', 'r') as file:
        reader = csv.DictReader(file)
        return render_template('sheet.html', csv=reader)


if __name__ == '__main__':
    app.run(debug=True)