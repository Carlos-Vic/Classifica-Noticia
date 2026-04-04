from scraper.base_scraper import coleta_materia
from datetime import datetime

def parser(url):
    materia = coleta_materia(url)
    titulo = materia.find('h1', attrs={'class':'Text__TextBase-sc-1d75gww-0 TcJvw'})
    subtitulo = trata_subtitulo(materia)
    texto = separa_texto(materia)
    data = trata_data(materia)
    
    return {
        'portal' : 'metropoles',
        'titulo' : titulo.text,
        'subtitulo' : subtitulo,
        'texto' : texto,
        'dataPublicacao' : data,
        'url': url,
    }
    

def trata_subtitulo(materia):
    subtitulo = materia.find('h2', attrs={'class': 'Text__TextBase-sc-1d75gww-0 eOYeiH noticiaCabecalho__subtitulo'})
    
    if subtitulo:
        return subtitulo.text
    else:
        return None
    

def separa_texto(materia):
    div_artigo = materia.find('div', attrs={'class': 'ConteudoNoticiaWrapper-sc-19fsm27-0 hIDPRr m-content'})
    div_social_coluna = div_artigo.find('div', attrs={'class': 'm-social-coluna'})
    if div_social_coluna:
        div_social_coluna.decompose()
    paragrafos = div_artigo.find_all('p')
    
    texto = []
    for p in paragrafos:
        texto_limpo = p.text.strip()
        if texto_limpo:
            texto.append(texto_limpo)
    
    return ''.join(texto).replace('\xa0', '')

def trata_data(materia):
    data = materia.find('time', attrs={'class': 'HeaderNoticiaWrapper__DataPublicacao-sc-4exe2y-3 dAMWSS'})
    data_str = data.text[:10]
    data_obj = datetime.strptime(data_str, '%d/%m/%Y').date()
    
    return data_obj