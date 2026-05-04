import streamlit as st
import pandas as pd
from app.utils import encontra_scraper, portais, processa_urls
from database import db

links_esq = db.busca_portais_demanda('Esquerda')
links_dir = db.busca_portais_demanda('Direita')

if links_esq or links_dir:
    st.title('Links de portais não cadastrados')
    df_esq = pd.DataFrame(links_esq, columns=['URL', 'Viés'])
    df_dir = pd.DataFrame(links_dir, columns=['URL', 'Viés'])
    df = pd.concat([df_esq, df_dir], ignore_index=True)
    st.dataframe(df, hide_index=True)
    botao = st.button(label='Reprocessar Links')
    
    if botao:
        urls_direita = df[df['Viés'] == 'Direita']['URL'].tolist()
        urls_esquerda = df[df['Viés'] == 'Esquerda']['URL'].tolist()
        
        s1, d1, p1, e1 = processa_urls(urls_direita, 'Direita')
        s2, d2, p2, e2 = processa_urls(urls_esquerda, 'Esquerda')
            
        salvos_no_banco = s1 + s2
        duplicatas = d1 + d2
        portais_nao_cadastrados = p1 + p2
        erros = e1 + e2
            
        for _, _, _, url in salvos_no_banco:
            db.deleta_link_demanda(url)
            
        for _, _, _, url in duplicatas:
            db.deleta_link_demanda(url)
            
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