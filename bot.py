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
                "link": track["track"]['external_urls']["spotify"],
                "artists": [artist["name"] for artist in track["track"]["artists"]]
                }
            saved_tracks.append(track_data)
        if not(next_set): break

        next_set, user_tracks = fetch_tracks(nxt_req=next_set)
        req_calls +=1
    print(f"Calls: {req_calls}")
    with open('tracks.json', 'w') as tracks:
        json.dump(saved_tracks, tracks, indent=3)
    return saved_tracks

def create_playlist(user_id, artist):
    schema = {
        "name" : f"Your {artist} Vibes❤️",
        "description": f"Auto generated of your liked songs by {artist}. Playlist created and automated with @SpotiBot🤖",
        "public": False
    }
    new_playlist = db.post_playlist(user_id, schema)
    return new_playlist

def add_tracks(tracks: list, spotify_id):
    schema = {
        "uris": tracks,
        "position": 0
    }
    added_tracks = bot.add_items(spotify_id, schema)
    return added_tracks

def sorted_tracks():
    liked_tracks = get_user_tracks()
    originsed_tracks = defaultdict(lambda : {"apperance": 0, "uris": []})
    sorted_tracks = {}
    tracks_info = defaultdict(lambda : {"id": "", "title" : "", "url": ""})
    for track in liked_tracks:
        tracks_info[track["uri"]]["id"] = track["id"]
        tracks_info[track["uri"]]["title"] = track["title"]
        tracks_info[track["uri"]]["url"] = track["link"]

        for artist in track["artists"]:
            originsed_tracks[artist]["apperance"] += 1
            originsed_tracks[artist]["uris"].append(track["uri"])

    for key, val in originsed_tracks.items():
        if val["apperance"] >= 3:
            sorted_tracks[key] = val["uris"]
    return sorted_tracks, tracks_info

def  main():
    """ 
        create playist accroding to user liked songs by artist 
    """
    try:
        user = bot.user_profile()
        print(f"User info: {user}")
        user_exists = db.check_for_user(user['email'])
        #  add user to db in user not in db
        if not user_exists:
            new_user = (user["display_name"], user["email"], user['id'], user['href'], 0)
            user_id = db.insert_user(new_user)
        else:
            user_id= db.select_user(user['email'])
        
        liked_tracks, tracks_info = sorted_tracks()
        for  artist, tracks in liked_tracks.items():
            playlist_id, spotify_id = db.select_playlist(user["email"], artist)

            if not playlist_id:
                new_playlist = create_playlist(user["id"], artist)
                new_playlist_data = (
                    user_id, 
                    new_playlist["title"], 
                    artist, 
                    new_playlist["id"],
                    new_playlist["external_urls"]["spotify"],
                    len(tracks)
                    )
                playlist_id, spotify_id = db.add_playlist(new_playlist_data)
            else:
                new_tracks = []
                playlist_tracks = db.select_all_tracks(user["email"], playlist_id)
                for track in tracks:
                    if track in playlist_tracks:
                        continue
                    else:
                        new_tracks.append(track)
                        pass

            if new_tracks:
                added_tracks = add_tracks(new_tracks, spotify_id)
                # insrt into db
                if added_tracks:
                    for track in new_tracks:
                        track_key = tracks_info[track]
                        data = (playlist_id, track_key["id"], track_key["title"], track, track_key["url"])
                        db.insert_track(data)
            else:
                added_tracks = add_tracks(tracks, spotify_id)
                #insert into 
                for track in tracks:
                    track_key = tracks_info[track]
                    data = (playlist_id, track["id"], track_key["title"], track, track_key["url"])
                    db.insert_track(data)

   
    except Exception as err:
        print(f"An error occured: {err}")




if __name__ == "__main__":
    # main()
    get_user_tracks()








