CREATE TABLE IF NOT EXISTS nba_players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    player_id TEXT NOT NULL UNIQUE,
    picture_path TEXT NOT NULL,
    player_worth DECIMAL(10, 2)
);

ALTER TABLE nba_players ADD COLUMN image BLOB;