from flask import Flask 
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def hello():
    return ('login.html')


@app.route('/cadastrar_two')
def cadastro():
    return ('cadastro.html')