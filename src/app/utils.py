from urllib.parse import urlparse
from scraper.portals import scraper_cb_poder, scraper_brasil_de_fato, scraper_cnn, scraper_correio_braziliense, scraper_g1, scraper_jornal_de_brasilia, scraper_metropoles, scraper_vero_noticias

portais = {
    'cb poder': (scraper_cb_poder, 'blogs.correiobraziliense.com.br'),
    'g1': (scraper_g1, 'g1.globo.com'),
    'cnn': (scraper_cnn, 'cnnbrasil.com.br'),
    'brasil de fato': (scraper_brasil_de_fato, 'brasildefato.com.br'),
    'jornal de brasila': (scraper_jornal_de_brasilia, 'jornaldebrasilia.com.br'),
    'correio braziliense': (scraper_correio_braziliense,'correiobraziliense.com.br'),
    'metropoles': (scraper_metropoles, 'metropoles.com'),
    'vero noticias': (scraper_vero_noticias,'veronoticias.com'),
}

def encontra_scraper(url):
    url_parseada = urlparse(url)
    dominio_esperado = url_parseada.netloc

    for _, (scraper, dominio) in portais.items():
        if dominio in dominio_esperado:
            return scraper, dominio_esperado

    return None, dominio_esperado