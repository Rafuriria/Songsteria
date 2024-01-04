import streamlit as st

from streamlit_option_menu import option_menu

import Song, request_page
st.set_page_config(
page_title="SONGSTERIA",
)

class MutliApp:
    def _init_(self):
        self.apps = []
    def add_app(self,title,function):
        self.apps.append({
            "title": title,
            "function": function
        })
    def run() :

        with st.sidebar:
            app = option_menu(
                menu_title= 'SONGSTERIA',
                options=['Music Recommendation','Chatbot'],
                #icons=
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "18px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},
                }

            )
        
        if app=='Music Recommendation' :
            Song.app()
        if app=='Chatbot' :
            request_page.app()   

    run() 