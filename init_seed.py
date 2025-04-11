import random
import sqlite3
from werkzeug.security import generate_password_hash

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM games")
db.execute("DELETE FROM teams")
db.execute("DELETE FROM players")

sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
db.execute(sql, ["admin", generate_password_hash("admin")])

teams = [
    "Oklahoma City Thunder",
    "Cleveland Cavaliers",
    "Boston Celtics",
    "Houston Rockets",
    "New York Knicks",
    "Los Angeles Lakers",
    "Denver Nuggets",
    "Indiana Pacers",
    "LA Clippers",
    "Golden State Warriors"
]

for team in teams:
    sql = "INSERT INTO teams (team, owner) VALUES (?, 1)"
    db.execute(sql, [team])

player_lists = [
    ["Shai Gilgeous-Alexander", "Alex Caruso", "Jalen Williams",
        "Chet Holmgren", "Isaiah Hartenstein"],  # Oklahoma City Thunder
    ["Darius Garland", "Donovan Mitchell", "Max Strus",
        "Evan Mobley", "Jarrett Allen"],  # Cleveland Cavaliers
    ["Jrue Holiday", "Derrick White", "Jaylen Brown",
        "Jayson Tatum", "Kristaps Porziņģis"],  # Boston Celtics
    ["Fred VanVleet", "Jalen Green", "Dillon Brooks",
        "Jabari Smith Jr.", "Alperen Şengün"],  # Houston Rockets
    ["Jalen Brunson", "Mikal Bridges", "OG Anunoby",
        "Julius Randle", "Mitchell Robinson"],  # New York Knicks
    ["D'Angelo Russell", "Austin Reaves", "LeBron James",
        "Rui Hachimura", "Anthony Davis"],  # Los Angeles Lakers
    ["Jamal Murray", "Kentavious Caldwell-Pope", "Michael Porter Jr.",
        "Aaron Gordon", "Nikola Jokić"],  # Denver Nuggets
    ["Tyrese Haliburton", "Andrew Nembhard", "Aaron Nesmith",
        "Pascal Siakam", "Myles Turner"],  # Indiana Pacers
    ["James Harden", "Terance Mann", "Paul George",
        "Kawhi Leonard", "Ivica Zubac"],  # LA Clippers
    ["Stephen Curry", "Brandin Podziemski", "Andrew Wiggins",
        "Jonathan Kuminga", "Draymond Green"]  # Golden State Warriors
]

team_id_counter = 0
for player_list in player_lists:
    team_id_counter += 1
    for player in player_list:
        sql = "INSERT INTO players (team_id, player, gp, pts, reb, ast) VALUES (?, ?, 9, ?, ?, ?)"
        db.execute(sql, [team_id_counter, player, random.randint(
            0, 270), random.randint(0, 200), random.randint(0, 100)])

team_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for i in team_ids:
    temp_team_ids = team_ids.copy()
    temp_team_ids.remove(i)
    for j in temp_team_ids:
        sql = "INSERT INTO games (home_id, away_id, winner_id) VALUES (?, ?, ?)"
        db.execute(sql, [i, j, random.choice([i, j])])

db.commit()
db.close()
