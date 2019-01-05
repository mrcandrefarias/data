#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mongoRepository
import json
from flask import Flask
from flask import render_template

app = Flask(__name__)
PORT = 80

'''
    Serviço responsável por processar e retornar as seguintes informações
      - Localidades com maiores volumes de eventos
      - Quantidade média de lotes (tipos de tickets) por eventos
      - Frequência de eventos por dia da semana
      - Maior valor de ingresso
    Returns:
        html
'''
@app.route('/relatorio', methods=['GET'])
def index():
    return render_template('index.html', title='index', dados=mongoRepository.relatorio())

'''
    Serviço responsável Retornar as informações de um determinado evento
    Parameters
        ----------
        id : int
            O id do evento
    Returns:
        As informações do evento em formato json
        ex: {"_id": 419998, "event_type": "NORMAL", 
        "images": {"lg": "https://images.sympla.com.br/5c09406677d9c-lg.png", 
        "original": "https://images.sympla.com.br/5c09406677d9c.png", 
        "xs": "https://images.sympla.com.br/5c09406677d9c-xs.png"}, 
        "location": {"address": "Avenida Professor M\u00e1rio Werneck", 
        "address_alt": "", "address_num": "530", "city": "Belo Horizonte", 
        "lat": -19.968206, "lon": -43.9575261, "name": "Quintal do Chal\u00e9", 
        "neighborhood": "Estoril", "state": "MG", "zip_code": "30455-610"}, 
        "start_date": null, "title": "SEXTA NO QUINTAL - 4-01", 
        "url": "https://www.sympla.com.br/sexta-no-quintal---4-01__419998", 
        "weekday": "Friday", "valor_tickets": [5.0, 10.0], "max_valor_ticket": 10.0, 
        "qtd_tickets": 2, "face_event_link": null}
'''
@app.route('/<int:id_evento>', methods=['GET'])
def show_post(id_evento):
    print (id_evento)
    return json.dumps(mongoRepository.getEvento(id_evento))
    
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=PORT)

