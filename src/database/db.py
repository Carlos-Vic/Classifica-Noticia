import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / os.getenv('DB_PATH', 'data/classifica.db')
QUERIES_DIR = BASE_DIR / 'src' / 'database' / 'queries'

def salva_artigo(dicionario):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        with open(QUERIES_DIR / 'insert_artigo.sql', 'r') as file:
            sql_script = file.read()
        
        dados = (dicionario['portal'], dicionario['titulo'], dicionario['subtitulo'], 
                dicionario['texto'], dicionario['dataPublicacao'], dicionario['label'],
                dicionario['url'], dicionario['dataColeta'])
        
        cursor.execute(sql_script, dados)

def verifica_duplicata(dicionario):
    with sqlite3.connect(DB_PATH) as conn:
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

def troca_vies(novo_vies, idMateria):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        with open(QUERIES_DIR / 'update_label.sql', 'r') as file:
            sql_script = file.read()
        
        dados = (novo_vies, idMateria)
        cursor.execute(sql_script, dados)

def registra_portal_sem_scraper(dados):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        with open(QUERIES_DIR / 'insert_portais_faltantes.sql', 'r') as file:
            sql_script = file.read()
            
        cursor.execute(sql_script, dados)

def mostra_portal_sem_scraper():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        with open(QUERIES_DIR / 'select_portal_faltante.sql', 'r') as file:
            sql_script = file.read()
        
        cursor.execute(sql_script)
        
        return cursor.fetchall()