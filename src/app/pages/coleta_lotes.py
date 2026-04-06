import streamlit as st
from database import db
from datetime import date
import traceback
from app.utils import encontra_scraper, portais

with st.form('coleta_em_lotes', clear_on_submit=True):
    st.write('Portais Cadastrados:')
    st.caption(f':red[{', '.join(portais)}]')
    texto = st.text_area('Cole o texto aqui', 
                         placeholder='Precisa seguir exatamente o formato abaixo: \n\n*DIREITA*\n\nLink1\n\nLink2\n\n...\n\n*ESQUERDA*\n\nLink1\n\nLink2\n\n...',
                         height=400)
    enviar = st.form_submit_button(label='Enviar')

def processa_urls(urls, label):
    portais_nao_cadastrados = []
    salvos_no_banco = []
    duplicatas = []
    erros = []
    hoje = date.today()
      
 
    for url in urls:
        scraper, dominio_esperado = encontra_scraper(url)
            
        if scraper:
            try:
                portal = scraper.parser(url)
            except Exception:
                dados = (url, label, traceback.format_exc(), hoje)
                erros.append(dados)
                db.registra_erro(*dados)
                continue
            
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
        
        
    return salvos_no_banco, duplicatas, portais_nao_cadastrados, erros



if enviar:
    if '*ESQUERDA*' not in texto or '*DIREITA*' not in texto:
        st.error('Formato de texto inválido, coloque os * na label')
    else:
        separador = texto.split('*ESQUERDA*')
        bloco_direita = separador[0]
        bloco_esquerda = separador[1]

        urls_direita = [linha for linha in bloco_direita.split('\n') if linha.startswith('http')]  
        urls_esquerda = [linha for linha in bloco_esquerda.split('\n') if linha.startswith('http')]
        
        
        s1, d1, p1, e1 = processa_urls(urls_direita, 'Direita')
        s2, d2, p2, e2 = processa_urls(urls_esquerda, 'Esquerda')
        
        salvos_no_banco = s1 + s2
        duplicatas = d1 + d2
        portais_nao_cadastrados = p1 + p2
        erros = e1 + e2
        
    
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
        
        st.error(f'{len(erros)} links que deram erro')
        with st.expander('Ver detalhes'):
            st.write('Salvo no banco de erros para possível correção no futuro')
            for url, label, _, _ in erros:
                st.write(f'Link {url}')
                st.write(f'Viés: {label}')
                st.divider()