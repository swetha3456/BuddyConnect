from flask import Flask, render_template, session, url_for, redirect, request, flash
from dbfunctions import *

app = Flask(__name__)
app.secret_key = b"030a8ee0eb274b3e7fd9db490b0fd6a532b1fa1f1fd6825c5852c7363358c4b6"

@app.route("/")
def home():
    if "user_email" not in session:
        return redirect(url_for("login"))

    return render_template("home.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        session["user_email"] = request.form["email"]
        register_user(request.form["email"], request.form["password"], request.form["firstName"], request.form["lastName"], request.form["gender"], request.form["location"], request.form.getlist("interests"))
        return redirect(url_for("home"))
    
    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        if authenticate_user(request.form["email"], request.form["password"]):
            session["user_email"] = request.form["email"]
            return redirect(url_for("home"))
        
        else:
            flash("Invalid credentials")

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)