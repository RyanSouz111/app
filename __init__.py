from flask import Flask
app = Flask(__name__, template_folder='view') #por default use o nome da pasta templates
def register_routes():
    import app.admim
    import app.cliente

register_routes()
