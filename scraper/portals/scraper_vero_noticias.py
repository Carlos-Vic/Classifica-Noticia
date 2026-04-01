from scraper.base_scraper import coleta_materia
from datetime import datetime

def parser(url):
    materia = coleta_materia(url)
    titulo = materia.find('h2', attrs={'class':'post-title'})
    texto = separa_texto(materia)
    data = trata_data(materia)
    
    return {
        'portal' : 'vero noticias',
        'titulo' : titulo.text,
        'subtitulo' : None,
        'texto' : texto,
        'dataPublicacao' : data,
        'url': url,
    }
    
def separa_texto(materia):
    div = materia.find('div', attrs={'class': 'post-content'})
    paragrafos = div.find_all('p')
    
    texto = []
    for p in paragrafos:
        temp = p.text
        texto.append(temp)
    
    return ''.join(texto)

def trata_data(materia):
    span = materia.find('span', attrs={'class': 'post-date'})
    data_str = span.text.strip()[0:10]
    data_obj = datetime.strptime(data_str, '%d/%m/%Y').date()
    
    return data_obj
    
    

url = input()
teste = parser(url)
print(teste)

