import streamlit as st
from urllib.parse import urlparse
from datetime import date, datetime
from database import db
from scraper.portals import scraper_brasil_de_fato, scraper_cnn, scraper_correio_braziliense, scraper_g1, scraper_jornal_de_brasilia, scraper_metropoles, scraper_vero_noticias

scrapers = {
    'G1': scraper_g1, 'Brasil de Fato': scraper_brasil_de_fato, 'CNN': scraper_cnn,
    'Jornal de Brasília': scraper_jornal_de_brasilia, 'Correio Braziliense': scraper_correio_braziliense,
    'Metrópoles': scraper_metropoles, 'Vero Notícias': scraper_vero_noticias
}

dominios = { 
      'G1': 'g1.globo.com', 'CNN': 'cnnbrasil.com.br', 'Jornal de Brasília': 'jornaldebrasilia.com.br',                                                                                                       
      'Metrópoles': 'metropoles.com', 'Correio Braziliense': 'correiobraziliense.com.br', 'Brasil de Fato': 'brasildefato.com.br',
      'Vero Notícias': 'veronoticias.com'
}


with st.form('coleta_artigos'):
    st.write('Portais Cadastrados:')
    st.caption(f':red[{', '.join(dominios)}]')
    
    url = st.text_input(
        key='input_url',
        label='Cole o link da matéria',
    )
    
    label = st.radio(
        key='label_radio',
        label='Escolha o viés da matéria:',
        options=['Direita', 'Esquerda'],
        index=None 
    )
    
    
    enviar = st.form_submit_button(label='Enviar')

def encontra_scraper(url):   
    url_parseada = urlparse(url)
    dominio_esperado = url_parseada.netloc
    
    for portal, dominio in dominios.items():
       if dominio in dominio_esperado:
           scraper = scrapers[portal]
           return scraper, dominio_esperado          
    return None, dominio_esperado 
 


@st.dialog('Confirmar matéria')
def confirmar_materia():
    st.write('Título: ', st.session_state['artigo']['titulo'])
    if st.session_state['artigo']['subtitulo']:
        st.write('Subtítulo: ', st.session_state['artigo']['subtitulo'])
    st.write('Viés escolhido: ', st.session_state['label_radio'])
    
    confirmar = st.button(label='Confirmar')
    cancelar = st.button(label='Cancelar')
    
    if confirmar:
        db.salva_artigo(st.session_state['artigo'])
        st.session_state['input_url'] = ''
        st.session_state['label_radio'] = None
        st.session_state['salvo'] = True
        st.rerun()
    
    if cancelar:
        st.rerun()

if enviar:
    scraper, dominio_esperado = encontra_scraper(url)
    
    if scraper:
        portal = scraper.parser(url)
        duplicata = db.verifica_duplicata(portal)
        
        if not duplicata:
            hoje = date.today()        
            st.session_state['artigo'] = portal
            st.session_state['artigo']['label'] = label
            st.session_state['artigo']['dataColeta'] = hoje
            confirmar_materia()     
        else:
            st.error('Essa matéria já foi salva no banco de dados')
            st.write('Título:', duplicata[0])
    else:
        st.error(f'Portal não cadastrado: {dominio_esperado}')

if st.session_state.get('salvo'):
    st.success('Salvo no Banco de Dados com Sucesso')
    st.session_state['salvo'] = None