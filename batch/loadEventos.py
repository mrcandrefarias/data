#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import  htmlParser
import json
from datetime import datetime
from pymongo import MongoClient
BASE_URL = 'https://www.sympla.com.br/eventos?ordem=data&pagina='

'''
    Conecta-se ao MongoDB.
    Returns:
        Conexão à base de dados bh-osm (MongoClient)
'''
def get_db():
    
    #client = MongoClient('mongo:27017')
    client = MongoClient('localhost:27017')
    db     = client['sympla']
    return db

'''
    Busca a pagina com a lista de eventos da Sympla,
    processa esses informações e salva os dados dos eventos
    no banco de dados mongodb
'''
def buscarEventos():
    # As informações são disponibilizados no site da sympla de forma paginada
    # Inicia a leitura dos eventos da pagina 1 até à pagina 100    
    for x in range(1, 100):
        url = BASE_URL + str(x)
        print(url)
        html_eventos = buscarPaginaHtml(url) 
        eventos = parserHtmlPaginaEventos( html_eventos ) 
        formatarSalvarEventos(eventos)
        
'''
    Busca a pagina Html da url recebida como parametro  e a retorna em formato texto. 
    Para tal, é usado a biblioteca request (http://docs.python-requests.org/en/master/)
    Parameters
        ----------
        url : str
            A url a ser processada. ex https://www.sympla.com.br/eventos?ordem=data&pagina=1
    Returns:
        str 
'''
def buscarPaginaHtml(url):
    resp = requests.get(url)
    return resp.text    

'''
    Recebe a String  Html da sympla, coleta e retorna os eventos 
    Parameters
        ----------
        html : str
            String Html da página de eventos da sympla
    Returns:
        dictionary
'''
def parserHtmlPaginaEventos(html):
    json_data = htmlParser.parserEventos(html)
    dados = json.loads( json_data )
    return dados['events']

'''
    Recebe os eventos do parametro, formata e salva os dados no mongodb 
    Parameters
        ----------
        eventos : dictionary
            dictionary contendo os eventos da sympla
'''
def formatarSalvarEventos(eventos):
    db = get_db()
    for evento in eventos:
        ids = evento['url'].split('__')
        evento['_id'] = int(ids[1])
        evento['start_date'] = datetime.strptime(evento['start_date'],'%Y-%m-%dT%H:%M:%S+00:00' )
        evento['weekday'] = evento['start_date'].strftime("%A")
        #carregarDetalhes(evento)
        db.evento.save(evento)

def carregarDetalhes(evento):
    resp = requests.get(evento['url'])
    detalhes = htmlParser.parserDetalhesEventos(resp.text)
    evento['valor_tickets'] = detalhes['valor_tickets']
    evento['max_valor_ticket'] = max(detalhes['valor_tickets'])
    evento['qtd_tickets'] = detalhes['qtd_tickets']
    evento['face_event_link'] = detalhes['face_event_link']



