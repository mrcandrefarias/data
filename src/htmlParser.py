from  html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    eventos = ""
    
    def handle_data(self, data):
        data = data.split('=')
        if data[0].strip() == "var _search_params":
            eventos = data[1]
            self.eventos = eventos[0:-1]

def parser(html):
    parser = MyHTMLParser()
    parser.feed(html)
    return parser.eventos