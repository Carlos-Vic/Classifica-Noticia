import json
from datetime import datetime
from bs4 import BeautifulSoup
from scraper.base_scraper import coleta_materia


def parser(url):
    materia = coleta_materia(url)
    script = materia.find('script', id='__NEXT_DATA__')
    data = json.loads(script.string)
    noticia = data['props']['pageProps']['dadosDaNoticia']

    titulo = noticia['title']
    subtitulo = noticia.get('excerpt') or None
    texto = separa_texto(noticia['content'])
    data_pub = datetime.fromisoformat(noticia['date']).date()

    return {
        'portal': 'metropoles',
        'titulo': titulo,
        'subtitulo': BeautifulSoup(subtitulo, 'html.parser').get_text().strip() if subtitulo else None,
        'texto': texto,
        'dataPublicacao': data_pub,
        'url': url,
    }


def separa_texto(content_html):
    soup = BeautifulSoup(content_html, 'html.parser')
    paragrafos = soup.find_all('p')
    texto = [p.get_text().strip() for p in paragrafos if p.get_text().strip()]
    return ''.join(texto).replace('\xa0', '')
