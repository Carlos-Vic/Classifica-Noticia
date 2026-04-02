from scraper.base_scraper import coleta_materia
from datetime import datetime

def parser(url):
    materia = coleta_materia(url)
    titulo = materia.find('h1', attrs={'class': 'post-title'})
    subtitulo = verifica_subtitulo(materia)
    texto = separa_texto(materia)
    data = trata_data(materia)
    
    return {
        'portal': 'jornal de brasilia',
        'titulo' : titulo.text,
        'subtitulo' : subtitulo,
        'texto' : texto,
        'dataPublicacao' : data,
        'url': url
    }

def verifica_subtitulo(materia):
    div = materia.find('div', attrs={'class': 'wrap-title'})
    subtitulo = div.find('p')
       
    if subtitulo:
        return subtitulo.text
    else:
        return None

def separa_texto(materia):
    div = materia.find('div', class_='the-post-content')
    paragrafos = div.find_all('p')
    
    texto = []
    for p in paragrafos:
            temp = p.text
            if not temp.isupper():
                texto.append(temp)
                 
    return "".join(texto)
    
def trata_data(materia):
    data = materia.find('p', attrs={'class': 'date'})
    data_str = data.text[:10]
    data_obj = datetime.strptime(data_str, '%d/%m/%Y').date()
    return data_obj