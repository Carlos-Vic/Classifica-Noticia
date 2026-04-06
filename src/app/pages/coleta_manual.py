import streamlit as st
from datetime import date
from database import db
import traceback
from app.utils import portais, encontra_scraper



with st.form('coleta_artigos'):
    st.write('Portais Cadastrados:')
    st.caption(f':red[{', '.join(portais)}]')
    
    url = st.text_input(
        key='input_url',
        label='Cole o link da matéria',
    )
    
    label = st.radio(
        key='label_radio',
        label='Escolha o viés da matéria:',
        options=['Direita', 'Esquerda'],
    )
    
    
    enviar = st.form_submit_button(label='Enviar')

@st.dialog('Confirmar matéria')
def confirmar_materia():
    st.write('**Link:** ', st.session_state['input_url'])
    st.write('**Título:** ', st.session_state['artigo']['titulo'])
    if st.session_state['artigo']['subtitulo']:
        st.write('**Subtítulo:** ', st.session_state['artigo']['subtitulo'])
    st.write('**Viés escolhido:** ', st.session_state['label_radio'])
    
    with st.expander('Clique para ler o texto do artigo:'):
        st.write(st.session_state['artigo']['texto'])
    
    confirmar = st.button(label='Confirmar')
    cancelar = st.button(label='Cancelar')
    
    if confirmar:
        db.salva_artigo(st.session_state['artigo'])
        st.session_state['input_url'] = ''
        st.session_state['salvo'] = True
        st.rerun()
    
    if cancelar:
        st.rerun()

@st.dialog('Editar Viés')
def editar_materia():
    if st.session_state['duplicata'][2] == 'Direita':
        novo_vies = 'Esquerda'
    else:
        novo_vies = 'Direita'
    
    st.warning(f'Essa matéria já foi salva com o viés **{st.session_state['duplicata'][2]}**, deseja mudar o viés para **{novo_vies}**?')
    st.caption('Informações da Matéria')
    st.write(f'**Link**: {st.session_state['input_url']}')
    st.write(f'**Portal**:  {st.session_state['duplicata'][3]}')
    st.write(f'**Título**: {st.session_state['duplicata'][1]}')
    
    with st.expander('Clique para ler o texto do artigo:'):
        st.write(st.session_state['duplicata'][4])
    
    confirmar = st.button(label='Confirmar')
    cancelar = st.button(label='Cancelar')
    
    if confirmar:
        db.troca_vies(novo_vies, st.session_state['duplicata'][0])
        st.session_state['alterado'] = True
        st.rerun()
    
    if cancelar:
        st.rerun()

if enviar:
    scraper, dominio_esperado = encontra_scraper(url)
    hoje = date.today() 
    
    if scraper:
        try:
            portal = scraper.parser(url)
        except Exception:
            st.error('Erro ao coletar o link, salvo no registro de erros para possível correção futura')
            db.registra_erro(url,label, traceback.format_exc(), hoje)
        else:
            duplicata = db.verifica_duplicata(portal)
            st.session_state['duplicata'] = duplicata
            
            if not duplicata:       
                st.session_state['artigo'] = portal
                st.session_state['artigo']['label'] = label
                st.session_state['artigo']['dataColeta'] = hoje
                confirmar_materia()     
            else:
                editar_materia()
    else:
        st.error(f'Portal não cadastrado: {dominio_esperado}')
        dados = (dominio_esperado, url, label)
        db.registra_portal_sem_scraper(dados)

if st.session_state.get('salvo'):
    st.success(f'Matéria "{st.session_state['artigo']['titulo']}" salva com sucesso')
    st.session_state['salvo'] = None

if st.session_state.get('alterado'):
    st.success(f'Viés da Matéria: "{st.session_state['duplicata'][1]}" alterado com sucesso')
    st.session_state['alterado'] = None