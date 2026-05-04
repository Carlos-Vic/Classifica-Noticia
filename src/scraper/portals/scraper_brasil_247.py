from scraper.base_scraper import coleta_materia
from datetime import datetime

def parser(url):
    materia = coleta_materia(url)
    titulo = materia.find('h1', attrs={'class': 'article__headline'})
    subtitulo = verifica_subtitulo(materia)
    texto = separa_texto(materia)
    data = trata_data(materia)
    
    return {
        'portal' : 'brasil 247',
        'titulo' : titulo.text,
        'subtitulo' : subtitulo,
        'texto' : texto,
        'dataPublicacao' : data,
        'url': url,
    }

def verifica_subtitulo(materia):
    subtitulo = materia.find('h2', attrs={'class':'article__lead'})
    
    if subtitulo:
        return subtitulo.text
    else:
        return None

def separa_texto(materia):
    div = materia.find('div', attrs={'data-cy': 'articleBody'})
    paragrafos = div.find_all('p')
    
    texto = []
    for p in paragrafos:
        temp = p.text
        texto.append(temp)

    return ''.join(texto).replace('\xa0', '')

def trata_data(materia):
    meses = {
        'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
        'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
        'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
    }
    
    time = materia.find('time', attrs={'class': 'article__time'})
    data_str = time.text.split(',')[0].replace(' de ', '/')
    
    for mes, numero in meses.items():
        data_str = data_str.replace(mes, numero)
    
    data_obj = datetime.strptime(data_str, '%d/%m/%Y').date()
    return data_obj