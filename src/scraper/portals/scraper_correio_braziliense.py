from scraper.base_scraper import coleta_materia
from datetime import datetime

def parser(url):
    materia = coleta_materia(url)
    div_titulo = materia.find('div', attrs={'class': 'materia-title'})
    titulo = separa_titulo(div_titulo)
    subtitulo = verifica_subtitulo(div_titulo)
    texto  = separa_texto(materia)
    data = trata_data(materia)
    
    
    return {
        'portal' : 'correio braziliense',
        'titulo' : titulo,
        'subtitulo' : subtitulo,
        'texto' : texto,
        'dataPublicacao' : data,
        'url': url,
    }


def separa_titulo(div_titulo):
    titulo = div_titulo.find('h1')
    
    return titulo.text

def verifica_subtitulo(div_titulo):
    subtitulo = div_titulo.find('h2')
    
    if subtitulo:
        return subtitulo.text
    else:
        return None
    
def separa_texto(materia):
    div_artigo = materia.find('div', attrs={'class': 'cb-content-materia'})
    div_ler_mais = div_artigo.find('div', attrs={'class': 'read-more'})
    if div_ler_mais:
        div_ler_mais.decompose()
    paragrafos = div_artigo.find_all('p', attrs={'class': 'texto'})
     
    texto = []
    for p in paragrafos:
        texto.append(p.text)
    
    return ''.join(texto)

def trata_data(materia):
    div = materia.find('div', attrs={'class': 'date'})
    data_str = div.text[12:22]
    data_obj = datetime.strptime(data_str, '%d/%m/%Y').date()
    
    return data_obj