#!/usr/bin/env python
# -*- coding: utf-8 -*-
from  html.parser import HTMLParser
import re

'''
    Classe para parser o html de eventos.
    Utiliza a biblioteca HTMLParser 
    https://docs.python.org/3/library/html.parser.html
'''
class HTMLParserEventos(HTMLParser):
    eventos = ""
    def handle_data(self, data):
        data = data.split(' = ')
        if data[0].strip() == "var _search_params":
            eventos = data[1]
            self.eventos = eventos[0:-1]

'''
    Realiza o parser da lista de eventos.
    Parameters
        ----------
        html : str
            Uma string html contendo a lista eventos 
    Returns:
        str
        Uma string json contendo a lista de eventos da pagina
            
'''
def parserEventos(html):
    parser = HTMLParserEventos()
    parser.feed(html)
    return parser.eventos

'''
    Classe para parser o html de informações complementares do evento.
    Utiliza a biblioteca HTMLParser 
    https://docs.python.org/3/library/html.parser.html
'''
class HTMLParserDetalhesEventos(HTMLParser):
    tickets = []
    lastTag = None
    face_event_link = None
    def handle_starttag(self, tag, attrs):
        self.lastTag = tag.strip()
    def handle_data(self, data):
        data = data.strip()
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
        if len(urls) > 0:
            urls = urls[0].split('/events/')
            if len(urls) == 2 and urls[1].isdigit():
                self.face_event_link = urls[0]
                print (urls[0])

        if self.lastTag == 'span' and data[0:2] == 'R$':
            valores = re.findall("\d+\.\d+", data[2:].strip().replace(',','.'))
            if len(valores) > 0:
                ticket = float(valores[0])
                if ticket > 0:
                    self.tickets.append(ticket)
            
'''
    Realiza o parser de informações complementares do evento.
    Parameters
        ----------
        html : str
            Uma string html contendo as informações complementares de um evento 
    Returns:
        dictionary
            As informações complementares de um evento
            ex: {
        'qtd_tickets': 1, 
        'valor_tickets': [0.0], 
        'face_event_link' : None
        }
'''
def parserDetalhesEventos(html):
    parser = HTMLParserDetalhesEventos()
    parser.tickets = []
    parser.lastTag = None
    parser.face_event_link = None
    parser.feed(html)

    if len(parser.tickets) == 0:
        parser.tickets.append(0)
    
    return {
        'qtd_tickets': len(parser.tickets), 
        'valor_tickets': parser.tickets, 
        'face_event_link' :  parser.face_event_link
        }
