from scraper.base_scraper import coleta_materia

def parser(url):
    materia = coleta_materia(url)
    titulo = materia.find('h1', attrs={'class':'content-head__title'})
    subtitulo = materia.find('h2',attrs={'class': 'content-head__subtitle'})
    texto = separa_texto(materia)
    data = materia.find('time', attrs={'itemprop': 'datePublished'})
    
    return texto

def separa_texto(materia):
    paragrafos = materia.find_all('p', attrs={'class':'content-text__container'})
    
    texto = []
    for p in paragrafos:
        temp = p.text
        texto.append(temp)
        
    return "".join(texto)
        

url = input()
teste = parser(url)
print(teste)