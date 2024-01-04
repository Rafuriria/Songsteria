import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av 
import cv2 
import numpy as np 
import mediapipe as mp
import json 
from keras.models import load_model
import webbrowser
from streamlit.components.v1 import html
import spotipy
#import sys
from spotipy.oauth2 import SpotifyOAuth, webbrowser


model  = load_model("model.h5")
label = np.load("labels.npy")
holistic = mp.solutions.holistic
hands = mp.solutions.hands
holis = holistic.Holistic()
drawing = mp.solutions.drawing_utils
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    	client_id='9434f485c5454c4d8110520b423d28cb',
    	client_secret='b946229d374f4655a44f1a2646503a97',
    	redirect_uri='https://open.spotify.com/',
    	scope='user-read-playback-state user-modify-playback-state'
	))
mood1 = 0.90  #happymood
mood2 = 0.07  #sadmood
mood3 = 0.10  #Panicmood
mood4 = 0.60  #Neutralmood
mood5 = 0.50  #Annoyedmood


# Define a function for each page
def home_page():
    st.title("Music Recommendation Based on User Emotion")
    # Add content for the home page

def request_page():
    st.title("Request Song")
    # Add content for the about page

def contact_page():
    st.title("Contact Page")
    # Add content for the contact page

# Create a dictionary to map page names to their respective functions
pages = {
    "Music Recommendation": home_page,
    "Request Song": request_page,
    "Contact": contact_page
}

# Create a sidebar or navigation bar to select the page
selected_page = st.sidebar.selectbox("Select a page", list(pages.keys()))

# Call the selected page function to display its content
if selected_page == "Music Recommendation":
    home_page()
elif selected_page == "Request Song":
    request_page()
elif selected_page == "Contact":
    contact_page()


#st.header("Music Recommendation Based on User Emotion")


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




genre = st.text_input("Genre")

if genre and st.session_state["run"] != "false":
	webrtc_streamer(key="key", desired_playing_state=True,
				video_processor_factory=EmotionProcessor)

btn = st.button("Recommend me songs")

track_url = "11dFghVXANMlKmJXsNCbNl"

if btn:
	if not(emotion):
		st.warning("Please let me capture your emotion first")
		st.session_state["run"] = "true"
	else:
		#webbrowser.open(f"https://open.spotify.com/search/{emotion}+{artist}")
		if emotion == 'Happy' and emotion == mood1 <= 1:
		   #try sort the artist, then track, then baru mood
		   webbrowser.open(f"https://open.spotify.com/{genre}+{emotion}/")		   
#elif emotion == 'sad' and emotion == mood2 < mood3:
		   #try sort the artist, then track, then baru mood
#		   webbrowser.open(f"https://open.spotify.com/{artist}+{emotion}/")
#elif emotion == 'Panic' and emotion == mood3 < mood4:
		   #try sort the artist, then track, then baru mood
#		   webbrowser.open(f"https://open.spotify.com/{artist}+{emotion}/")
#elif emotion == 'Neutral' and emotion == mood4 < mood1:
		   #try sort the artist, then track, then baru mood
#		   webbrowser.open(f"https://open.spotify.com/{artist}+{emotion}/")
#elif emotion == 'Annoyed' and emotion == mood5 < mood1:
		   #try sort the artist, then track, then baru mood
#			webbrowser.open(f"https://open.spotify.com/{artist}+{emotion}/")


np.save("emotion.npy", np.array([""]))
st.session_state["run"] = "false"
