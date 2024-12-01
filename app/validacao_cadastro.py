class ContaCliente:
    def __init__(self):
        self.armazenar_dados_clientes = {}

    def adicionar_cliente(self, nome, cpf, id, email, senha, telefone, cep, nascimento):
        if email in [cliente['email'] for cliente in self.armazenar_dados_clientes.values()] or cpf in [cliente['cpf']for cliente in self.armazenar_dados_clientes.values()]:
            return f'já cadastrado'
        self.armazenar_dados_clientes[id] = {'nome': nome, 'cpf': cpf, 'email': email, 'senha': senha, 'telefone': telefone, 'cep': cep, 'nascimento': nascimento}
        print(self.listar_clientes())
        return f'cadastrado com sucesso!'

    def remover_cliente(self, id):
        if id in self.armazenar_dados_clientes:
            del self.armazenar_dados_clientes[id]
            return f'cliente removido'
        else:
            return f'não encontrado'

    def listar_clientes(self):
        return list(self.armazenar_dados_clientes.values())

    def autenticar_clientes(self, email, senha):
        verificacao = any(cliente['email'] == email and cliente['senha'] == senha for cliente in self.armazenar_dados_clientes.values())
        return verificacao
