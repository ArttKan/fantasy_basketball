import db


def add_team(team_name):
    sql = "INSERT INTO teams (team) VALUES (?)"
    db.execute(sql, [team_name])


def get_teams():
    sql = "Select id, team FROM teams"
    return db.query(sql)


def get_team(team_id):
    sql = "SELECT team, id, wins, losses FROM teams WHERE teams.id = ?"
    return db.query(sql, [team_id])[0]
