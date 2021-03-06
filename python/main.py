#I can't figure out how to get requests imported on a normal computer, only on replit
#So this code won't work outside of replit for now
import requests
import datetime
import base64
from urllib.parse import urlencode

client_id = SPOTIFY_CLIENT_ID
client_secret = SPOTIFY_CLIENT_SECRET

class SpotifyAPI(object):
  access_token = None
  access_token_expires = datetime.datetime.now()
  access_token_did_expire = True
  client_id = None
  client_secret = None
  token_url = "https://accounts.spotify.com/api/token"

  def __init__(self, client_id, client_secret, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.client_id = client_id
    self.client_secret = client_secret

  def get_client_credentials(self):
    """
    Returns a base64 encoded string
    """
    client_id = self.client_id
    client_secret = self.client_secret
    if client_id == None or client_secret == None:
      raise Exception("You must set client id and client secret")
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    return client_creds_b64.decode()

  def get_token_headers(self):
    client_creds_b64 = self.get_client_credentials()
    return {
      "Authorization": f"Basic {client_creds_b64}"
    }

  def get_token_data(self):
    return {
      "grant_type": "client_credentials"
    }

  # Recieves+defines access token to use for requests
  def perform_auth(self): 
    token_url = self.token_url
    token_data = self.get_token_data()
    token_headers = self.get_token_headers()
    r = requests.post(token_url, data=token_data, headers=token_headers)
    print(r.json())
    if r.status_code not in range(200, 299):
      return False

    # Handling response data
    data = r.json()
    now = datetime.datetime.now()
    access_token = data.get("access_token")
    expires_in = data.get("expires_in")
    expires = now + datetime.timedelta(seconds=expires_in)
    self.access_token = access_token
    self.access_token_expires = expires
    self.access_token_did_expire = expires < now
    return True

spotify = SpotifyAPI(client_id, client_secret)
spotify.perform_auth()
access_token = spotify.access_token

#Searching for a track
track = input("Enter the Spotify link to a song: ")
trackID = track[31:53]

headers = {
  "Authorization": f"Bearer {access_token}"
}
endpoint = "https://api.spotify.com/v1/tracks"
lookup_url = f"{endpoint}/{trackID}?market=US"
r = requests.get(lookup_url, headers=headers)
songData = r.json()
songName = songData.get("name")
songAlbumData = songData.get("album")
songArtistData = songAlbumData.get("artists")
songArtist = songArtistData[0].get("name")

print("That's the link to",songName,"by",songArtist,"!")