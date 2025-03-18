import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import teams

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    all_teams = teams.get_teams()
    return render_template("index.html", teams=all_teams)


@app.route("/find_team")
def find_team():
    query = request.args.get("query")
    if query:
        results = teams.find_teams(query)
    else:
        query = ""
        results = []
    return render_template("find_team.html", query=query, results=results)


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/team/<int:team_id>")
def show_team(team_id):
    team = teams.get_team(team_id)
    return render_template("show_team.html", team=team)


@app.route("/add_team")
def add_team():
    return render_template("add_team.html")


@app.route("/create_team", methods=["POST"])
def create_team():
    team_name = request.form["name"]
    owner_id = session["user_id"]
    teams.add_team(team_name, owner_id)
    return redirect("/")


@app.route("/edit_team/<int:team_id>")
def edit_team(team_id):
    team = teams.get_team(team_id)
    return render_template("edit_team.html", team=team)


@app.route("/update_team", methods=["POST"])
def update_team():
    team_id = request.form["team_id"]
    team_name = request.form["name"]
    owner_id = session["user_id"]
    teams.update_team(team_id, team_name, owner_id)
    return redirect("/team/" + str(team_id))


@app.route("/delete_team/<int:team_id>", methods=["GET", "POST"])
def delete_team(team_id):
    if request.method == "GET":
        team = teams.get_team(team_id)
        return render_template("delete_team.html", team=team)

    if request.method == "POST":
        if "delete" in request.form:
            teams.delete_team(team_id)
            return redirect("/")
        else:
            return redirect("/team/" + str(team_id))


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"


@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")
