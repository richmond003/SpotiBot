import requests

""" 
get user's profile 
https://api.spotify.com/v1

get all user's playlists
https://api.spotify.com/v1/me/playlists

check all users saved track
https://api.spotify.com/v1/me/tracks

create playlist
https://api.spotify.com/v1/users/{user_id}/playlists
json {
    "name": "New Playlist",
    "description": "New playlist description",
    "public": false
}

add items to playlist
https://api.spotify.com/v1/playlists/{playlist_id}/tracks
{
    "uris": [
        "string"
    ],
    "position": 0
}
 """

class Api():
    # BASEURL = 'https://api.spotify.com/v1/me'
    def __init__(self, token):
        self.token = token
        self.BASEURL = 'https://api.spotify.com/v1'
        self.headers = {
            'Authorization': f"Bearer {self.token}",
            'Content-Type': "application/x-www-form-urlencoded"
        }
    def user_profile(self):
        try:
            endpoint = f'{self.BASEURL}/me'
            res = requests.get(url=endpoint, headers= self.headers)
            res.raise_for_status()
            data = res.json()
            return data
        except Exception as err:
            print(f"Error from API (user_profile): {err}")
    
    def playlists(self, next_ptr=None):
        try:
            endpoint = next_ptr or f"{self.BASEURL}/me/playlists"
            res = requests.get(url=endpoint, headers=self.headers)
            res.raise_for_status()
            data = res.json()
            return data
        except:
            print(f"Error from API (playlist)")
    
    def tracks(self, next_ptr=None):
        try:
            endpoint = next_ptr or f"{self.BASEURL}/me/tracks?limit=50"
            res = requests.get(url= endpoint , headers=self.headers)
            res.raise_for_status()
            data = res.json()
            return data
        except Exception as err:
            print(f"Error from API (tracks): {err}")
    
    
    def post_playlist(self, user_id, data):
        try:
            endpoint = f"{self.BASEURL}/users/{user_id}/playlists"
            res = requests.post(url=endpoint, headers=self.headers, json=data)
            res.raise_for_status()
            stauts_code = res.status_code
            if stauts_code == 201:
                data = res.json()
                return data
            else:
                
                return {}, False
        except Exception as err:
            print(f"Error from API (post_playlist): {err}")

    def add_items(self, playlist_id, data):
        try:
            endpoint = f"{self.BASEURL}/playlists/{playlist_id}/tracks"
            res = requests.post(url=endpoint, headers=self.headers, json=data)
            res.raise_for_status()
            data = res.json()
            return data
        except Exception as err:
            print(f"Error from (add_items): {err}")
    
    def get_playlist(self, playlist_id):
        try:
            """ 
                https://api.spotify.com/v1/playlists/{playlist_id} 
            """
            endpoint = f"{self.BASEURL}/playlists/{playlist_id}"
            res = requests.get(url=endpoint, headers=self.headers)
            res.raise_for_status()
            data = res.json()
            return data
        except Exception as err:
            print(f"Error from API (get_playlist): {err}")
    
