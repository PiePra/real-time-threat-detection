from helper import *
import streamlit as st
import pathlib
from PIL import Image
import requests
import json
import plotly.express as px

data = ""
# load css and page design
load_css.read_css()
# streamlit_static_path = pathlib.Path(st.__path__[0])/ 'static'
# print(streamlit_static_path)
logo_path = "static/logo.jpg"
image = Image.open(logo_path)
st.sidebar.image(image, use_column_width = True,)
st. sidebar.info("Team: Gold Digger")
st.write(""" # Activity Statistics""")

r = requests.get("http://localhost:8000/activity-ratios")
stats = pd.DataFrame(json.loads(r.json()))
stats = stats.reset_index()
fig = px.pie(stats, values='conn_count', names='index', title='Distribution of USB Device Connections')
st.metric("Connected USB Devices", sum(stats['conn_count']))
st.plotly_chart(fig, use_container_width=True)