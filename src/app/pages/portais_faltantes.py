import streamlit as st
from database import db

resultado = db.mostra_portal_sem_scraper()

st.table(resultado)