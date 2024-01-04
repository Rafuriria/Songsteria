import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av 
import cv2 
import numpy as np 
import mediapipe as mp 
from keras.models import load_model
#import webbrowser
from streamlit.components.v1 import html
import spotipy
#import sys
from spotipy.oauth2 import SpotifyOAuth


st.markdown("# Music Recommendation Based on Facial 🎈")
st.sidebar.markdown("# Music Recommendation Based on Facial 🎈")

model  = load_model("model.h5")
label = np.load("labels.npy")
holistic = mp.solutions.holistic
hands = mp.solutions.hands
holis = holistic.Holistic()
drawing = mp.solutions.drawing_utils
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    	client_id='9434f485c5454c4d8110520b423d28cb',
    	client_secret='b946229d374f4655a44f1a2646503a97',
    	redirect_uri='https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF',
    	scope='user-read-playback-state user-modify-playback-state'
	))

#to detect the emotion from the user facial

if "run" not in st.session_state:
	st.session_state["run"] = "true"

try:
	emotion = np.load("emotion.npy")[0]
except:
	emotion=""

if not(emotion):
	st.session_state["run"] = "true"
else:
	st.session_state["run"] = "false"

class EmotionProcessor:
	def recv(self, frame):
		frm = frame.to_ndarray(format="bgr24")

		##############################
		frm = cv2.flip(frm, 1)

		res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

		lst = []

		if res.face_landmarks:
			for i in res.face_landmarks.landmark:
				lst.append(i.x - res.face_landmarks.landmark[1].x)
				lst.append(i.y - res.face_landmarks.landmark[1].y)

			if res.left_hand_landmarks:
				for i in res.left_hand_landmarks.landmark:
					lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
					lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
			else:
				for i in range(42):
					lst.append(0.0)

			if res.right_hand_landmarks:
				for i in res.right_hand_landmarks.landmark:
					lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
					lst.append(i.y - res.right_hand_landmarks.landmark[8].y)
			else:
				for i in range(42):
					lst.append(0.0)

			lst = np.array(lst).reshape(1,-1)

			pred = label[np.argmax(model.predict(lst))]

			print(pred)
			cv2.putText(frm, pred, (50,50),cv2.FONT_ITALIC, 1, (255,0,0),2)

			np.save("emotion.npy", np.array([pred]))

			
		drawing.draw_landmarks(frm, res.face_landmarks, holistic.FACEMESH_TESSELATION,
								landmark_drawing_spec=drawing.DrawingSpec(color=(0,0,255), thickness=-1, circle_radius=1),
								connection_drawing_spec=drawing.DrawingSpec(thickness=1))
		drawing.draw_landmarks(frm, res.left_hand_landmarks, hands.HAND_CONNECTIONS)
		drawing.draw_landmarks(frm, res.right_hand_landmarks, hands.HAND_CONNECTIONS)


		##############################

		
		return av.VideoFrame.from_ndarray(frm, format="bgr24")



lang = st.selectbox(
   "Language:",
   ("English", "Malay", "Korean", "Japan","Chinese", "Others"),
   index=None,
   placeholder="Song Language",
)

#st.write('You selected:', option)

artist = st.text_input("Artist Name")

if artist and st.session_state["run"] != "false":
	webrtc_streamer(key="key", desired_playing_state=True,
				video_processor_factory=EmotionProcessor)

btn = st.button("Start Video")

track_url = ""

if btn:
	if not(emotion):
		st.warning("Please let me capture your emotion first")
		st.session_state["run"] = "true"
else:
        emotion_to_track_uri = {
            "Happy": "SPOTIFY_PLAYLIST_URI_FOR_HAPPY",
            "Sad": "SPOTIFY_PLAYLIST_URI_FOR_SAD",
            "Panic": "SPOTIFY_PLAYLIST_URI_FOR_PANIC",
            "Neutral": "SPOTIFY_PLAYLIST_URI_FOR_NEUTRAL",
            "Annoyed": "SPOTIFY_PLAYLIST_URI_FOR_ANNOYED"
        }


# Check if track_url is not empty before embedding the player
if track_url:
    # Generate HTML code for the embedded player
    track_url_parts = track_url.split(':')
    if len(track_url_parts) >= 3:
        track_id = track_url_parts[2]
        track_url = f"https://open.spotify.com/embed/track/{track_id}"

        # Add the 'autoplay' attribute to the <iframe> element
        player_code = f'<iframe src="{track_url}" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media" autoplay></iframe>'

        # Embed the player in Streamlit
        html_code = f'<div>{player_code}</div>'
        html(html_code)