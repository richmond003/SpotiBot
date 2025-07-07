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
            INSERT INTO users (name, email, spotify_id, spotify_url, total_playlist)
            VALUES(%s, %s, %s, %s, %s)
            RETURNING id
            """, data
            )
            self.conn.commit()
            results = self.cur.fetchall()
            return results[0]
        except Exception as err:
            print(f"Error: {err}")

    def insert_playlist(self, data):
        try:
            self.cur.execute("""
            INSERT INTO playlists (id, playlist_name, playlist_id, playlist_link, total_tracks) 
            VALUES(%s, %s, %s, %s, %s)
            RETURNING *
            """, data
            )
            self.conn.commit()
            results = self.cur.fetchall()
            return results
        except Exception as err:
            print(f"Error: {err}")

    def insert_track(self, data):
        try:
            self.cur.execute("""
            INSERT INTO tracks (id, track_id, track_name, track_link) 
            VALUES(%s, %s, %s, %s)
            """, data
            )
            self.conn.commit()
            results = self.cur.fetchall()
            return results
        except Exception as err:
            print(f"Error: {err}")
    
    def select_playlist(self, user, artist):
        try:
            self.cur.execute(""" 
            SELECT playlist_name, playlist_id, playlist_link, total_tracks 
            FROM playlists p 
            JOIN users u ON u.id = p.id 
            WHERE u.email = %s AND p.artist = %s
            """ , (user,artist)
            )
            # self.conn.commit()
            results = self.cur.fetchall()
            return results
        except Exception as err:
            print(f"Error: {err}")

    def select_user(self, email):
        try:
            self.cur.execute(""" 
                SELECT id FROM users u
                WHERE u.email = %s 
             """, (email,))
            results = self.cur.fetchone()
            return results
        except Exception as err:
            print(f"An error occured: {err}")

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
            print(f"Error: {err}")


    def check_track(self, data):
        try:
            self.cur.execute(""" 
                SELECT EXISTS(
                    SELECT 1 FROM tracks t
                    JOIN playlists p ON t.id = p.entry_id
                    JOIN users u ON p.id = u.id
                    WHERE u.email = %s AND p.id = %s AND t.track_name = %s
                )
             """, data)
            results = self.cur.fetchone()
            return results[0]
        except Exception as err:
            print(f"Error: {err}")

    def check_playlist_exist(self, data):
        try:
            self.cur.execute(""" 
                SELECT EXISTS(
                    SELECT 1 FROM playlists p
                    JOIN users u ON u.id = p.id
                    WHERE u.email = %s AND p.artist = %s
                )
            """, data)
            results = self.cur.fetchone()
            return results[0]
        
        except Exception as err:
            print(f"Error: {err}")

    def close(self):
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    testDB = PostgresDB()
    data = ('Alice', 'Alice Chill', 'Chill Vibes')
    new_user = ("Testing", "test@example.com", "spotify12345", "https://dumylink", 0)
    # user = testDB.check_track_exist(data)
    user = testDB.select_user("bob@example.com")
    print(f"user: {user}")
    testDB.close()

