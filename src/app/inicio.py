import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st

st.title('Interface de Coleta de Artigos')
st.caption('Plataforma de coleta, rotulagem e visualização de notícias políticas brasileiras.')

st.divider()

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader('📰 Coleta Manual')
        st.write('Cole a URL de um artigo, selecione o viés e salve no banco. O portal é detectado automaticamente.')
        st.markdown('''
**Como usar:**
1. Cole a URL do artigo
2. Confirme os dados coletados
3. Selecione o viés (Esquerda/Direita)
4. Salve no banco
''')

with col2:
    with st.container(border=True):
        st.subheader('📦 Coleta em Lote')
        st.write('Cole um bloco de URLs separadas por label e envie tudo de uma vez. Ideal para rotular grandes volumes rapidamente.')
        st.markdown('''
**Como usar:**
1. Cole o bloco de URLs no formato esperado
2. Clique em Enviar
3. Acompanhe o relatório de salvos e duplicatas
''')

with col3:
    with st.container(border=True):
        st.subheader('📋 Artigos')
        st.write('Visualize todos os artigos salvos no banco com filtros por portal e viés.')
        st.markdown('''
**Como usar:**
1. Selecione os filtros de portal e viés
2. Navegue pelas páginas
3. Visualize os artigos coletados
''')

with col4:
    with st.container(border=True):
        st.subheader('📊 Dashboard')
        st.write('Acompanhe o progresso da coleta com gráficos de distribuição de viés, portais sem scraper e registro de erros de coleta.')
        st.markdown('''
**Como usar:**
1. Acesse a página
2. Os gráficos são gerados automaticamente
3. Monitore o equilíbrio entre esquerda e direita
4. Verifique os links que falharam no registro de erros
''')
