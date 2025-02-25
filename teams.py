import db


def add_team(team_name):
    sql = """INSERT INTO teams (team) VALUES (?)"""
    db.execute(sql, [team_name])
