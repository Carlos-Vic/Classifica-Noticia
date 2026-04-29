import streamlit as st
import pandas as pd
from app.utils import encontra_scraper, portais, processa_urls
from database import db

erros = db.mostra_erros()

if erros:
    st.title('Erros')
    df_erros = pd.DataFrame(erros, columns=['URL', 'Viés', 'Erro', 'dataColeta'])
    df_erros['dataColeta'] = pd.to_datetime(df_erros['dataColeta'])
    st.metric(label='Total de Erros registrados', value=len(df_erros))
    st.dataframe(df_erros, hide_index=True, column_config={'Erro': None,
                                                           'dataColeta': st.column_config.DateColumn(format='DD/MM/YYYY')})
    botao = st.button(label='Reprocessar Erros')
    
    with st.expander('Ver tracebacks'):
        for linha in df_erros.itertuples():                                                                                                                        
            st.markdown(f'**{linha.URL}**') 
            st.code(linha.Erro)                                                                                                                                    
            st.divider()

    if botao:
        urls_direita = df_erros[df_erros['Viés'] == 'Direita']['URL'].tolist()
        urls_esquerda = df_erros[df_erros['Viés'] == 'Esquerda']['URL'].tolist()
        
        s1, d1, p1, e1 = processa_urls(urls_direita, 'Direita')
        s2, d2, p2, e2 = processa_urls(urls_esquerda, 'Esquerda')
        
        salvos_no_banco = s1 + s2
        duplicatas = d1 + d2
        portais_nao_cadastrados = p1 + p2
        erros = e1 + e2
        
        for _, _, _, url in salvos_no_banco:
            db.deleta_erro(url)
        
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