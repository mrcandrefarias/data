from  html.parser import HTMLParser
import re
class HTMLParserEventos(HTMLParser):
    eventos = ""
    def handle_data(self, data):
        data = data.split('=')
        if data[0].strip() == "var _search_params":
            eventos = data[1]
            self.eventos = eventos[0:-1]

def parserEventos(html):
    parser = HTMLParserEventos()
    parser.feed(html)
    return parser.eventos

class HTMLParserDetalhesEventos(HTMLParser):
    tickets = []
    lastTag = None
    def handle_starttag(self, tag, attrs):
        self.lastTag = tag.strip()
    def handle_data(self, data):
        data = data.strip()
        #urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+, data)
        
        if self.lastTag == 'span' and data[0:2] == 'R$':
            valores = re.findall("\d+\.\d+", data[2:].strip().replace(',','.'))
            if len(valores) > 0:
                ticket = float(valores[0])
                if ticket > 0:
                    self.tickets.append(ticket)
            

def parserDetalhesEventos(html):
    parser = HTMLParserDetalhesEventos()
    parser.tickets = []
    parser.lastTag = None
    parser.feed(html)

    if len(parser.tickets) == 0:
        parser.tickets.append(0)
    
    return {'qtd_tickets': len(parser.tickets), 'valor_tickets': parser.tickets, 'face_event_link' : "" }
