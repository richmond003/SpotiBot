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
CIIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRETE")
REDIRECT_URL = os.getenv("SPOTIFY_REDIRECT_URI")
SCOPE= "user-library-read playlist-modify-private playlist-modify-public"


app = Flask(__name__)

TOKENS_PATH = 'spotify_tokens.json'

def save_tokens(data):
    with open(TOKENS_PATH, 'w') as file:
        json.dump(data, file)

def load_tokens():
    if os.path.exists(TOKENS_PATH):
        return json.load(open(TOKENS_PATH))
    return {}

@app.route('/')
def login():
    params = {
        'client_id': CLIENT_ID,
        'response_type': "code",
        "redirect_uri": REDIRECT_URL,
        "scope": SCOPE
    }
    url = f"https://accounts.spotify.com/authorize?{urlencode(params)}"
    return redirect(url)
@app.route("/callback")
def callback():
    #spotify redirects here with code ?code=AUTH_CODE
    code = request.args.get("code")

    # check if code was recieved
    if not code:
        print("missing code")
        return "Missing code", 400
    
    #Exchange code for tokens
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URL,
    }

    auth_header = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_ID)

    res = requests.post(token_url, data=payload, auth=auth_header)
    
    print("This is the token data: ", res.json())
    tokens = res.json()
    save_tokens(tokens)
    return "Authentication successfull! You can close this window."

if __name__ == "__main__":
    app.run(port=8888)