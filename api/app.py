import relatorio
import mongoRepository
import json
from flask import Flask
from flask import render_template

app = Flask(__name__)

PORT = 80

@app.route('/relatorio')
def index():
    return render_template('index.html', title='index', dados=relatorio.relatorio())

@app.route('/<int:id_evento>')
def show_post(id_evento):
    db = mongoRepository.get_db()
    evento = db.evento.find_one({"_id": id_evento})
    evento['start_date'] = None;
    return json.dumps(evento)
    
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=PORT)

