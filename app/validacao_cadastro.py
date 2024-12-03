from datetime import datetime, timedelta

class Cliente:
    id = 0

    def __init__(self, nome, cpf, cep, telefone, nascimento, email, senha):
        self.id = Cliente.id
        Cliente.id += 1
        self.nome = nome
        self.cpf = cpf
        self.cep = cep
        self.telefone = telefone
        self.nascimento = nascimento
        self.email = email
        self.senha = senha
        self.plano_atual = 'silver'
        self.forma_pagamento = None
        self.creditos_restantes = 3
        self.__data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def alterar_plano(self, plano):
        print(f"(Objeto) Alterando plano do cliente: {plano}.")
        self.plano_atual = plano
        
        if plano == 'silver':
            self.creditos_restantes = 3
        elif plano == 'gold':
            self.creditos_restantes = 20
        elif plano == 'diamond':
            self.creditos_restantes = 9999

    def __str__(self):
        return f"""
        Cliente #{self.id}
            Nome: {self.nome}
            CPF: {self.cpf}
            CEP: {self.cep}
            Telefone: {self.telefone}
            Nascimento: {self.nascimento}
            Email: {self.email}
            Plano Atual: {self.plano_atual}
            Pagamento: {self.forma_pagamento}
            Creditos Restantes: {self.creditos_restantes}
        """

class BancoDeDados:
    def __init__(self):
        self.armazenar_dados_clientes = []

    def adicionar_cliente(self, novo_cliente):
        if any(novo_cliente.email == cliente.email or novo_cliente.cpf == cliente.cpf for cliente in self.armazenar_dados_clientes):
            return 'Já cadastrado'

        self.armazenar_dados_clientes.append(novo_cliente)
        return 'OK'

    def remover_cliente(self, id):
        cliente_para_remover = self.encontrar_cliente_por_id(id)
        if cliente_para_remover:
            self.armazenar_dados_clientes.remove(cliente_para_remover)
            return f'Cliente removido.'
        else:
            return f'Não encontrado.'

    def listar_clientes(self):
        for cliente in self.armazenar_dados_clientes:
            print(cliente.nome, cliente.email, cliente.senha, cliente.telefone) 

    def autenticar_clientes(self, email, senha):
        if any(cliente.email == email and cliente.senha == senha for cliente in self.armazenar_dados_clientes):
            cliente = next((cliente for cliente in self.armazenar_dados_clientes if cliente.email == email and cliente.senha == senha), None)
            return cliente            
        else:
            return False

    def encontrar_cliente_por_id(self, id):
        print(f"Procurando cliente com ID {id}...")
        return next((cliente for cliente in self.armazenar_dados_clientes if cliente.id == id), None)