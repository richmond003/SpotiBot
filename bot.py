from oauth_server import app, load_tokens
from spotify_api import Api
from pathlib import Path
import json
import os

USER_TOKEN_PATH = './user_token.json'
token_exist = os.path.exists(USER_TOKEN_PATH)


get_token = load_tokens()["access_token"]
bot = Api(token=get_token)
user_id = bot.user_profile()["id"]

def save_user(new_data: dict):
    """
        Save or add new user data in json formate 
    """
    try:
        data = {} 
        if os.path.exists(USER_DATA_PATH):
            with (USER_DATA_PATH, 'r') as file:
                data = json.load(file)
        else:
            data = {}
        data.append(new_data)
        with open(USER_DATA_PATH, 'w') as file:
            json.dump(data, file, indent=4)
    except:
        print("Error occured")
    finally:
        print("Done") 

def fetch_tracks(nxt_req=None):
    """ 
     request for user tracks and also make tracks for next set of user tracks  
    """
    tracks = bot.tracks(nxt_req)
    next_set = tracks["next"]
    user_tracks = tracks["items"]
    return next_set, user_tracks

def  playlist_by_artist(bot, id, artist):
    """ 
        create playist accroding to user liked songs by artist 
    """
    for artist in artist:
        #TODO: check if artists playlist is already before creating a new playlist
        create_playlist = {
            "name" : artist,
            "description": f"Auto generated of your liked song by {artist}.\n Automated with @SpotiBot🤖",
            "public": "false"
        }

        created_playlist = bot.create_playlist(user_id=id, data=create_playlist)
        if created_playlist: #TODO: handle create_playist() to return true/false if rquest went through or not
            new_playlist = {
                "name": create_playlist["name"],
                "id": created_playlist["id"],
                "owner_id": created_playlist["owner"]["id"],
                "tracks_limit": created_playlist["tracks"]["limit"],
                "total_tracks": created_playlist["tracks"]["total"]
            }
            #TODO: put or add new playlist in database/json file
        else:
            raise Exception("An error occured with request")

def get_all_playlist():
    pass

def add_tracks_playlist():
    pass

def get_user_tracks():
    track_archives = {}
    next_set, user_tracks = fetch_tracks()
    req_calls = 1
    while next_set != None:
        for track in user_tracks:
            track_archives[track["track"]["name"]] = {
                "id": track["track"]['id'], 
                "link": track["track"]['href'],
                "artists": [artist["name"] for artist in track["track"]["artists"]]
                }  
        next_set, user_tracks = fetch_tracks(nxt_req=next_set)
        req_calls +=1
    print(f"Calls: {req_calls}")
    return track_archives
















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

