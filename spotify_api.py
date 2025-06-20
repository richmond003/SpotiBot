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

class Spotify_Api():
    BASEURL = 'https://api.spotify.com/v1/me'
    def __init__(self, token):
        self.token = token
        self.BASEURL = 'https://api.spotify.com/v1/me'
        self.headers = {
            'Authorization': f"Bearer {self.token}",
            'Content-Type': "application/x-www-form-urlencoded"
        }
    def user_profile(self):
        res = requests.get(url=self.BASEURL, headers= self.headers)
        res.raise_for_status()
        data = res.json()
        return data
    
    def playlists(self):
        endpoint = f"{self.BASEURL}/me/playlists"
        res = requests.get(url=endpoint, headers=self.headers)
        res.raise_for_status()
        data = res.json()
        return data
    
    def tracks(self):
        endpoint = f"{self.BASEURL}me/tracks"
        res = requests.get(url= endpoint , headers=self.headers)
        res.raise_for_status()
        data = res.json()
        return data
    
    def create_playlist(self, user_id, data):
        endpoint = f"{self.BASEURL}/users/{user_id}/playlists"
        res = requests.post(url=endpoint, headers=self.headers, data=data)
        res.raise_for_status()
        data = res.json()
        return data

    def add_items(self, playlist_id, data):
        endpoint = f"{self.BASEURL}/playlists/{playlist_id}/tracks"
        res = requests.post(url=endpoint, headers=self.headers, data=data)
        res.raise_for_status()
        data = res.json()
        return data
    
    def update_playlist(self):
        pass