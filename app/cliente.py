from app import app
from flask import request, render_template, redirect, url_for

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/index") 
def index():
    return render_template('index.html', par1="Boa tarde", par2="Cliente")

@app.route("/cadastro", methods=['GET','POST']) 
def cadastro():
    return render_template('cadastro.html')

@app.route("/cadastrar", methods=['GET','POST']) 
def cadastrarCliente():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    telefone = request.form.get("telefone")
    cep = request.form.get("cep")
    nascimento = request.form.get("nascimento")
    cpf = request.form.get("cpf")
    print(f"Cadastro realizado com sucesso! Nome: {nome}, Email: {email}")
    return render_template('planos.html')

@app.route("/login", methods=['GET','POST'])
def login():
    return render_template("login.html")

@app.route("/autentica", methods=['POST'])
def autentica():
    email = request.form.get("email")
    senha = request.form.get("senha")
    print(f"Login realizado: {email}.")
    return redirect(url_for('selecionar_previsao'))

@app.route("/selecionar_previsao")
def selecionar_previsao():
    return render_template('selecionar_previsao.html')

# Alterar Informações

@app.route("/alterar_cadastro") 
def alterar_cadastro():
    return render_template("alterar_cadastro.html")

@app.route("/atualizar_cadastro", methods=['POST'])
def atualizar_cadastro():
    nome = request.form.get("nome")
    telefone = request.form.get("telefone")
    cep = request.form.get("cep")

    print(nome, telefone, cep)

@app.route("/alterar_plano") 
def alterar_plano():
    return render_template("alterar_plano.html")

@app.route("/alterar_senha") 
def alterar_senha():
    return render_template("alterar_senha.html")

@app.route("/atualizar_senha", methods=['POST'])
def atualizar_senha():
    senha = request.form.get("nova_senha")
    print(senha)
    return redirect(url_for('perfil_usuario'))

@app.route("/atualizar_plano", methods=['POST'])
def atualizar_plano():
    plano = request.form.get("plano")
    print(plano)

# 

@app.route("/perfil_usuario") 
def perfil_usuario():
    return render_template('perfil_usuario.html')

@app.route("/planos") 
def planos():
    return render_template('planos.html')

# Pagamento

@app.route("/pagamento") 
def pagamento():
    return render_template('pagamento.html')

@app.route("/pagar", methods=["POST"]) 
def pagar():
    pagamento = request.form.get("forma_pagamento")
    return redirect(url_for('perfil_usuario'))

# Senhas

@app.route("/redefinir_senha") 
def redefinir_senha():
    return render_template('redefinir_senha.html')

# Histórico e Previsões

@app.route("/graficos_historico/<item>") 
def graficos_historico(item):
    print(item)
    return render_template('graficos_historico.html', item=item)

@app.route("/graficos_previsao/<item>") 
def graficos_previsao(item):
    print(item)
    return render_template('graficos_previsao.html', item=item)

@app.route("/selecionar_folhagem") 
def selecionar_folhagem():
    return render_template('selecionar_folhagem.html')

@app.route("/selecionar_frutas") 
def selecionar_frutas():
    return render_template('selecionar_frutas.html')

@app.route("/selecionar_hortalica") 
def selecionar_hortalica():
    return render_template('selecionar_hortalica.html')


