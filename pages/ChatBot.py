import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = '9434f485c5454c4d8110520b423d28cb'
SPOTIPY_CLIENT_SECRET = 'b946229d374f4655a44f1a2646503a97'
SPOTIPY_REDIRECT_URI = 'http://localhost:8501/callback'

#cari local host laptop 

# Set up Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='user-modify-playback-state user-read-playback-state'))

# Streamlit UI
st.title("Music Chatbot")

# Function to play a specific track
#cari server utk bg spotify to play
def play_track(track_name):
    results = sp.search(q=track_name, type='track', limit=1)
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[track_uri])
        st.success(f"Now playing: {track_name}")
    else:
        st.error(f"Sorry, couldn't find a track with the name: {track_name}")

# Get user input for a track
user_input = st.text_input("Ask for a song:")
if user_input:
    play_track(user_input)

# Streamlit callback to check user well-being after a song
if st.button("Finish Song"):
    # You can add more advanced well-being checks here
    st.write("How are you feeling after the song?")

# Run the Streamlit app
#if __name__ == '__main__':
#    st.run_app()
