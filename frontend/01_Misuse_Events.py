import streamlit as st
from helper import *
import pathlib
from PIL import Image
import requests
import pandas as pd
import numpy as np
import json



st.set_page_config(
    page_title= "Privilege Misuse Detection",
    page_icon = "👨‍🔬",
)
data = ""
str_arr_warn = [] 
str_arr_alert = [] 
to_out_warn = [] 
to_out_alert = [] 

# load css and page design
load_css.read_css()
#streamlit_static_path = pathlib.Path(st.__path__[0])/ 'static'
logo_path = "static/logo.jpg"
image = Image.open(logo_path)
st.sidebar.image(image, use_column_width = True,)
st. sidebar.info("Team: Gold Digger")
st.write(""" # Privilege Misuse Detection """)

to_out_warn = ''.join(str_arr_warn)
to_out_alert = ''.join(str_arr_alert)

st.markdown("<div>"+ "Current alerts: "+ "</div>", unsafe_allow_html= True)

data = sql.getactivity()
if not data.empty:
  data.drop('id', axis=1,inplace=True)
  st.dataframe(data)