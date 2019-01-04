import requests
import  htmlParser
import json
import mongoRepository

BASE_URL = 'https://www.sympla.com.br/eventos?ordem=data&pagina=1'

def carregar():
    resp = requests.get(BASE_URL)

    json_data = htmlParser.parserEventos(resp.text)

    dados = json.loads( json_data )
    
    #db = mongoRepository.get_db()
    for evento in dados['events']:
        detalhes = carregarDetalhes(evento['url'])    
        if detalhes is not None:
            evento['endDate'] = detalhes['endDate']
            evento['description'] = detalhes['description']
        
        #print(detalhes)
        #mongoRepository.savarDados( db,  evento)


def carregarDetalhes(url):
    resp = requests.get("https://www.sympla.com.br/radical-parque-03012019__427917")
    json_data = htmlParser.parserDetalhesEventos(resp.text)
    
    print (json_data)


