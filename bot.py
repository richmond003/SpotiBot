from oauth_server import app, load_tokens
from spotify_api import Api
from pathlib import Path
from database import PostgresDB
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
    print(saved_tracks)
    with open('tracks.json', 'w') as tracks:
        json.dump(saved_tracks, tracks, indent=3)
    return saved_tracks

def create_playlist():
    schema = {
        "name" : f"{artist} Vibes❤️",
        "description": f"Auto generated of your liked song by {artist}.\n Playlist created and automated with @SpotiBot🤖",
        "public": "false"
    }
    new_playlist = db.post_playlist(user_id, schema)
    
def save_track():


def  main():
    """ 
        create playist accroding to user liked songs by artist 
    """
    try:
        
        user = bot.user_profile()

        user_exists = db.check_for_user(user['email'])
        #  add user to db in user not in db
        if not user_exists:
            new_user = (user["display_name"], user["email"], user['id'], user['href'])
            user_id = db.insert_user(new_user)
        else:
            user_id,  = db.select_user(user['email'])
            

        ###################################
        all_tracks = get_user_tracks()
        for track in all_tracks:
            for artists in track["artists"]:
                # check in playlist is created
                exist = db.check_playlist_exist(user["email"], artists)
                if not exist:
                    # call create playlist 
                    # inert track
                    pass
                else:
                    # check whether track is already in playlist
                    data = (user["email"], playlist_id, track_id)
                    track_exist = db.check_track()
                    # call insert track function
                    pass
    except Exception as err:
        print(f"An error occured: {err}")




if __name__ == "__main__":
    main()












""" 
#######  create platlist schema

------------------------------------------------------------------------
##### Create new bot playlist and add to database
create_playlist = bot.create_playlist(user_id=id, data=create_playlist)
        if create_playlist: #TODO: handle create_playist() to return true/false if rquest went through or not
            new_playlist = {
                "name": create_playlist["name"],
                "artist": "artist name"   NEW
                "id": created_playlist["id"],
                "owner_id": created_playlist["owner"]["id"],
                "link": "playlist href link"  NEW
                "tracks_limit": created_playlist["tracks"]["limit"],
                "total_tracks": created_playlist["tracks"]["total"]
            }
            #TODO: put or add new playlist in database/json file
        else:
            raise Exception("An error occured with request")

"""


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

