import requests
import  htmlParser
import json
import mongoRepository
from datetime import datetime
BASE_URL = 'https://www.sympla.com.br/eventos?ordem=data&pagina=1'

def carregar():
    resp = requests.get(BASE_URL)

    json_data = htmlParser.parserEventos(resp.text)

    dados = json.loads( json_data )
    
    db = mongoRepository.get_db()
    for evento in dados['events']:
        ids = evento['url'].split('__')
        evento['_id'] = int(ids[1])
        evento['start_date'] = datetime.strptime(evento['start_date'],'%Y-%m-%dT%H:%M:%S+00:00' )
        evento['weekday'] = evento['start_date'].strftime("%A")
        carregarDetalhes(evento)
        mongoRepository.savarDados( db,  evento)


def carregarDetalhes(evento):
    print ("carregando url:" + evento['url'])
    resp = requests.get(evento['url'])
    detalhes = htmlParser.parserDetalhesEventos(resp.text)
    evento['valor_tickets'] = detalhes['valor_tickets']
    evento['max_valor_ticket'] = max(detalhes['valor_tickets'])
    evento['qtd_tickets'] = detalhes['qtd_tickets']
    evento['face_event_link'] = detalhes['face_event_link']
    
    


