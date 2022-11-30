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
st.write(""" # PC Statistics""")
st.write("Statstics over last 30 days")
r = requests.get("http://localhost:8000/pc-role-factors")
stats = pd.DataFrame(json.loads(r.json()))
stats = stats.reset_index()
col1, col2 = st.columns(2)
col1.metric("Connections Included", sum(stats["date"]))
col2.metric("Active Users", sum(stats["employee_name"]))
stats["inverse"] = 1 / stats["factor"]
fig = px.pie(stats, values='inverse', names='index', title='Amount of unique PCs used per Role')
st.plotly_chart(fig, use_container_width=True)