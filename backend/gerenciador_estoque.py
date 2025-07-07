from datetime import datetime
from banco_dados import BancoDados


class Produto:
    def __init__(self, id=None, nome="", descricao="", quantidade=0, preco=0.0):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.quantidade = quantidade
        self.preco = preco
    
    def formatar_preco(self):
        return f"R$ {self.preco:.2f}"

class GerenciadorEstoque:
    def __init__(self):
        self.bd = BancoDados()
        self.bd.criar_tabelas()

    def adicionar_produto(self, nome, descricao, quantidade, preco, forcar=False):
        # Verifica se já existe produto com o mesmo nome
        produtos_iguais = self.bd.buscar_produto_por_nome(nome)
        existe_igual = any(p[1].strip().lower() == nome.strip().lower() for p in produtos_iguais)
        if existe_igual and not forcar:
            raise ValueError('duplicado')
        self.bd.inserir_produto(nome, descricao, quantidade, preco)

    def editar_produto(self, produto_id, nome, descricao, quantidade, preco):
        self.bd.atualizar_produto(produto_id, nome, descricao, quantidade, preco)

    def remover_produto(self, produto_id):
        self.bd.remover_produto(produto_id)

    def listar_produtos(self):
        return [Produto(*p) for p in self.bd.listar_produtos()]

    def buscar_produto(self, produto_id):
        produto = self.bd.buscar_produto(produto_id)
        return Produto(*produto) if produto else None

    def buscar_produtos_por_nome(self, nome):
        return [Produto(*p) for p in self.bd.buscar_produto_por_nome(nome)]

    def registrar_venda(self, produto_id, quantidade):
        return self.bd.registrar_venda(produto_id, quantidade)

    def listar_vendas(self):
        vendas = self.bd.listar_vendas()
        return [{
            'id': v[0],
            'produto_nome': v[1],
            'quantidade': v[2],
            'preco_unitario': v[3],
            'total': v[4],
            'data': datetime.strptime(v[5], '%Y-%m-%d %H:%M:%S')
        } for v in vendas]

    def total_produtos_vendidos(self):
        return self.bd.total_produtos_vendidos()

    def total_produtos_estoque(self):
        return self.bd.total_produtos_estoque()

    # --- Usuários ---
    def cadastrar_usuario(self, nome, email, cpf, senha):
        if self.bd.buscar_usuario_por_email(email):
            raise ValueError('E-mail já cadastrado.')
        if self.bd.buscar_usuario_por_cpf(cpf):
            raise ValueError('CPF já cadastrado.')
        self.bd.inserir_usuario(nome, email, cpf, senha)

    def autenticar_usuario(self, email, senha):
        usuario = self.bd.buscar_usuario_por_email(email)
        if usuario and usuario[4] == senha:
            return usuario
        return None