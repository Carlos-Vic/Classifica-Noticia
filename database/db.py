import sqlite3

conn = sqlite3.connect('database/database.db')
cursor = conn.cursor()


def salva_artigo(dicionario):
    with open('database/queries/insert_artigo.sql', 'r') as file:
        sql_script = file.read()
    
    dados = (dicionario['portal'], dicionario['titulo'], dicionario['subtitulo'], 
             dicionario['texto'], dicionario['dataPublicacao'], dicionario['label'],
             dicionario['url'], dicionario['dataColeta'])
     
    cursor.execute(sql_script, dados)
    conn.commit()
    conn.close()