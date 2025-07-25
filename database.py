import psycopg2
from dotenv import load_dotenv
import os

class PostgresDB:
    def __init__(self):
        load_dotenv()
        PASSWORD = os.getenv("POSTGRESDB_PASSWORD")
        self.conn = psycopg2.connect(
            dbname = "SpotiBot_DB",
            user = 'postgres',
            password = PASSWORD,
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()

    def insert_user(self, data):
        try:
            self.cur.execute("""
            INSERT INTO users (name, email, user_spotify_id, user_spotify_url, total_playlist)
            VALUES(%s, %s, %s, %s, %s)
            RETURNING user_id
            """, data
            )
            self.conn.commit()
            results = self.cur.fetchone()
            return results[0]
        except Exception as err:
            print(f"Error from insert user db: {err}")

    def add_playlist(self, data):
        try:
            self.cur.execute("""
            INSERT INTO playlists (user_id, playlist_name, artist, playlist_spotify_id, playlist_spotify_url, total_tracks) 
            VALUES(%s, %s, %s, %s, %s, %s)
            RETURNING playlist_id, playlist_spotify_id 
            """, data
            )
            self.conn.commit()
            results = self.cur.fetchone()
            return results
        except Exception as err:
            print(f"Error from add playlist db: {err}")

    def insert_track(self, data):
        try:
            self.cur.execute("""
            INSERT INTO tracks (playlist_id, track_spotify_id, track_name, track_spotify_uri, track_spotify_url) 
            VALUES(%s, %s, %s, %s, %s)
            """, data
            )
            self.conn.commit()
            # results = self.cur.fetchall()
            # return results
        except Exception as err:
            print(f"Error from insert track db: {err}")
    
    def select_playlist(self, email, artist):
        try:
            self.cur.execute(""" 
            SELECT playlist_id, playlist_spotify_id
            FROM playlists p 
            JOIN users u ON u.user_id = p.playlist_id 
            WHERE u.email = %s AND p.artist = %s
            """ , (email, artist)
            )
            # self.conn.commit()
            results = self.cur.fetchone()
            if not results:
                return (None, None)
            return results
        except Exception as err:
            print(f"Error from select playlist db: {err}")

    def select_user(self, email):
        try:
            self.cur.execute(""" 
                SELECT user_id FROM users u
                WHERE u.email = %s 
             """, (email,))
            results = self.cur.fetchone()
            return results[0]
        except Exception as err:
            print(f"Error from select user db: {err}")

    def select_all_tracks(self, email ,playlist_id):
        try:
            self.cur.execute(""" 
                SELECT track_spotify_url FROM tracks t
                JOIN playlists p ON t.playlist_id = p.playlist_id
                JOIN users u ON u.user_id = p.user_id
                WHERE u.email = %s AND p.playlist_id = %s
            """, (email, playlist_id))
            results = self.cur.fetchall()
            flattend = list(zip(*results))[0]
            return list(flattend)
        except Exception as err:
            print(f"Error from select all tracks: {err}")

    def check_for_user(self, email):
        try:
            self.cur.execute("""
            SELECT EXISTS(
                SELECT 1 FROM users WHERE email = %s
            )
            """, (email,))
            results = self.cur.fetchone()
            return results[0]
        except Exception as err:
            print(f"Error from check all users: {err}")


    def check_track(self, email, playlist_id, track_uri):
        try:
            self.cur.execute(""" 
                SELECT EXISTS(
                    SELECT 1 FROM tracks t
                    JOIN playlists p ON t.playlist_id = p.playlist_id
                    JOIN users u ON p.user_id = u.user_id
                    WHERE u.email = %s AND p.playlist_id = %s AND t.track_spotify_id = %s
                )
             """, data)
            results = self.cur.fetchone()
            return results[0]
        except Exception as err:
            print(f"Error from check track: {err}")

    def check_playlist_exist(self, data):
        try:
            self.cur.execute(""" 
                SELECT EXISTS(
                    SELECT 1 FROM playlists p
                    JOIN users u ON u.user_id = p.user_id
                    WHERE u.email = %s AND p.artist = %s
                )
            """, data)
            results = self.cur.fetchone()
            return results[0]
                
        except Exception as err:
            print(f"Error from check playlist exist: {err}")

    def increace_playlist():
        try:
            pass
        except Exception as err:
            print(f"Error from increase_playlist: {err}")

    def close(self):
        self.cur.close()
        self.conn.close()


if __name__ == "__main__":
    testDB = PostgresDB()
    # new_user = ("Testing2", "test2@example.com", "spotify123425", "https://dumylink2", 0)
    user, checking = testDB.select_playlist('alice@example.com', 'mike')
    print(user)
    testDB.close()

