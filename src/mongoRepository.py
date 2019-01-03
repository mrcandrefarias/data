#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient

def get_db():
    '''
        Conecta-se ao MongoDB.
        Returns:
            Conexão à base de dados bh-osm (MongoClient)
    '''
    client = MongoClient('mongo:27017')
    db     = client['eventos']
    return db

def savarDados(eventos):
    db = get_db()
    for evento in eventos:
        print(evento)
        print(":")
        db.evento.save(evento)
        
    