import sqlite3

def salva_artigo(dicionario):
    with sqlite3.connect('data/classifica.db') as conn:
        cursor = conn.cursor()
        
        with open('src/database/queries/insert_artigo.sql', 'r') as file:
            sql_script = file.read()
        
        dados = (dicionario['portal'], dicionario['titulo'], dicionario['subtitulo'], 
                dicionario['texto'], dicionario['dataPublicacao'], dicionario['label'],
                dicionario['url'], dicionario['dataColeta'])
        
        cursor.execute(sql_script, dados)

def verifica_duplicata(dicionario):
    with sqlite3.connect('data/classifica.db') as conn:
        cursor = conn.cursor()
    
        with open('src/database/queries/select_url.sql', 'r') as file:
            sql_script = file.read()
        
        dado = (dicionario['url'],)
        
        cursor.execute(sql_script, dado)
        resultado = cursor.fetchone()
               
        if resultado:
            return resultado
        else:
            return None