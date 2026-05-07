from scraper.base_scraper import coleta_materia
from datetime import datetime

def parser(url):
    materia = coleta_materia(url)
    titulo = materia.find('h1', attrs={'class': 'elementor-heading-title elementor-size-default'})
    subtitulo = verifica_subtitulo(materia)
    texto  = separa_texto(materia)
    data = trata_data(materia)
    
    
    return {
        'portal' : 'bsb capital',
        'titulo' : titulo.text,
        'subtitulo' : subtitulo,
        'texto' : texto,
        'dataPublicacao' : data,
        'url': url,
    }

def verifica_subtitulo(materia):
    div = materia.find('div', attrs={'class': 'elementor-element elementor-element-d5a9207 elementor-widget elementor-widget-heading'})
    
    if div:
        return div.text
    else:
        return None
    
def separa_texto(materia):
    div_artigo = materia.find('div', attrs={'class': 'elementor-element elementor-element-c31d7ad elementor-widget elementor-widget-theme-post-content'})
    paragrafos = div_artigo.find_all('p')
    
    texto = []
    for p in paragrafos:
        texto_limpo = p.text.strip()
        if texto_limpo:
            texto.append(texto_limpo)
    
    return ''.join(texto).replace('\xa0', '').replace('\n', ' ')

def trata_data(materia):
    time = materia.find('time')
    data_str = time.text
    data_obj = datetime.strptime(data_str, '%d/%m/%Y').date()
    
    return data_obj

teste = input()
print(parser(teste))