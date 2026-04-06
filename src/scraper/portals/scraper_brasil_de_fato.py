from scraper.base_scraper import coleta_materia
from datetime import datetime

def parser(url):
    materia = coleta_materia(url)
    titulo = materia.find('h1', attrs={'class': 'elementor-heading-title elementor-size-default'})
    subtitulo = verifica_subtitulo(materia)
    texto = separa_texto(materia)
    data = trata_data(materia)
    
    return {
        'portal' : 'brasil de fato',
        'titulo' : titulo.text,
        'subtitulo' : subtitulo,
        'texto' : texto,
        'dataPublicacao' : data,
        'url': url,
    }

def verifica_subtitulo(materia):
    h2 = materia.find_all('h2', attrs={'class':'elementor-heading-title elementor-size-default'})
    subtitulo = h2[1]
    
    if subtitulo:
        return subtitulo.text
    else:
        return None

def separa_texto(materia):
    div = materia.find('div', attrs={'class': 'elementor-element elementor-element-8e74bee e-con-full e-flex e-con e-child'})
    paragrafos = div.find_all('p')
    
    texto = []
    for p in paragrafos:
        if p.text.startswith('Apoie a comunicação popular'):
            break
        else:
            temp = p.text
            texto.append(temp)

    return ''.join(texto).replace('\xa0', '')

def trata_data(materia):
    meses = {                                                                                                                                                  
      'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04', 'mai': '05', 'jun': '06',                                                                                                                 
      'jul': '07', 'ago': '08', 'set': '09','out': '10', 'nov': '11', 'dez': '12'                                                                                                                  
}     
    
    time = materia.find('time')
    data_str = time.text.split('-')[0].replace(' ', '')
    data_str = data_str.replace('.', '/')
    
    for mes, numero in meses.items():
        data_str = data_str.replace(mes, numero)
    
    data_obj = datetime.strptime(data_str, '%d/%m/%Y').date()
    return data_obj