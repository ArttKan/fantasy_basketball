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
    team_id INTEGER,
    player TEXT,
    gp INTEGER,
    pts INTEGER,
    reb INTEGER,
    ast INTEGER,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
);

CREATE TABLE games (
    id INTEGER PRIMARY KEY,
    home_id INTEGER ,
    away_id INTEGER,
    winner_id INTEGER,
    FOREIGN KEY (home_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (away_id) REFERENCES teams(id) ON DELETE CASCADE
);