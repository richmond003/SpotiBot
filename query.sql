-- Active: 1751837045646@@127.0.0.1@5432@SpotiBot_DB

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE NOT NULL,
    spotify_id TEXT UNIQUE NOT NULL,
    spotify_url TEXT NOT NULL,
    total_playlist INT 
);

-- Create playlist table
CREATE TABLE playlists (
    entry_id SERIAL PRIMARY KEY,  
    id INTEGER NOT NULL REFERENCES users(id),
    playlist_name TEXT NOT NULL,
    artist TEXT NOT NULL,
    playlist_id TEXT UNIQUE NOT NULL,
    playlist_url TEXT UNIQUE NOT NULL,
    total_tracks INT 
);

-- Create tracks table
CREATE TABLE tracks (
    entry_id SERIAL PRIMARY KEY,
    id INTEGER NOT NULL REFERENCES playlists(entry_id),
    track_id TEXT NOT NULL,
    track_name TEXT NOT NULL,
    track_url Text NOT NULL
);


-- Insert dummy users
INSERT INTO users (name, email, spotify_id, spotify_url, total_playlist) VALUES
('Alice', 'alice@example.com', 'alice_spotify', 'https://open.spotify.com/user/alice', 2),
('Bob', 'bob@example.com', 'bob_spotify', 'https://open.spotify.com/user/bob', 1);

-- Insert dummy user_playlists for testing
INSERT INTO playlists (id, playlist_name, playlist_id, playlist_url, total_tracks) VALUES
(1, 'Alice Favorites', 'alice_fav', 'https://open.spotify.com/playlist/alice_fav', 3),
(1, 'Alice Chill', 'alice_chill', 'https://open.spotify.com/playlist/alice_chill', 2),
(2, 'Bob Rock', 'bob_rock', 'https://open.spotify.com/playlist/bob_rock', 1);

-- Insert dummy tracks for testing
INSERT INTO tracks (id, track_id, track_name, track_url) VALUES
(1, 'track_001', 'Song One', 'https://open.spotify.com/track/track_001'),
(1, 'track_002', 'Song Two', 'https://open.spotify.com/track/track_002'),
(1, 'track_003', 'Song Three', 'https://open.spotify.com/track/track_003'),
(2, 'track_004', 'Chill Vibes', 'https://open.spotify.com/track/track_004'),
(2, 'track_005', 'Relax Tune', 'https://open.spotify.com/track/track_005'),
(3, 'track_006', 'Rock Anthem', 'https://open.spotify.com/track/track_006');


-- Select users table
SELECT * FROM users

-- Select  playlist table
SELECT * FROM playlists

-- Select tracks table
SELECT * FROM tracks

-- Select all user's playlists
SELECT playlist_name, playlist_id, playlist_url, total_tracks
FROM playlists p
JOIN users u ON u.id = p.id
WHERE u.name = 'Alice'

-- Select all tracks belonging to a specific user's playlist
SELECT track_id, track_name, track_url
FROM tracks t
JOIN playlists p ON t.id = p.entry_id
JOIN users u ON p.id = u.id
WHERE u.name = 'Alice' AND p.playlist_name = 'Alice Chill'

-- Check if a user exist
SELECT EXISTS (
    SELECT 1 FROM users WHERE users.email = 'rich@rich.com'
)

-- Check if a track belongs to a playlist
SELECT EXISTS (
    SELECT 1 FROM tracks t
    JOIN playlists p ON t.id = p.entry_id
    JOIN users u ON p.id = u.id
    WHERE u.name = 'Alice' AND p.playlist_name = 'Alice Chill' AND t.track_name = 'Chill Vibes'
)

-- Check if a playlist exist
SELECT EXISTS (
    SELECT 1 FROM playlists p
    JOIN users u ON u.id = p.id
    WHERE u.name = 'Alice' AND p.playlist_name = 'Alice Chill'
)

SELECT spotify_id from users
WHERE users.email = 'rich@rich.com'



