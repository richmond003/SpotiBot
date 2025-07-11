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
        endpoint = f'{self.BASEURL}/me'
        res = requests.get(url=endpoint, headers= self.headers)
        res.raise_for_status()
        data = res.json()
        return data
    
    def playlists(self, next_ptr=None):
        endpoint = next_ptr or f"{self.BASEURL}/me/playlists"
        res = requests.get(url=endpoint, headers=self.headers)
        res.raise_for_status()
        data = res.json()
        return data
    
    def tracks(self, next_ptr=None):
        endpoint = next_ptr or f"{self.BASEURL}/me/tracks?limit=50"
        res = requests.get(url= endpoint , headers=self.headers)
        res.raise_for_status()
        data = res.json()
        return data
    
    def post_playlist(self, user_id, data):
        endpoint = f"{self.BASEURL}/users/{user_id}/playlists"
        res = requests.post(url=endpoint, headers=self.headers, json=data)
        res.raise_for_status()
        stauts_code = res.status_code
        if stauts_code == 201:
            data = res.json()
            return data
        else:
            
            return {}, False

    def add_items(self, playlist_id, data):
        endpoint = f"{self.BASEURL}/playlists/{playlist_id}/tracks"
        res = requests.post(url=endpoint, headers=self.headers, json=data)
        res.raise_for_status()
        data = res.json()
        return data
    
    def get_playlist(self, playlist_id):
        """ 
            https://api.spotify.com/v1/playlists/{playlist_id} 
        """
        endpoint = f"{self.BASEURL}/playlists/{playlist_id}"
        res = requests.get(url=endpoint, headers=self.headers)
        res.raise_for_status()
        data = res.json()
        return data
    
  
    """ 
     new_playlist = {
    "name" : "{artist}",
    "description": "Auto generated playlist of your liked songs by {artist}.\n Automated with SpotiBot",
    "publc": "false"
}
      
    """
