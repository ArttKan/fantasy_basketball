CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE teams (
    id INTEGER PRIMARY KEY,
    team TEXT,
    'owner' INTEGER
);

CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    team_id INTEGER REFERENCES teams,
    player TEXT,
    gp INTEGER,
    pts INTEGER,
    reb INTEGER,
    ast INTEGER
);

CREATE TABLE games (
    id INTEGER PRIMARY KEY,
    home_id INTEGER REFERENCES teams,
    away_id INTEGER REFERENCES teams,
    winner_id INTEGER REFERENCES teams
);