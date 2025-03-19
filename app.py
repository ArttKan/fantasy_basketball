import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import teams
import users

app = Flask(__name__)
app.secret_key = config.secret_key


def require_login():
    if "user_id" not in session:
        abort(403)


@app.route("/")
def index():
    all_teams = teams.get_teams()
    return render_template("index.html", teams=all_teams)


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    teams = users.get_teams(user_id)
    if not user:
        abort(404)
    return render_template("show_user.html", user=user, teams=teams)


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
    owner = teams.get_owner_name(team_id)
    if not team:
        abort(404)
    return render_template("show_team.html", team=team, owner=owner)


@app.route("/add_team")
def add_team():
    require_login()
    return render_template("add_team.html")


@app.route("/create_team", methods=["POST"])
def create_team():
    require_login()
    team_name = request.form["name"]
    if not team_name or len(team_name) > 50:
        abort(403)
    owner_id = session["user_id"]
    teams.add_team(team_name, owner_id)
    return redirect("/")


@app.route("/edit_team/<int:team_id>")
def edit_team(team_id):
    require_login()
    team = teams.get_team(team_id)
    if team["owner"] != session["user_id"]:
        abort(403)
    if not team:
        abort(404)
    return render_template("edit_team.html", team=team)


@app.route("/update_team", methods=["POST"])
def update_team():
    require_login()
    team_id = request.form["team_id"]
    team = teams.get_team(team_id)
    team_id = request.form["team_id"]
    team_name = request.form["name"]
    owner_id = session["user_id"]

    if not team_name or len(team_name) > 50:
        abort(403)
    if team["owner"] != session["user_id"]:
        abort(403)
    if not team:
        abort(404)

    teams.update_team(team_id, team_name, owner_id)
    return redirect("/team/" + str(team_id))


@app.route("/delete_team/<int:team_id>", methods=["GET", "POST"])
def delete_team(team_id):
    require_login()
    team = teams.get_team(team_id)
    if not team:
        abort(404)

    if team["owner"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
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
        return "ERROR: Passwords do not match"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "ERROR: Username already in use"

    return render_template("registered.html")


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
            return "ERROR: Incorrect username or password"


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
    return redirect("/")
