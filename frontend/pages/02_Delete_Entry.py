from helper import *
import streamlit as st
import pathlib
from PIL import Image

data = ""
# load css and page design
load_css.read_css()
#streamlit_static_path = pathlib.Path(st.__path__[0])/ 'static'
#print(streamlit_static_path)
logo_path = "static/logo.jpg"
image = Image.open(logo_path)
st.sidebar.image(image, use_column_width = True,)
st. sidebar.info("Team: Gold Digger")
st.write(""" # Delete Warnings And Alerts """)

with st.form("my_form2"):
    input = st.text_input("Enter user id to delete warning or alert.", key = "text")
    submitted = st.form_submit_button("Submit")

if submitted:
  while data == "":
    placeholder = st.info("Loading")