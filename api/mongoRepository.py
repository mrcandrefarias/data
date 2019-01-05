#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient

'''
    Conecta-se ao MongoDB.
    Returns:
        Conexão à base de dados sympla (MongoClient)
'''
def get_db():
    #client = MongoClient('mongo:27017')
    client = MongoClient('localhost:27017')
    db     = client['sympla']
    return db

'''
    Processa os eventos armazenados no banco de dados e retornar
    as Localidades com maiores volumes de eventos, quantidade média de lotes por eventos,
    frequência de eventos por dia da semana, maior valor de ingresso,
    quantidade de eventos online e link para evento cadastrado no facebook
    Returns:
        dictionary
        ex: {'cidades': [{'_id': 'Belo Horizonte', 'count': 13}, 
        {'_id': 'São Paulo', 'count': 7}, {'_id': 'Recife', 'count': 7}, 
        {'_id': 'Salvador', 'count': 4}, {'_id': 'Porto Alegre', 'count': 3}], 
        'dias': [{'_id': 'Friday', 'count': 33}, {'_id': 'Saturday', 'count': 28}], 
        'eventos_online': 5, 'media_lotes': 1.8688524590163935, 
        'maior_valor_ingresso': 700.0, 'face_event_link': 0}
'''
def relatorio(): 
    return {
        'cidades': getCidades(), 
        'dias': getDias(), 
        'eventos_online': getEventosOnline(),
        'media_lotes': getMediaLotes(),
        'maior_valor_ingresso': getValorMaximo(),
        'face_event_link' : getEventosLinkFace()
        }

'''
    Consulta e Retorna a frequência de eventos por dia da semana
    Returns:
        list
        ex: [{'_id': 'Friday', 'count': 33}, {'_id': 'Saturday', 'count': 28}]
'''
def getDias():
    pipeline = [
        {"$group": {"_id":"$weekday", "count":{"$sum":1}}}, {"$sort": {"count":-1} }
    ]
    db = get_db()
    return list(db.evento.aggregate(pipeline))

'''
    Consulta e Retorna a lista das cinco cidades com maiores números de eventos
    Returns:
        list
        ex: [{'_id': 'Belo Horizonte', 'count': 13}, 
        {'_id': 'São Paulo', 'count': 7}, {'_id': 'Recife', 'count': 7}, 
        {'_id': 'Salvador', 'count': 4}, {'_id': 'Porto Alegre', 'count': 3}]
''' 
def getCidades():
    pipeline = [
        {"$match": {"location.city": { "$exists": 1}}}, {"$group": {"_id":"$location.city", "count":{"$sum":1}}}, {"$sort": {"count":-1} },{"$limit":5}
    ]
    db = get_db()
    return list(db.evento.aggregate(pipeline))

'''
    Consulta e Retorna o número de eventos que são do tipo online(via internet)
    Returns:
        int
''' 
def getEventosOnline():
    db = get_db()
    return db.evento.find({ 'event_type' : "ONLINE" }).count()

'''
    Retorna o número médio de lotes por evento
    Returns:
        float
'''
def getMediaLotes():
    pipeline = [
        {"$group":{"_id": "id", "media": { "$avg": "$qtd_tickets" }}}
    ]
    db = get_db()
    dados = list(db.evento.aggregate(pipeline))
    for dado in dados:
        return dado['media']

'''
    Consulta e Retorna o valor do ingresso do evento com valor mais elevado
    Returns:
        int
''' 
def getValorMaximo():
    pipeline = [
        {"$group":{"_id": "id", "maxValue": { "$max": "$max_valor_ticket" } }}
    ]
    db = get_db()
    valores = list(db.evento.aggregate(pipeline))
    for valor in valores:
        return valor['maxValue']
    
def getEventosLinkFace():
    db = get_db()
    return db.evento.find({"face_event_link": { "$exists": 1, "$ne": None}}).count()

'''
    Consulta e Retorna as informações do evento pesquisado
    Parameters
        ----------
        id : int
            O id do evento
    Returns:
        dictionary
'''
def getEvento(id):
    db = get_db()
    evento = db.evento.find_one({"_id": id})
    evento['start_date'] = None
    print (evento)
    return evento