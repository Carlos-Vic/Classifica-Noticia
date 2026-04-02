from scraper.base_scraper import coleta_materia
from datetime import datetime

def parser(url):
    materia = coleta_materia(url)
    titulo = materia.find('h1', attrs={'class':'content-head__title'})
    subtitulo = verifica_subtitulo(materia)
    texto = separa_texto(materia)
    data = trata_data(materia)
    
    return {
        'portal' : 'g1',
        'titulo' : titulo.text,
        'subtitulo' : subtitulo,
        'texto' : texto,
        'dataPublicacao' : data,
        'url': url,
    }

def separa_texto(materia):
    paragrafos = materia.find_all('p', attrs={'class':'content-text__container'})
    
    texto = []
    for p in paragrafos:
        temp = p.text
        texto.append(temp)
        
    return "".join(texto)

def trata_data(materia):
    data = materia.find('time', attrs={'itemprop': 'datePublished'})
    data_str = data.text[1:11]
    data_obj = datetime.strptime(data_str, '%d/%m/%Y').date()
    return data_obj

def verifica_subtitulo(materia):
    subtitulo = materia.find('h2',attrs={'class': 'content-head__subtitle'})
    
    if subtitulo:
        return subtitulo.text
    else:
        return None