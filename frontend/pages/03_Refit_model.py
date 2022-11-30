from helper import *
import streamlit as st
import pathlib
from PIL import Image

data = ""
# load css and page design
load_css.read_css()
#streamlit_static_path = pathlib.Path(st.__path__[0])/ 'static'
logo_path = "static/logo.jpg"
image = Image.open(logo_path)
st.sidebar.image(image, use_column_width = True,)
st. sidebar.info("Team: Gold Digger")
st.write(""" # Refit Model """)

options = ["Login-Time", "PC-Usage","Activity", "All models"]

with st.form("my_for3"):
    model_selected = st.selectbox("Select the model for refit", options = options)
    submitted = st.form_submit_button("Submit")



if submitted:
    placeholder = st.info("Loading")
    if model_selected == "Login-Time":
      url = "http://116.202.137.233:8000/time-refit"
    elif model_selected == "PC-Usage":
      url = "http://116.202.137.233:8000/pc-refit"
    elif model_selected == "Activity":
      url = "http://116.202.137.233:8000/activity-refit"
    elif model_selected == "All models":
      url = "http://116.202.137.233:8000/all-refit"
    #data = request.fetchdata(url)

    placeholder.empty()
    st.success("Successfully refitted model: " + model_selected)




