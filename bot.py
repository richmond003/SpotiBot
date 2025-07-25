from oauth_server import load_tokens
from spotify_api import Api
from time import sleep
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


def fetch_tracks(nxt_req=None):
    """ 
     fetch user tracks and also make tracks for next set of user tracks in API  
    """
    tracks = bot.tracks(nxt_req)
    next_set = tracks["next"]
    user_tracks = tracks["items"]
    return next_set, user_tracks

def get_user_tracks():
    """ 
    Get all user liked songs 
    """
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
    return saved_tracks

def create_playlist(user_id, artist):
    """ 
        Create new playlist for a specific artist 
    """
    schema = {
        "name" : f"Your {artist} Essentials",
        "description": f"Auto generated of your liked songs by {artist}. Playlist created and automated with @SpotiBot🤖",
        "public": "false"
    }
    new_playlist = bot.post_playlist(user_id, schema)
    return new_playlist

def add_tracks(tracks: list, spotify_id):
    """ Add new tracks to playlist """
    schema = {
        "uris": tracks,
        "position": 0
    }
    added_tracks = bot.add_items(spotify_id, schema)
    return added_tracks

def sorted_tracks():
    """ sort tracks data for easy manuplations """
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
        if val["apperance"] >= 5:
            sorted_tracks[key] = val["uris"]
    return sorted_tracks, tracks_info

def  main():
    try:
        user = bot.user_profile() 
        user_exists = db.check_for_user(user['email'])
        if not user_exists:
            new_user = (user["display_name"], user["email"], user['id'], user['href'], 0)
            user_id = db.insert_user(new_user)
        else:
            user_id= db.select_user(user['email'])
        
        liked_tracks, tracks_info = sorted_tracks()
        for  artist, tracks in liked_tracks.items():
            new_tracks = []
            playlist_id, spotify_id = db.select_playlist(user["email"], artist)
            if not playlist_id:
                new_playlist = create_playlist(user["id"], artist)
                sleep(0.2) 
                new_playlist_data = (
                    user_id, 
                    new_playlist["name"], 
                    artist, 
                    new_playlist["id"],
                    new_playlist["external_urls"]["spotify"],
                    len(tracks)
                    )
                playlist_id, spotify_id = db.add_playlist(new_playlist_data)
            else:
                playlist_tracks = db.select_all_tracks(user["email"], playlist_id)

                for track in tracks:
                    if track in playlist_tracks:
                        continue
                    else:
                        new_tracks.append(track)

            if new_tracks:
                added_tracks = add_tracks(new_tracks, spotify_id) # add new tracks to spotify playlist

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
                    data = (playlist_id, track_key["id"], track_key["title"], track, track_key["url"])
                    db.insert_track(data)

    except Exception as err:
        print(f"Error from bot: {err}")


if __name__ == "__main__":
    main()









