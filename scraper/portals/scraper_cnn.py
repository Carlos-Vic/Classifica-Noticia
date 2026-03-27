from scraper.base_scraper import coleta_materia
from datetime import datetime

def parser(url):
    materia = coleta_materia(url)
    titulo = materia.find('h1', attrs={'class': 'font-bold text-3xl lg:text-4xl'})
    subtitulo = verifica_subtitulo(materia)
    texto = separa_texto(materia)
    data = trata_data(materia)
    
    return {
        'portal': 'cnn',
        'titulo' : titulo.text,
        'subtitulo' : subtitulo,
        'texto' : texto,
        'dataPublicacao' : data,
        'url': url
        
    }

def verifica_subtitulo(materia):
    subtitulo = materia.find('h2', attrs={'class': 'text-lg font-normal group-[.isActiveSource]:text-xl'})
    
    if subtitulo:
        return subtitulo.text
    else:
        return None

def separa_texto(materia):
    paragrafos = materia.find_all('p', attrs={'class': 'my-5 break-words group-[.isActiveSource]:text-xl'})
    
    texto = []
    for p in paragrafos:
        temp = p.text
        texto.append(temp)
        
    return "".join(texto)

def trata_data(materia):
    data = materia.find('span', attrs={'class': 'timestamp__date'})
    data_str = data.text[0:8]
    data_obj = datetime.strptime(data_str, '%d/%m/%y').date()
    return data_obj