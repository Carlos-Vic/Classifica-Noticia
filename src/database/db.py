import psycopg2
from psycopg2 import pool
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
db_pool = pool.SimpleConnectionPool(1, 10, DATABASE_URL)
BASE_DIR = Path(__file__).resolve().parents[2] # Pega a raiz do projeto
QUERIES_DIR = BASE_DIR / 'src' / 'database' / 'queries'

def salva_artigo(dicionario):
    conn = db_pool.getconn()
    try:
        with conn:
            cursor = conn.cursor()
            
            with open(QUERIES_DIR / 'insert_artigo.sql', 'r') as file:
                sql_script = file.read()
            
            dados = (dicionario['portal'], dicionario['titulo'], dicionario['subtitulo'], 
                    dicionario['texto'], dicionario['dataPublicacao'], dicionario['label'],
                    dicionario['url'], dicionario['dataColeta'])
            
            cursor.execute(sql_script, dados)
    finally:
        db_pool.putconn(conn)

def verifica_duplicata(dicionario):
    conn = db_pool.getconn()
    try:
        with conn:
            cursor = conn.cursor()

            with open(QUERIES_DIR / 'select_url.sql', 'r') as file:
                sql_script = file.read()
            
            dado = (dicionario['url'],)
            
            cursor.execute(sql_script, dado)
            resultado = cursor.fetchone()
                
            if resultado:
                return resultado
            else:
                return None
    finally:
        db_pool.putconn(conn)

def troca_vies(novo_vies, idMateria):
    conn = db_pool.getconn()
    try:
        with conn:
            cursor = conn.cursor()
            
            with open(QUERIES_DIR / 'update_label.sql', 'r') as file:
                sql_script = file.read()
            
            dados = (novo_vies, idMateria)
            cursor.execute(sql_script, dados)
    finally:
        db_pool.putconn(conn)

def registra_portal_sem_scraper(dados):
    conn = db_pool.getconn()
    try:
        with conn:
            cursor = conn.cursor()
            
            with open(QUERIES_DIR / 'insert_portais_faltantes.sql', 'r') as file:
                sql_script = file.read()
                
            cursor.execute(sql_script, dados)
    finally:
        db_pool.putconn(conn)

def mostra_portal_sem_scraper():
    conn = db_pool.getconn()
    try:
        with conn:
            cursor = conn.cursor()
            
            with open(QUERIES_DIR / 'select_portal_faltante.sql', 'r') as file:
                sql_script = file.read()
            
            cursor.execute(sql_script)
            
            return cursor.fetchall()
    finally:
        db_pool.putconn(conn)

def mostra_artigos(offset, portal=None, label=None):
    conn = db_pool.getconn()
    try:
        with conn:
            cursor = conn.cursor()

            filtros = []
            dados = []

            if portal:
                filtros.append('portal = %s')
                dados.append(portal)
            if label:
                filtros.append('label = %s')
                dados.append(label)

            where = ' WHERE ' + ' AND '.join(filtros) if filtros else ''

            sql_artigos = 'SELECT * FROM artigos' + where + ' LIMIT 10 OFFSET %s'
            sql_count = 'SELECT COUNT(*) FROM artigos' + where # Count separado, pois assim da pra saber quantas páginas existe no total

            cursor.execute(sql_count, tuple(dados))
            total = cursor.fetchone()[0]

            cursor.execute(sql_artigos, tuple(dados + [offset]))
            artigos = cursor.fetchall()

            return artigos, total
    finally:
        db_pool.putconn(conn)

def mostra_total_vies():
    conn = db_pool.getconn()
    try:
        with conn:
            cursor = conn.cursor()
        
            with open(QUERIES_DIR / 'select_vies_total.sql', 'r') as file:
                sql_script = file.read()
            
            cursor.execute(sql_script)
            
            return cursor.fetchall()
    finally:
        db_pool.putconn(conn)

def mostra_vies_por_portal():
    conn = db_pool.getconn()
    try:
        with conn:
            cursor = conn.cursor()
        
            with open(QUERIES_DIR / 'select_vies_portal.sql', 'r') as file:
                sql_script = file.read()
            
            cursor.execute(sql_script)
            
            return cursor.fetchall()
    finally:
        db_pool.putconn(conn)

def registra_erro(url, label, erro, dataColeta):
    conn = db_pool.getconn()
    try:
        with conn:
            cursor = conn.cursor()
        
            with open(QUERIES_DIR / 'insert_erro.sql', 'r') as file:
                sql_script = file.read()
            
            dados = (url, label, erro, dataColeta)
            
            cursor.execute(sql_script, dados)
    finally:
        db_pool.putconn(conn)

def mostra_erros():
    conn = db_pool.getconn()
    try:
        with conn:
            cursor = conn.cursor()
        
            with open(QUERIES_DIR / 'select_erros.sql', 'r') as file:
                sql_script = file.read()
            
            cursor.execute(sql_script)
            
            return cursor.fetchall()
    finally:
        db_pool.putconn(conn)

def deleta_erro(url):
    conn = db_pool.getconn()
    try:
        with conn:
            cursor = conn.cursor()
        
            with open(QUERIES_DIR / 'delete_erro.sql', 'r') as file:
                sql_script = file.read()
            
            dados = (url,)
            
            cursor.execute(sql_script, dados)
    finally:
        db_pool.putconn(conn)

def busca_portais_demanda(label):
    conn = db_pool.getconn()
    try:
        with conn:
            cursor = conn.cursor()
        
            with open(QUERIES_DIR / 'select_label_portal_faltante.sql', 'r') as file:
                sql_script = file.read()
            
            dados = (label,)
            
            cursor.execute(sql_script, dados)
            return cursor.fetchall()
    finally:
        db_pool.putconn(conn)

def deleta_link_demanda(url):
    conn = db_pool.getconn()
    try:
        with conn:
            cursor = conn.cursor()
        
            with open(QUERIES_DIR / 'delete_link_demanda.sql', 'r') as file:
                sql_script = file.read()
            
            dados = (url,)
            
            cursor.execute(sql_script, dados)
    finally:
        db_pool.putconn(conn)