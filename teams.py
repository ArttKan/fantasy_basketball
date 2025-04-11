import db


def add_team(team_name, owner_id):
    sql = """INSERT INTO teams (team, owner)
            VALUES (?, ?)"""
    db.execute(sql, [team_name, owner_id])


def get_teams():
    sql = """SELECT id,
                    team,
                    owner
                FROM teams"""
    return db.query(sql)


def get_team_id(team_name):
    sql = """SELECT teams.id
                FROM teams
                WHERE teams.team = ?"""
    return db.query(sql, [team_name])[0][0]


def get_team(team_id):
    sql = """SELECT teams.team,
                    teams.id,
                    teams.owner,
                    users.username
                FROM teams,
                    users
                WHERE teams.owner = users.id AND
                    teams.id = ?"""
    result = db.query(sql, [team_id])
    return result[0] if result else None


def update_team(team_id, team_name, owner_id):
    sql = """UPDATE teams SET team = ?,
                            owner = ?
                            WHERE id = ?"""
    db.execute(sql, [team_name, owner_id, team_id])


def delete_team(team_id):
    sql = """DELETE FROM teams WHERE id = ?"""
    db.execute(sql, [team_id])


def find_teams(query):
    sql = """SELECT id, team
                FROM teams
                WHERE team LIKE ?"""
    return db.query(sql, ["%" + query + "%"])


def get_owner_name(team_id):
    sql = """SELECT users.username
                FROM users, teams
                WHERE teams.owner = users.id AND
                teams.id = ?"""
    return db.query(sql, [team_id])[0]


def get_players(team_id):
    sql = """SELECT players.id,
                    players.team_id,
                    players.player,
                    players.pts,
                    players.ast,
                    players.reb,
                    players.gp
                FROM players
                WHERE players.team_id = ?"""
    return db.query(sql, [team_id])


def get_wins(team_id):
    sql = """SELECT COUNT(winner_id)
                FROM games
                WHERE winner_id = ?"""
    return db.query(sql, [team_id])[0][0]


def get_games(team_id):
    sql = """SELECT COUNT(home_id)
                FROM games
                WHERE home_id = ?"""
    home = db.query(sql, [team_id])[0][0]
    sql = """SELECT COUNT(away_id)
            FROM games
            WHERE away_id = ?"""
    away = db.query(sql, [team_id])[0][0]
    return home + away


def teams_count():
    sql = """COUNT(*) FROM teams"""
    return db.query(sql)
