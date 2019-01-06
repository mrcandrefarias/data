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
    client = MongoClient('mongo:27017')
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

    print ("Finalizado carregamento eventos, parte 1")

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
    try:
        dados = json.loads( json_data )
    except Exception:
        print ("Erro json")
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
        evento['detalhes'] = 0
        #salva o evento no banco de dados
        db.evento.save(evento)

'''
    Busca os detalhes dos eventos salvos no banco no site da sympla,
    processa os dados e aggrega outras informações aos eventos.
    Feito isso, o evento é atualizado no banco de dados
'''
def carregarDetalhesEventos():
    db = get_db()
    # coleta os eventos que não possuem informações detalhadas
    # Carrega somente 10 eventos por vez, para não sobrecarregar o script
    eventos = db.evento.find({"detalhes": 0}).limit(10)
    for evento in eventos:
        formatarSalvarDetalhesEventos(evento, db)
     
    eventos_sem_detalhes = db.evento.find({"detalhes": 0}).count()
    # enquanto houver eventos_sem_detalhes, chama recursivamente
    # a função carregarDetalhesEventos()
    if eventos_sem_detalhes:
        # chamada recursiva
        carregarDetalhesEventos()

def formatarSalvarDetalhesEventos(evento, db):
    resp = requests.get(evento['url'])
    detalhes = htmlParser.parserDetalhesEventos(resp.text)
    # altera o valor de detalhes para 1, dessa forma
    # é possível identificar que o evento já foi atualizado
    # com informações adicionais
    evento['detalhes'] = 1
    
    evento['valor_tickets'] = detalhes['valor_tickets']
    evento['max_valor_ticket'] = max(detalhes['valor_tickets'])
    evento['qtd_tickets'] = detalhes['qtd_tickets']
    evento['face_event_link'] = detalhes['face_event_link']
    
    #salva as alterações do evento no banco de dados
    db.evento.save(evento)


