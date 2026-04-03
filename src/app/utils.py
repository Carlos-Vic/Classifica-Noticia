from urllib.parse import urlparse
from scraper.portals import scraper_cb_poder, scraper_brasil_de_fato, scraper_cnn, scraper_correio_braziliense, scraper_g1, scraper_jornal_de_brasilia, scraper_metropoles, scraper_vero_noticias

portais = {
    'CB Poder': (scraper_cb_poder, 'blogs.correiobraziliense.com.br'),
    'G1': (scraper_g1, 'g1.globo.com'),
    'CNN': (scraper_cnn, 'cnnbrasil.com.br'),
    'Brasil de Fato': (scraper_brasil_de_fato, 'brasildefato.com.br'),
    'Jornal de Brasilia': (scraper_jornal_de_brasilia, 'jornaldebrasilia.com.br'),
    'Correio Braziliense': (scraper_correio_braziliense,'correiobraziliense.com.br'),
    'Metropoles': (scraper_metropoles, 'metropoles.com'),
    'Vero Noticias': (scraper_vero_noticias,'veronoticias.com'),
}

def encontra_scraper(url):
    url_parseada = urlparse(url)
    dominio_esperado = url_parseada.netloc

    for _, (scraper, dominio) in portais.items():
        if dominio in dominio_esperado:
            return scraper, dominio_esperado

    return None, dominio_esperado