from scraper.base_scraper import coleta_materia
from datetime import datetime

def parser(url):
    materia = coleta_materia(url)
    titulo = materia.find('h1', attrs={'class': 'title-post'})
    texto  = separa_texto(materia)
    data = trata_data(materia)
    
    
    return {
        'portal' : 'cb poder',
        'titulo' : titulo.text,
        'subtitulo' : None,
        'texto' : texto,
        'dataPublicacao' : data,
        'url': url,
    }
    
def separa_texto(materia):
    div_artigo = materia.find('div', attrs={'class': 'entry-content mgt-xlarge'})
    paragrafos = div_artigo.find_all('p')
    
    texto = []
    for p in paragrafos:
        temp = p.text
        texto.append(temp)
    
    return ''.join(texto).replace('\xa0', '')

def trata_data(materia):
    data = materia.find('time', attrs={'class': 'entry-date published updated'})
    data_str = data.text[:10]
    data_obj = datetime.strptime(data_str, '%d/%m/%Y').date()
    
    return data_obj