import streamlit as st
from database import db

resultado = db.mostra_portal_sem_scraper()

if resultado:
    st.table(resultado)
else:
    st.write('Nenhum portal sem registro salvo no banco')