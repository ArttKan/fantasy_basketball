import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM games")
db.execute("DELETE FROM teams")
db.execute("DELETE FROM players")
print("jee")
user_count = 1000
team_count = 10**5
player_count = 10**6
game_count = 10**4

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, team_count + 1):
    db.execute("INSERT INTO teams (team, owner) VALUES (?, ?)",
               ["team" + str(i), random.randint(1, user_count)])

for i in range(1, player_count + 1):
    team_id = random.randint(1, team_count)
    db.execute("""INSERT INTO players (team_id, player, gp, pts, reb, ast)
                  VALUES (?, ?, 0, 0, 0, 0)""",
               [team_id, "player" + str(i)])

for i in range(1, game_count + 1):
    home_id = random.randint(1, team_count)
    away_id = random.randint(1, team_count)
    if home_id == away_id:
        if home_id > team_count:
            home_id += 1
        else:
            home_id -= 1
    db.execute("""INSERT INTO games (home_id, away_id, winner_id)
                  VALUES (?, ?, ?)""",
               [home_id, away_id, random.choice([home_id, away_id])])
db.commit()
db.close()
print("jee")
