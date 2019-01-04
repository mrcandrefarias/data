import mongoRepository

def relatorio():
    
    return {
        'cidades': getCidades(), 
        'dias': getDias(), 
        'eventos_online': getEventosOnline(),
        'media_lotes': getMediaLotes(),
        'maior_valor_ingresso': getValorMaximo(),
        'face_event_link' : getEventosLinkFace()
        }
    
def getDias():
    pipeline = [
        {"$group": {"_id":"$weekday", "count":{"$sum":1}}}, {"$sort": {"count":-1} }
    ]
    db = mongoRepository.get_db()
    return list(db.evento.aggregate(pipeline))
    
def getCidades():
    pipeline = [
        {"$match": {"location.city": { "$exists": 1}}}, {"$group": {"_id":"$location.city", "count":{"$sum":1}}}, {"$sort": {"count":-1} },{"$limit":5}
    ]
    db = mongoRepository.get_db()
    return db.evento.aggregate(pipeline)
    
def getEventosOnline():
    db = mongoRepository.get_db()
    return db.evento.find({ 'event_type' : "ONLINE" }).count()

def getMediaLotes():
    pipeline = [
        {"$group":{"_id": "id", "media": { "$avg": "$qtd_tickets" }}}
    ]
    db = mongoRepository.get_db()
    return db.evento.aggregate(pipeline)
    
def getValorMaximo():
    pipeline = [
        {"$group":{"_id": "id", "maxValue": { "$max": "$max_valor_ticket" } }}
    ]
    db = mongoRepository.get_db()
    return list(db.evento.aggregate(pipeline))

def getEventosLinkFace():
    db = mongoRepository.get_db()
    return db.evento.find({"face_event_link": { "$exists": 1}}).count()
    
    

    
    

