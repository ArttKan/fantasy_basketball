import db


def add_player(player_name, team_id):
    sql = """INSERT INTO players (player, team_id, gp, pts, reb, ast)
            VALUES (?, ?, 0, 0, 0, 0)"""
    db.execute(sql, [player_name, team_id])


def get_players():
    sql = """SELECT players.id,
                    players.player,
                    players.gp,
                    players.pts,
                    players.reb,
                    players.ast,
                    players.team_id,
                    teams.team
                FROM players
                LEFT JOIN teams
                ON teams.id = players.team_id"""
    return db.query(sql)


def get_player(player_id):
    sql = """SELECT players.id,
                    players.player,
                    players.gp,
                    players.pts,
                    players.reb,
                    players.ast,
                    players.team_id
                FROM players
                WHERE players.id = ?"""
    result = db.query(sql, [player_id])
    return result[0] if result else None


def get_team(player_id):
    sql = """SELECT teams.owner,
                    teams.team,
                    teams.id
                FROM teams
                LEFT JOIN players
                ON teams.id = players.team_id
                WHERE players.id = ?"""
    return db.query(sql, [player_id])[0]


def delete_player(player_id):
    sql = """DELETE FROM players WHERE id = ?"""
    db.execute(sql, [player_id])


def update_player(player_id, player_name, team_id):
    sql = """UPDATE players SET player = ?,
                            team_id = ?
                            WHERE id = ?"""
    db.execute(sql, [player_name, team_id, player_id])


def update_stats(player_id, points, rebounds, assists):
    sql = """UPDATE players SET pts = pts + ?,
                            reb = reb + ?,
                            ast = ast + ?,
                            gp = gp + 1
                            WHERE id = ?"""
    db.execute(sql, [points, rebounds, assists, player_id])


def find_players(query):
    sql = """SELECT id,
                    player,
                    pts,
                    ast,
                    reb,
                    gp
                FROM players
                WHERE player LIKE ?"""
    return db.query(sql, ["%" + query + "%"])


def player_count():
    sql = """COUNT(*) FROM players"""
    return db.query(sql)


def get_all_names():
    sql = "SELECT player FROM players"
    return db.query(sql)
