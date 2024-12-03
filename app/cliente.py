from app import app
from flask import request, render_template, redirect, url_for, session
from functools import wraps
from app.validacao_cadastro import BancoDeDados, Cliente
from app.plot_serie_historica import plotar_serie_historica
import json
import os

bd = BancoDeDados()

# Função para verificar se há um usuário logado

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_atual' not in session:  # Verifique se a sessão contém o usuário
            return redirect(url_for('login'))  # Redirecione para a página de login
        return f(*args, **kwargs)
    return decorated_function

# Função para ler JSON

def carregar_dados_json(arquivo):
    caminho_arquivo = os.path.join(app.root_path, 'static', 'JSON', f'{arquivo}.json')
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        dados = json.load(file)
    return dados

# Index

@app.route("/", methods=['GET'])
def home():
    print("Renderizar Home chamado.")
    if 'usuario_atual' in session:
        return redirect(url_for('selecionar_previsao'))
    else:
        return render_template('index.html')

@app.route("/index") 
def index():
    print("Renderizar Home chamado.")
    if 'usuario_atual' in session:
        return redirect(url_for('selecionar_previsao'))
    else:
        return render_template('index.html')

# Cadastro e Login

@app.route("/cadastro", methods=['GET','POST']) 
def cadastro():
    print("Cadastro renderizado.")
    if 'usuario_atual' in session:
        return redirect(url_for('selecionar_previsao'))
    else:
        return render_template('cadastro.html', cadastrado=False)

@app.route("/cadastrar", methods=['GET','POST']) 
def cadastrarCliente():
    print("Cadastrar Cliente chamado.")
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    telefone = request.form.get("telefone")
    cep = request.form.get("cep")
    nascimento = request.form.get("nascimento")
    cpf = request.form.get("cpf")

    cliente = Cliente(nome, cpf, telefone, nascimento, cep, email, senha)
    print("Objeto da classe cliente criado.")
    print(cliente)
    req = bd.adicionar_cliente(cliente)

    if req == 'Já cadastrado':
        print("Usuário já cadastrado.")
        return render_template('cadastro.html', cadastrado=True)

    print("Usuário criado com sucesso!")
    session['usuario_atual'] = cliente.__dict__
    return redirect(url_for('planos'))

@app.route("/login", methods=['GET','POST'])
def login():
    print("Renderizar Login chamado.")
    if 'usuario_atual' in session:
        return redirect(url_for('selecionar_previsao'))
    else:
        return render_template("login.html", usuario_nao_existe=False)

@app.route("/autentica", methods=['POST'])
def autentica():
    email = request.form.get("email")
    senha = request.form.get("senha")

    print(f"Autenticação sendo feito para {email}...")
    user = bd.autenticar_clientes(email, senha)

    if user:
        print(f"Login realizado: {email}.")
        session['usuario_atual'] = user.__dict__
        return redirect(url_for('selecionar_previsao'))
    else:
        print("Usuário não encontrado. Redirecionando para login.")
        return render_template("login.html", usuario_nao_existe=True)

@app.route("/sair")
@login_required
def sair():
    print("Deslogando usuário da sessão.")
    session.pop('usuario_atual', None)
    return redirect(url_for('login'))

# Alteração de planos, cadastro e senha

@app.route("/perfil_usuario") 
@login_required
def perfil_usuario():
    usuario_atual = session['usuario_atual']
    print(f"Perfil do usuário chamado para usuário {usuario_atual}.")
    return render_template('perfil_usuario.html', user=usuario_atual)

@app.route("/alterar_cadastro") 
@login_required
def alterar_cadastro():
    print(f"Alterar cadastro chamado para usuário {session['usuario_atual']}.")
    return render_template("alterar_cadastro.html", telefone=session['usuario_atual']['telefone'], cep=session['usuario_atual']['cep'])

@app.route("/atualizar_cadastro", methods=['POST'])
@login_required
def atualizar_cadastro():
    print("Atualizar cadastro chamado.")
    telefone = request.form.get("telefone")
    cep = request.form.get("cep")
    print(f"Dados para atualizar: telefone {telefone}, CEP {cep}.")

    cliente = bd.encontrar_cliente_por_id(session['usuario_atual']['id'])

    if telefone:
        cliente.telefone = telefone

    if cep:
        cliente.cep = cep

    session['usuario_atual'] = cliente.__dict__
    return redirect(url_for('perfil_usuario'))

@app.route("/alterar_plano") 
@login_required
def alterar_plano():
    print("Alterar plano chamado.")
    return render_template("alterar_plano.html")

@app.route("/alterar_senha") 
@login_required
def alterar_senha():
    print("Alterar senha chamado.")
    return render_template("alterar_senha.html", senhas_iguais=True)

@app.route("/atualizar_senha", methods=['POST'])
@login_required
def atualizar_senha():
    print("Atualizar senha chamado.")
    if request.method == 'POST':
        senha = request.form.get("nova_senha")
        confirmar_senha = request.form.get("nova_senha_confirmar")

        if senha and confirmar_senha != None:
            print("Senhas não vazias.")
            if senha == confirmar_senha:
                print("Senhas são iguais.")
                cliente = bd.encontrar_cliente_por_id(session['usuario_atual']['id'])
                cliente.senha = senha
                return redirect(url_for('perfil_usuario'))
            else:
                print("Senhas não são iguais. Redirecionando para a tela de alterar senha novamente.")
                return redirect(url_for('alterar_senha', senhas_iguais=False))

    print("Senha alterada.")
    return render_template('alterar_senha.html', senhas_iguais=False)

# Planos e Pagamento

@app.route("/planos") 
@login_required
def planos():
    print("Planos chamado.")
    return render_template('planos.html')

@app.route("/assinar_plano", methods=['POST'])
@login_required
def assinar_plano():
    print("Assinar plano chamado.")
    plano = request.form.get("tipo_plano")
    print(f"Plano escolhido: {plano}")
    return redirect(url_for('pagamento', plano=plano))

@app.route("/pagamento") 
@login_required
def pagamento():
    print("Renderizar pagamento chamado.")
    plano = request.args.get('plano')
    return render_template('pagamento.html', plano=plano)

@app.route("/pagar", methods=["POST"]) 
@login_required
def pagar():
    print("Pagamento chamado.")
    pagamento = request.form.get("forma_pagamento")
    plano = request.form.get("plano")
    print(f"Plano escolhido: {plano}. Forma de pagamento escolhido: {pagamento}.")
    cliente = bd.encontrar_cliente_por_id(session['usuario_atual']['id'])
    cliente.alterar_plano(plano)
    cliente.forma_pagamento = pagamento

    session['usuario_atual'] = cliente.__dict__

    return redirect(url_for('perfil_usuario'))

# Histórico e Previsões

@app.route("/selecionar_previsao")
@login_required
def selecionar_previsao():
    print("Renderizar selecionar a previsão chamado.")
    return render_template('selecionar_previsao.html')

@app.route("/graficos_historico/<item>") 
@login_required
def graficos_historico(item):
    print(f"Gráfico do Histórico chamado para item {item}.")
    grafico = plotar_serie_historica('Pcomum', item)
    return render_template('graficos_historico.html', item=item, grafico=grafico)

@app.route("/graficos_previsao/<item>") 
@login_required
def graficos_previsao(item):
    print(f"Grafico de Previsão chamado para item {item}.")
    return render_template('graficos_previsao.html', item=item)

@app.route("/selecionar_folhagem") 
@login_required
def selecionar_folhagem():
    print("Renderizado selecionar folhagem.")
    dados = carregar_dados_json('folhagens')
    return render_template('selecionar_folhagem.html', dados=dados)

@app.route("/selecionar_frutas") 
@login_required
def selecionar_frutas():
    print("Renderizado selecionar fruta.")
    dados = carregar_dados_json('frutas')
    return render_template('selecionar_frutas.html', dados=dados)

@app.route("/selecionar_hortalica") 
@login_required
def selecionar_hortalica():
    print("Renderizado selecionar hortaliça.")
    dados = carregar_dados_json('hortalicas')
    return render_template('selecionar_hortalica.html', dados=dados)