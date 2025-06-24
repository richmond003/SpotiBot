from oauth_server import app, load_tokens
from spotify_api import Api
from pathlib import Path
import json
import os

USER_DATA_PATH = './users_data.json'
token_exist = os.path.exists(USER_DATA_PATH)
track_archives = {}

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
    user_tracks = track["items"]
    return tracks, next_set, user_tracks

def  playlist_by_artist(bot, id, artist):
    """ 
        create playist accroding to user liked songs by artist 
    """
    for artist in artist:
        #TODO: check if artists playlist is already before creating a new playlist
        new_playlist = {
            "name" : artist,
            "description": f"Auto generated of your liked song by {artist}",
            "public": "false"
        }

        is_created = bot.create_playlist(user_id=id, data=new_playlist)
        if is_created: #TODO: handle create_playist() to return true/false if rquest went through or not
            continue
        else:
            raise Exception("An error occured with request")

def add_songs_playlist():
    pass

    
if (token_exist):
    get_token = load_tokens()["access_token"]
    bot = Api(token=get_token)
    user_id = bot.user_profile()["id"]

    """ # get first set of user track data
    tracks = bot.tracks()
    #get the next object if exist not null or none
    next_set = tracks["next"]
    # get item from the tracks data
    user_tracks = tracks["items"]
 """
    tracks, next_set, user_tacks = fetch_tracks()

    while next_set != None:
        for track in user_tracks["track"]:
            track_archives[track["name"]] = {
                "id": track['id'], 
                "link": track['href'],
                "artists": [artist["name"] for artist in track["track"]["artists"]]
                }
        """ tracks = bot.tracks(next_ptr=next_set)
        next_set = tracks["next"]
        user_tracks = tracks["items"] """

        tracks, next_set, user_tracks = fetch_tracks(nxt_req=next_set)
else:
    raise Exception("File does not exist yet. Check oauth server or json file")















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

