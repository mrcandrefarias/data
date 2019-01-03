import requests
import  htmlParser
import json
import mongoRepository

BASE_URL = 'https://www.sympla.com.br/eventos?ordem=data&pagina=1'

def carregar():
    resp = requests.get(BASE_URL)

    json_data = htmlParser.parser(resp.text)

    dados = json.loads( json_data )

    mongoRepository.savarDados( dados['events'] )
