CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    team TEXT
);

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES teams,
    player TEXT,
    gp INTEGER,
    pts INTEGER,
    reb INTEGER,
    ast INTEGER
);

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    home_id INTEGER REFERENCES teams,
    away_id INTEGER REFERENCES teams,
    winner_id INTEGER REFERENCES teams
);

INSERT INTO teams (team) VALUES ('San Antonio Spurs');
INSERT INTO teams (team) VALUES ('Cleveland Cavaliers');
INSERT INTO teams (team) VALUES ('Golden State Warriors');
INSERT INTO players (team_id, player, gp, pts, reb, ast) Values (3, 'Stephen Curry', 1, 35, 6, 10);
INSERT INTO players (team_id, player, gp, pts, reb, ast) Values (1, 'Victor Wembanyama', 1, 27, 8, 5);
INSERT INTO players (team_id, player, gp, pts, reb, ast) Values (2, 'Evan Mobley', 1, 20, 12, 6);
INSERT INTO games (home_id, away_id, winner_id) VALUES (1, 2, 2);