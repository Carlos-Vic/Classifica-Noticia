import traceback
from datetime import date
from database import db
from urllib.parse import urlparse
from scraper.portals import scraper_cb_poder, scraper_brasil_de_fato, scraper_cnn, scraper_correio_braziliense, scraper_g1, scraper_jornal_de_brasilia, scraper_metropoles, scraper_vero_noticias, scraper_brasil_247, scraper_bsb_capital

portais = {
    'cb poder': (scraper_cb_poder, 'blogs.correiobraziliense.com.br'),
    'g1': (scraper_g1, 'g1.globo.com'),
    'cnn': (scraper_cnn, 'cnnbrasil.com.br'),
    'brasil de fato': (scraper_brasil_de_fato, 'brasildefato.com.br'),
    'jornal de brasilia': (scraper_jornal_de_brasilia, 'jornaldebrasilia.com.br'),
    'correio braziliense': (scraper_correio_braziliense,'correiobraziliense.com.br'),
    'metropoles': (scraper_metropoles, 'metropoles.com'),
    'vero noticias': (scraper_vero_noticias,'veronoticias.com'),
    'brasil 247': (scraper_brasil_247, 'brasil247.com'),
    'bsb capital': (scraper_bsb_capital, 'bsbcapital.com.br')
}

def encontra_scraper(url):
    url_parseada = urlparse(url)
    dominio_esperado = url_parseada.netloc

    for _, (scraper, dominio) in portais.items():
        if dominio in dominio_esperado:
            return scraper, dominio_esperado

    return None, dominio_esperado

def processa_urls(urls, label):
    portais_nao_cadastrados = []
    salvos_no_banco = []
    duplicatas = []
    erros = []
    hoje = date.today()
      
 
    for url in urls:
        scraper, dominio_esperado = encontra_scraper(url)
            
        if scraper:
            try:
                portal = scraper.parser(url)
            except Exception:
                dados = (url, label, traceback.format_exc(), hoje)
                erros.append(dados)
                db.registra_erro(*dados)
                continue
            
            duplicata = db.verifica_duplicata(portal)
                
            if duplicata:
                dados = (duplicata[1], duplicata[2], duplicata[3], url)
                duplicatas.append(dados)
            else:
                portal['dataColeta'] = hoje
                portal['label'] = label
                db.salva_artigo(portal)
                dados = (portal['titulo'], portal['label'], portal['portal'], url)
                salvos_no_banco.append(dados)
        else:
            dados = (dominio_esperado, url, label)
            portais_nao_cadastrados.append(dados)
            db.registra_portal_sem_scraper(dados)
        
        
    return salvos_no_banco, duplicatas, portais_nao_cadastrados, erros