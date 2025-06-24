import os
import json
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv
from flask import Flask, redirect, request
import requests.auth

# load env variables here
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRETE")
REDIRECT_URL = os.getenv("SPOTIFY_REDIRECT_URI")
SCOPE= "user-library-read playlist-modify-private playlist-modify-public"
URL = "https://accounts.spotify.com/"
TOKENS_PATH = "user_token.json"
app = Flask(__name__)

def save_tokens(token):
    with open(TOKENS_PATH, 'w') as file:
        json.dump(token, file, indent=3)

def load_tokens():
    if os.path.exists(TOKENS_PATH):
        return json.load(open(TOKENS_PATH))
    return {}

@app.route('/')
def login():
    endpoint = 'authorize?'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': SCOPE,
        'redirect_uri': REDIRECT_URL
    }
    url = URL + endpoint + urlencode(params)
    return redirect(url)

@app.route('/callback')
def callback():
    endpoint = "api/token"
    url = URL + endpoint
    code = request.args.get('code')
    if not code:
        print(code)
        return "Missing code", 400
    payload = {
        'grant_type': "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URL
    }
    auth_header = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    res = requests.post(url=url, data=payload, auth=auth_header)
    if res.raise_for_status():
        return "Authentication failed"
    tokens =  res.json()
    save_tokens(tokens)
    return "You are all set and ready to go. You can close the page now😉"
    
@app.route("/refresh")
def refresh():
    endpoint = 'api/token'
    url = URL + endpoint
    old_tokens = load_tokens()["refresh_token"]
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": old_tokens,
        "client_id": CLIENT_ID
    }
    auth_header = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    res = requests.post(url=url, data=payload, auth=auth_header)

    if res.raise_for_status():
        return "An error occured"
    
    new_tokens = res.json()
    
    new_tokens["refresh_token"] = new_tokens.get("refresh_token",old_tokens)
    save_tokens(new_tokens)
    return "Token sucessfully refreshed"
    
if __name__ == "__main__":
    app.run(port=8888, debug=True)


