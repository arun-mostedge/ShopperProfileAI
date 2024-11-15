import streamlit as st 
import pickle 
import yaml 
import pandas as pd

st.set_page_config(
    page_title="Mostedge Face Recognition Solution",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.mostedge.com/',
        'About': "# This is a *SaaS* based store monitoring solution app, developed by:orange[***Mostedge***]!",
    }
)
st.image('logo.png')

cfg = yaml.load(open("config.yaml", "r"), Loader=yaml.FullLoader)
PKL_PATH = cfg['PATH']["PKL_PATH"]

#Load databse 
with open(PKL_PATH, 'rb') as file:
    database = pickle.load(file)

Index, Id, Name, Image  = st.columns([0.5,0.5,3,3])

for idx, person in database.items():
    with Index:
        st.write(idx)
    with Id: 
        st.write(person['id'])
    with Name:     
        st.write(person['name'])
    with Image:     
        st.image(person['image'],width=200)

