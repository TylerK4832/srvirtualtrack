import os
import sqlite3

from helpers import bubbleSortDates, bubbleSortTimes, apology

from flask import Flask, render_template, request, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Luluislazy48!@localhost/srvirtualtrack'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Times(db.Model):
    __tablename__ = 'times'
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String())
    last = db.Column(db.String())
    year = db.Column(db.String())
    gender = db.Column(db.String())
    event = db.Column(db.String())
    minutes = db.Column(db.Integer())
    seconds = db.Column(db.Integer())
    milliseconds = db.Column(db.Integer())
    date = db.Column(db.String())
    email = db.Column(db.String())

    def __init__(self, first, last, year, gender, event, minutes, seconds, milliseconds, date, email):
        self.first = first
        self.last = last
        self.year = year
        self.gender = gender
        self.event = event
        self.minutes = minutes
        self.seconds = seconds
        self.milliseconds = milliseconds
        self.date = date
        self.email = email


@app.route("/")
def index():
    connection=sqlite3.connect("srvirtualtrack.db")
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM times")
    entries=cursor.fetchall()

    list = []
    for t in entries:
        sub = [t[0] + ' ' + t[1], t[5], t[6], t[7], t[2], t[8], t[4]]
        list.append(sub)
    bubbleSortDates(list)
    for t in list:
        rep = str(t[1] + ':' + t[2] + '.' + t[3])
        del t[1], t[1], t[1]
        t.append(rep)

    return render_template("index.html", list=list, length = len(list))

@app.route("/rankings")
@app.route("/rankings/<event>/<gender>/")
def rankings(event=1, gender=1):
    if event == 1 and gender == 1:
        return render_template("rankingshome.html")
    else:
        connection=sqlite3.connect("srvirtualtrack.db")
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM times WHERE event = :event AND gender = :gender", {'event': event, 'gender': gender.capitalize()})
        timesList=cursor.fetchall()

        list = []
        for t in timesList:
            sub = [t[0] + ' ' + t[1], t[5], t[6], t[7], t[2], t[8]]
            list.append(sub)
        bubbleSortTimes(list)
        for t in list:
            rep = str(t[1] + ':' + t[2] + '.' + t[3])
            del t[1], t[1], t[1]
            t.append(rep)

        return render_template("rankings.html", list=list, event=event, gender=gender.capitalize(), length = len(list))

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "GET":
        return render_template("submit.html")

    if request.method == "POST":
        first = request.form.get("first")
        last = request.form.get("last")
        year = request.form.get("year")
        email = request.form.get("email")
        gender = request.form.get("gender")
        event = request.form.get("event")
        minutes = request.form.get("minutes")
        seconds = request.form.get("seconds")
        milliseconds = request.form.get("milliseconds")
        date = request.form.get("date")

        if not minutes.isdigit() or not seconds.isdigit() or not milliseconds.isdigit():
            return apology("Invalid input: time")

        if len(minutes) > 2 or len(seconds) > 2 or len(milliseconds) > 2:
            return apology("Invalid input: time")

        if len(minutes) == 1:
            minutes = '0' + minutes

        if len(seconds) == 1:
            seconds = '0' + seconds

        if len(milliseconds) == 1:
            milliseconds = '0' + milliseconds

        connection=sqlite3.connect("srvirtualtrack.db")
        cursor=connection.cursor()
        cursor.execute("INSERT INTO times (firstname, lastname, year, gender, event, minutes, seconds, milliseconds, date, email) VALUES(:first, :last, :year, :gender, :event, :minutes, :seconds, :milliseconds, :date, :email)",
                        dict(first=first, last=last, year=year, gender=gender, event=event, minutes=minutes, seconds=seconds, milliseconds=milliseconds, date=date, email=email))
        connection.commit()

        return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
