from flask import Flask, render_template, session, url_for, redirect, request, flash
from dbfunctions import *
from datetime import datetime
from email_notif import send_email

app = Flask(__name__)
app.secret_key = b"030a8ee0eb274b3e7fd9db490b0fd6a532b1fa1f1fd6825c5852c7363358c4b6"

@app.route("/")
def home():
    if "user_email" not in session:
        return redirect(url_for("login"))

    events = get_relevant_events(session["user_email"])
    context = []

    for event in events:
        date_object = datetime.strptime(event[5], r"%Y-%m-%d")
        formatted_date = date_object.strftime("%B %-d, %Y")

        starttime_object = datetime.strptime(event[6], "%H:%M")
        endtime_object = datetime.strptime(event[7], "%H:%M")
        formatted_starttime = starttime_object.strftime("%I:%M %p")
        formatted_endtime = endtime_object.strftime("%I:%M %p")

        event_details = {
            "eventName" : event[1],
            "eventType" : event[2],
            "venue" : event[3],
            "eventDate" : formatted_date,
            "startTime" : formatted_starttime,
            "endTime" : formatted_endtime,
            "description" : event[8],
            "userFullName" : get_full_name(event[9])
        }

        context.append(event_details)

    return render_template("home.html", context=context)

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

@app.route("/newEvent", methods = ["GET", "POST"])
def new_event():
    if "user_email" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        create_event(
            request.form["eventName"],
            request.form["eventType"],
            request.form["venue"],
            get_user_location(session["user_email"]),
            request.form["eventDate"],
            request.form["startTime"],
            request.form["endTime"],
            session["user_email"],
            request.form["eventDescription"]
        )
        
        return redirect(url_for("home"))
    
    return render_template("addNewEvent.html")

@app.route("/events/<int:eventID>", methods = ["GET", "POST"])
def event_details(eventID):
    if request.method == "POST":
        send_email(eventID, session["user_email"])
        return redirect(url_for("home"))

    event_info = get_event_details(eventID)

    date_object = datetime.strptime(event_info[5], r"%Y-%m-%d")
    formatted_date = date_object.strftime("%B %-d, %Y")

    starttime_object = datetime.strptime(event_info[6], "%H:%M")
    endtime_object = datetime.strptime(event_info[7], "%H:%M")
    formatted_starttime = starttime_object.strftime("%I:%M %p")
    formatted_endtime = endtime_object.strftime("%I:%M %p")

    context = {
        "eventName" : event_info[1],
        "eventType" : event_info[2],
        "venue" : event_info[3],
        "startTime" : formatted_starttime,
        "endTime" : formatted_endtime,
        "eventDate" : formatted_date,
        "description" : event_info[8],
        "userFullName" : get_full_name(event_info[9]),
        "pastEventsCount" : num_events_posted(event_info[9]),
        "gender" : get_gender(event_info[9])
    }

    return render_template("eventpage.html", context=context)

if __name__ == "__main__":
    app.run(debug=True)