import streamlit as st
from database import db
from app.utils import portais
import pandas as pd
from math import ceil
from typing import Optional


def reseta_pagina():
    st.session_state['pagina'] = 1

st.write('Filtros:')
portal: Optional[str] = st.selectbox(label='Portal',options=['Todos'] + list(portais.keys()), index=0, on_change=reseta_pagina)
vies: Optional[str] = st.selectbox(label='Viés', options=['Todos', 'Direita', 'Esquerda'], index=0, on_change=reseta_pagina)

if 'pagina' not in st.session_state:  
     st.session_state['pagina'] = 1 
    

offset = (st.session_state['pagina'] - 1) * 10 # calcula o offset dinamicamente pra mandar pra query no db.py 

if portal == 'Todos':
    portal = None

if vies == 'Todos':
    vies = None

artigos, total = db.mostra_artigos(offset, portal, vies)
total_paginas = ceil(total / 10) # arredonda a página

df = pd.DataFrame(artigos, columns=['id', 'portal', 'titulo', 'subtitulo', 'texto', 'dataPublicacao', 'label', 'url', 'dataColeta'])
st.dataframe(df, column_config={
    'id' : None
}, width='stretch', hide_index=True)

col1, col2 = st.columns(2)
with col1:
    if st.button('Anterior', disabled=st.session_state['pagina'] <= 1):
        st.session_state['pagina'] -= 1
        st.rerun()
with col2:
    if st.button('Próxima', disabled=st.session_state['pagina'] >= total_paginas):
        st.session_state['pagina'] += 1
        st.rerun()