from database import db
from datetime import date
from scraper.portals import scraper_cnn, scraper_g1, scraper_jornal_de_brasilia, scraper_brasil_de_fato, scraper_correio_braziliense, scraper_metropoles, scraper_vero_noticias


hoje = date.today()
data_formatada = hoje.strftime('%d/%m/%Y')

dic = {'g1': scraper_g1, 'cnn': scraper_cnn, 'jbr': scraper_jornal_de_brasilia,
       'bdf' : scraper_brasil_de_fato, 'cbr': scraper_correio_braziliense, 'mtr': scraper_metropoles,
       'vn': scraper_vero_noticias}

def menu(entrada, url):
    materia = dic[entrada].parser(url)
    label = input('Digite o label d ou e: ')
    materia.update({'label':label, 'dataColeta':data_formatada})
    duplicata = db.verifica_duplicata(materia)
    
    if duplicata:
        print('Essa matéria já foi registrada anteriormente', duplicata[0])
    else: 
        db.salva_artigo(materia)
        print('Matéria salva com sucesso')
    
    
entrada = input('Digite o portal g1, cnn, jbr, bdf, cbr, mtr, vn: ')
url = input('Cole a url: ')

menu(entrada, url)