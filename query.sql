-- Active: 1751837045646@@127.0.0.1@5432@SpotiBot_DB

-- Create users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE NOT NULL,
    user_spotify_id TEXT UNIQUE NOT NULL,
    user_spotify_url TEXT UNIQUE NOT NULL,
    total_playlist INT 
);

-- Create playlist table
CREATE TABLE playlists (
    playlist_id SERIAL PRIMARY KEY,  
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    playlist_name TEXT NOT NULL,
    artist TEXT NOT NULL,
    playlist_spotify_id TEXT UNIQUE NOT NULL,
    playlist_spotify_url TEXT UNIQUE NOT NULL,
    total_tracks INT 
);

-- Create tracks table
CREATE TABLE tracks (
    track_id SERIAL PRIMARY KEY,
    playlist_id INTEGER NOT NULL REFERENCES playlists(playlist_id),
    track_spotify_id TEXT NOT NULL,
    track_name TEXT NOT NULL,
    track_spotify_uri TEXT NOT NULL,
    track_spotify_url Text NOT NULL
);

-- Insert dummy users
INSERT INTO users (name, email, user_spotify_id, user_spotify_url, total_playlist) VALUES
('Alice', 'alice@example.com', 'alice_spotify', 'https://open.spotify.com/user/alice', 2),
('Bob', 'bob@example.com', 'bob_spotify', 'https://open.spotify.com/user/bob', 1);

-- Insert dummy user_playlists for testing
INSERT INTO playlists (user_id, playlist_name, artist, playlist_spotify_id, playlist_spotify_url, total_tracks) VALUES
(1, 'Alice Favorites','some artist', 'alice_fav', 'https://open.spotify.com/playlist/alice_fav', 3),
(1, 'Alice Chill','some artist', 'alice_chill', 'https://open.spotify.com/playlist/alice_chill', 2),
(2, 'Bob Rock','some artist', 'bob_rock', 'https://open.spotify.com/playlist/bob_rock', 1);

-- Insert dummy tracks for testing
INSERT INTO tracks (playlist_id, track_spotify_id, track_name, track_spotify_uri ,track_spotify_url) VALUES
(1, 'track_001', 'Song One', 'track uri' ,'https://open.spotify.com/track/track_001'),
(1, 'track_002', 'Song Two', 'track uri' ,'https://open.spotify.com/track/track_002'),
(1, 'track_003', 'Song Three', 'track uri' ,'https://open.spotify.com/track/track_003'),
(2, 'track_004', 'Chill Vibes', 'track uri' ,'https://open.spotify.com/track/track_004'),
(2, 'track_005', 'Relax Tune', 'track uri' ,'https://open.spotify.com/track/track_005')


-- Select users table
SELECT * FROM users

-- Select  playlist table
SELECT * FROM playlists

-- Select tracks table
SELECT * FROM tracks

-- Select all user's playlists
SELECT playlist_name, playlist_spotify_id, playlist_spotify_url, total_tracks
FROM playlists p
JOIN users u ON u.user_id = p.user_id
WHERE u.name = 'Alice'

-- Select all tracks belonging to a specific user's playlist
SELECT track_spotify_id, track_spotify_name, track_spotify_url
FROM tracks t
JOIN playlists p ON t.playlist_id = p.playlist_id
JOIN users u ON p.user_id = u.user_id
WHERE u.name = 'Alice' AND p.playlist_name = 'Alice Chill'

-- Check if a user exist
SELECT EXISTS (
    SELECT 1 FROM users WHERE users.email = 'rich@rich.com'
)

-- Check if a track belongs to a playlist
SELECT EXISTS (
    SELECT 1 FROM tracks t
    JOIN playlists p ON t.playlist_id = p.playlist_id
    JOIN users u ON p.user_id = u.user_id
    WHERE u.name = 'Alice' AND p.playlist_name = 'Alice Chill' AND t.track_name = 'Chill Vibes'
)

-- Check if a playlist exist
SELECT EXISTS (
    SELECT 1 FROM playlists p
    JOIN users u ON u.user_id = p.user_id
    WHERE u.name = 'Alice' AND p.playlist_name = 'Alice Chill'
)

SELECT user_spotify_id from users
WHERE users.email = 'rich@rich.com'



