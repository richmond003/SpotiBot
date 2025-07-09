from oauth_server import app, load_tokens
from spotify_api import Api
from pathlib import Path
from database import PostgresDB
from collections import defaultdict
import json
import os

USER_TOKEN_PATH = './user_token.json'
token_exist = os.path.exists(USER_TOKEN_PATH)
if not(token_exist):
    raise Exception("Token doesn't exist yet. Check oauth or redirect url to http://localhost:8888/refresh")

db = PostgresDB()
token = load_tokens()["access_token"]
bot = Api(token=token)

def save_user(user):
    """
        Save or add new user data in json formate 
    """
    try:
        user_exists = db.check_for_user(user['email'])
        if user_exists:
            return
        new_user = (user["display_name"], user["email"], user['id'], user['href'], 0)
        db.insert_user(new_user)

    except Exception as err:
        print(f"Error: {err}")
    finally:
        print("Done") 

def get_bot_playlists():
    playlists = bot.playlists()
    next_set = playlists["next"]
    items = playlists["items"]
    all_playlist = [playlist["id"] for playlist in items]
    while next_set:
        playlists = bot.playlists(next_set)
        next_set = playlists['next']
        items = playlists["items"]
        for playlist in items:
            playlist_id = playlist['id']
            all_playlist.append(playlist_id)
    #TODO: Sort and return all playlist created by spotibot
    print(f"All playlist ID: {all_playlist}")

def fetch_tracks(nxt_req=None):
    """ 
     request for user tracks and also make tracks for next set of user tracks  
    """
    tracks = bot.tracks(nxt_req)
    next_set = tracks["next"]
    user_tracks = tracks["items"]
    return next_set, user_tracks

def get_user_tracks():
    saved_tracks = []
    next_set, user_tracks = fetch_tracks()
    req_calls = 1
    while True:
        for track in user_tracks:
            track_data = {
                "title": track["track"]["name"],
                "id": track["track"]['id'],
                "uri": track["track"]["uri"],
                "link": track["track"]['href'],
                "artists": [artist["name"] for artist in track["track"]["artists"]]
                }
            saved_tracks.append(track_data)
        if not(next_set):
            """ Break loop when next is null """
            break

        next_set, user_tracks = fetch_tracks(nxt_req=next_set)
        req_calls +=1
    print(f"Calls: {req_calls}")
    with open('tracks.json', 'w') as tracks:
        json.dump(saved_tracks, tracks, indent=3)
    return saved_tracks

def create_playlist(user_id, artist):
    schema = {
        "name" : f"My {artist} Vibes❤️",
        "description": f"Auto generated of your liked songs by {artist}. Playlist created and automated with @SpotiBot🤖",
        "public": False
    }
    new_playlist = db.post_playlist(user_id, schema)
    return new_playlist
    
def save_track():
    pass

def post_tracks(tracks):
    pass


def  main():
    """ 
        create playist accroding to user liked songs by artist 
    """
    try:
        user = bot.user_profile()
        print(f"User info: {user}")
        user_exists = db.check_for_user(user['email'])
        tracks_ready = defaultdict(list)
        #  add user to db in user not in db
        if not user_exists:
            new_user = (user["display_name"], user["email"], user['id'], user['href'], 0)
            user_id = db.insert_user(new_user)
        else:
            user_id= db.select_user(user['email'])
            

        all_tracks = get_user_tracks()
        for track in all_tracks:
            for artist in track["artists"]:
                # check in playlist is created
                playlist_exist = db.check_playlist_exist(user["email"], artist)
                if not playlist_exist:
                    # call create playlist 
                    new_playlist = create_playlist(user_id=user["id"], artist= artist)
                    # insert new playlist into db if no errors
                    if new_playlist: playlist_id = db.insert_playlist(user_id, new_playlist["name"], artist, new_playlist["id"], new_playlist["href"], 0)
                    print(f"New playlist id: {playlist_id}")
                else:
                    playlist_id = db.select_playlist(email=user["email"], artist=artist)

                # check whether track is already in playlist
                track_data = (user["email"], playlist_id, track["id"])
                track_exist = db.check_track(track_data)
                # call insert track function
                if track_exist:
                    continue
                else:
                    #post track to spotify
                    # if len(tracks_ready[spotify_id]) < 100 : tracks_ready[spotify_id].append(uri)
                    pass
   
    except Exception as err:
        print(f"An error occured: {err}")




if __name__ == "__main__":
    # main()
    get_user_tracks()







""" 
user tracks:
artist{name, uri, href} loop
name, id, href, uri 

{
    "name": "New Playlist", artist 
    "description": "New playlist description",
    "public": false
}
"""

