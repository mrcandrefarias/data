import relatorio

from flask import Flask
from flask import render_template

app = Flask(__name__)

PORT = 80

@app.route('/index')
def index():
    return render_template('index.html', title='index', dados=relatorio.relatorio())

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=PORT)

