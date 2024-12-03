from flask import Flask, request
from app import validacao_cadastro
app = Flask(__name__, template_folder='templates') #por default use o nome da pasta templates
app.secret_key = '123456789'

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def register_routes():
    import app.admin
    import app.cliente

register_routes()