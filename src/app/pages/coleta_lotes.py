import streamlit as st
from database import db
from datetime import date
from app.utils import encontra_scraper

with st.form('coleta_em_lotes', clear_on_submit=True):
    input = st.text_area('Cole o texto aqui')
    enviar = st.form_submit_button(label='Enviar')

def processa_urls(urls, label):
    portais_nao_cadastrados = []
    salvos_no_banco = []
    duplicatas = [] 
    hoje = date.today()
    
    for url in urls:
        scraper, dominio_esperado = encontra_scraper(url)
        
        if scraper:
            portal = scraper.parser(url)
            duplicata = db.verifica_duplicata(portal)
            
            if duplicata:
                dados = (duplicata[1], duplicata[2], duplicata[3], url)
                duplicatas.append(dados)
            else:
                portal['dataColeta'] = hoje
                portal['label'] = label
                db.salva_artigo(portal)
                dados = (portal['titulo'], portal['label'], portal['portal'], url)
                salvos_no_banco.append(dados)
        else:
            dados = (dominio_esperado, url, label)
            portais_nao_cadastrados.append(dados)
            db.registra_portal_sem_scraper(dados)
        
    return salvos_no_banco, duplicatas, portais_nao_cadastrados



if enviar:
    separador = input.split('*ESQUERDA*')
    bloco_direita = separador[0]
    bloco_esquerda = separador[1]

    urls_direita = [linha for linha in bloco_direita.split('\n') if linha.startswith('http')]  
    urls_esquerda = [linha for linha in bloco_esquerda.split('\n') if linha.startswith('http')]
    
    
    
    s1, d1, p1 = processa_urls(urls_direita, 'Direita')
    s2, d2, p2 = processa_urls(urls_esquerda, 'Esquerda')
    
    salvos_no_banco = s1 + s2
    duplicatas = d1 + d2
    portais_nao_cadastrados = p1 + p2
    
    
    st.success(f'{len(salvos_no_banco)} matérias salvas')
    with st.expander('Ver detalhes'):
        for titulo, label, portal, url in salvos_no_banco:
            st.write(f'**{titulo}**')                                                                                                                                  
            st.write(f'Viés: {label} | Portal: {portal}')
            st.write(f'Link: {url}')
            st.divider()
    
    st.warning(f'{len(duplicatas)} duplicatas ignoradas')
    with st.expander('Ver detalhes'):
        for titulo, label, portal, url in duplicatas:
            st.write(f'**{titulo}**')                                                                                                                                  
            st.write(f'Viés: {label} | Portal: {portal}')
            st.write(f'Link: {url}')
            st.divider()
    
    st.error(f'{len(portais_nao_cadastrados)} portais não cadastrados')
    with st.expander('Ver detalhes'):
        for dominio_esperado, url, _ in portais_nao_cadastrados:
            st.write(f'Portal não Cadastrado: {dominio_esperado}')
            st.write(f'Link: {url}')
            st.divider()