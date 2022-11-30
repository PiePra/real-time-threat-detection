import streamlit as st
import pathlib
class load_css():
    def __init__(self):
        ""
    @staticmethod
    def read_css():
    #load css from static
        #streamlit_static_path = pathlib.Path(st.__path__[0])/ 'static'      
        css_path = ("static/style.css")
        with open(css_path) as f:
            st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
        
        
