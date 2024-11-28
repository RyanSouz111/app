from app import app
from flask import request, render_template

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html', par1='boa tarde', par2='POO')

@app.route("/index") 
def index():
    return render_template('index.html', par1="Boa tarde", par2="Cliente")

@app.route("/cadastro", methods=['GET','POST']) 
def cadastro():
    if request.method == "POST":
        # Coleta os dados enviados pelo formulário
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        print(f"Cadastro realizado com sucesso! Nome: {nome}, Email: {email}")


    return render_template('cadastro.html')

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/alterar_cadastro") 
def alterar_cadastro():
    return render_template("alterar_cadastro.html")

@app.route("/perfil_usuario") 
def perfil_usuario():
    return render_template('perfil_usuario.html')

@app.route("/planos") 
def planos():
    return render_template('planos.html')

@app.route("/pagamentos") 
def pagamentos():
    return render_template('pagamentos.html')

@app.route("/redefinir_senha") 
def redefinir_senha():
    return render_template('redefinir_senha.html')

@app.route("/graficos_historico") 
def graficos_historico():
    return render_template('graficos_historico.html')

@app.route("/graficos_previsao") 
def graficos_previsao():
    return render_template('graficos_previsao.html')

@app.route("/selecionar_folhagem") 
def selecionar_folhagem():
    return render_template('selecionar_folhagem.html')

@app.route("/selecionar_frutas") 
def selecionar_frutas():
    return render_template('selecionar_frutas.html')

@app.route("/selecionar_hortalica") 
def selecionar_hortalica():
    return render_template('selecionar_hortalica.html')

@app.route("/selecionar_previsao") 
def selecionar_previsao():
    return render_template('selecionar_previsao.html')


