import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import teams
import users
import players
import games
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key


def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


def require_login():
    if "user_id" not in session:
        abort(403)


@app.route("/")
def index():
    all_teams = teams.get_teams()
    all_players = players.get_players()
    all_games_id = games.get_games()
    all_games = []
    all_teams_with_record = []
    for team in all_teams:
        wins = teams.get_wins(team["id"])
        total_games = teams.get_games(team["id"])
        losses = total_games - wins
        all_teams_with_record.append(
            (team["id"], team["team"], wins, losses))
    for game in all_games_id:
        home = teams.get_team(game["home_id"])
        away = teams.get_team(game["away_id"])
        winner = teams.get_team(game["winner_id"])
        game = (home["team"], home["id"], away["team"],
                away["id"], winner["team"], winner["id"])
        all_games.append(game)
    all_teams_with_record.sort(key=lambda x: (-x[2], x[3]))
    return render_template("index.html", teams=all_teams_with_record, players=all_players, games=all_games)


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    teams = users.get_teams(user_id)
    if not user:
        abort(404)
    return render_template("show_user.html", user=user, teams=teams)


@app.route("/find_entity")
def find_entity():
    team_query = request.args.get("team_query")
    player_query = request.args.get("player_query")
    if team_query:
        team_results = teams.find_teams(team_query)
    else:
        team_query = ""
        team_results = []
    if player_query:
        player_results = players.find_players(player_query)
    else:
        player_query = ""
        player_results = []
    return render_template("find_entity.html", team_query=team_query, player_query=player_query, player_results=player_results, team_results=team_results)


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/team/<int:team_id>")
def show_team(team_id):
    team = teams.get_team(team_id)
    owner = teams.get_owner_name(team_id)
    players = teams.get_players(team_id)
    wins = teams.get_wins(team_id)
    total_games = teams.get_games(team_id)
    losses = total_games - wins
    if not team:
        abort(404)
    return render_template("show_team.html", wins=wins, team=team, owner=owner, players=players, losses=losses)


@app.route("/add_team")
def add_team():
    require_login()
    return render_template("add_team.html")


@app.route("/create_team", methods=["POST"])
def create_team():
    require_login()
    check_csrf()
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
    check_csrf()
    team_id = request.form["team_id"]
    team = teams.get_team(team_id)
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
    print(team_id)
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


@app.route("/add_player")
def add_player():
    require_login()
    all_teams = teams.get_teams()
    return render_template("add_player.html", teams=all_teams)


@app.route("/create_player", methods=["POST"])
def create_player():
    require_login()
    check_csrf()
    player_name = request.form["name"]
    team_id = request.form["team"]
    team = teams.get_team(team_id)
    all_teams = teams.get_teams()
    all_team_ids = []
    print(team)
    for team in all_teams:
        all_team_ids.append(team["id"])
    if not player_name or len(player_name) > 50:
        abort(403, "Invalid player name")
    if not team_id:
        abort(403, "You must choose team for the player")
    if team["owner"] != session["user_id"]:
        abort(403, "You must choose a team you own")
    if team["id"] not in all_team_ids:
        abort(403, "You must choose an existing team")
    players.add_player(player_name, team_id)
    return redirect("/")


@app.route("/player/<int:player_id>")
def show_player(player_id):
    player = players.get_player(player_id)
    team = players.get_team(player_id)
    if not player:
        abort(404)
    return render_template("show_player.html", player=player, team=team)


@app.route("/delete_player/<int:player_id>", methods=["GET", "POST"])
def delete_player(player_id):
    require_login()
    player = players.get_player(player_id)
    team = players.get_team(player_id)
    if not player:
        abort(404)

    if team["owner"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete_player.html", team=team, player=player)

    if request.method == "POST":
        if "delete" in request.form:
            players.delete_player(player_id)
            return redirect("/")
        else:
            return redirect("/")


@app.route("/edit_player/<int:player_id>")
def edit_player(player_id):
    require_login()
    p_team = players.get_team(player_id)
    player = players.get_player(player_id)
    all_teams = teams.get_teams()
    if p_team["owner"] != session["user_id"]:
        abort(403)
    if not p_team:
        abort(404)
    return render_template("edit_player.html", p_team=p_team, player=player, all_teams=all_teams)


@app.route("/update_player", methods=["POST"])
def update_player():
    require_login()
    player_name = request.form["name"]
    player_id = request.form["player_id"]
    team_id = request.form["team"]
    team = teams.get_team(team_id)
    if not player_name or len(player_name) > 50:
        abort(403)
    if team["owner"] != session["user_id"]:
        abort(403)
    if not team:
        abort(404)
    players.update_player(player_id, player_name, team_id)
    return redirect("/player/" + str(player_id))


@app.route("/add_game")
def add_game():
    require_login()
    all_teams = teams.get_teams()
    return render_template("add_game.html", teams=all_teams)


@app.route("/finalise_game", methods=["POST"])
def finalise_game():
    require_login()
    check_csrf()
    home_team_id = int(request.form["home_team"])
    away_team_id = int(request.form["away_team"])
    if home_team_id == away_team_id:
        abort(403, "You must choose two different teams!")
    if not home_team_id or not away_team_id:
        abort(403)
    home_team = teams.get_team(home_team_id)
    away_team = teams.get_team(away_team_id)
    home_players = teams.get_players(home_team_id)
    away_players = teams.get_players(away_team_id)
    return render_template("/finalise_game.html", home_team=home_team, away_team=away_team, home_players=home_players, away_players=away_players)


@app.route("/create_game", methods=["POST"])
def create_game():
    require_login()
    check_csrf()
    winner_id = request.form["winner"]
    if not winner_id:
        abort(403, "You must choose a winner for the game")
    home_team_id = int(request.form["home_team_id"])
    away_team_id = int(request.form["away_team_id"])
    games.post_result(home_team_id, away_team_id, winner_id)
    home_players = teams.get_players(home_team_id)
    away_players = teams.get_players(away_team_id)
    for player in home_players:
        pts = request.form[str(player["id"]) + "_pts"]
        reb = request.form[str(player["id"]) + "_reb"]
        ast = request.form[str(player["id"]) + "_ast"]
        players.update_stats(player["id"], pts, reb, ast)
    for player in away_players:
        pts = request.form[str(player["id"]) + "_pts"]
        reb = request.form[str(player["id"]) + "_reb"]
        ast = request.form[str(player["id"]) + "_ast"]
        players.update_stats(player["id"], pts, reb, ast)
    return redirect("/")


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "ERROR: Passwords do not match"

    try:
        users.create_user(username, password1)
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

        user_id = users.check_login(username, password)

        if user_id:
            session["username"] = username
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return "ERROR: Incorrect username or password"


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
    return redirect("/")
