import streamlit as st
from scraper.portals import scraper_brasil_de_fato, scraper_cnn, scraper_correio_braziliense, scraper_g1, scraper_jornal_de_brasilia, scraper_metropoles, scraper_vero_noticias

portais = {
    'G1': scraper_g1, 'Brasil de Fato': scraper_brasil_de_fato, 'CNN': scraper_cnn,
    'Jornal de Brasília': scraper_jornal_de_brasilia, 'Correio Braziliense': scraper_correio_braziliense,
    'Metrópoles': scraper_metropoles, 'Vero Notícias': scraper_vero_noticias
}

dominios = { 
      'G1': 'g1.globo.com', 'CNN': 'cnnbrasil.com.br', 'Jornal de Brasília': 'jornaldebrasilia.com.br',                                                                                                       
      'Metrópoles': 'metropoles.com', 'Correio Braziliense': 'correiobraziliense.com.br', 'Brasil de Fato': 'brasildefato.com.br',
      'Vero Notícias': 'veronoticias.com'
}

portal_selecionado = st.selectbox(
    'Selecione o portal',
     portais)

url = st.text_input(
    'Cole o link da matéria',
)
