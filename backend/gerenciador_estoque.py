"""
Módulo gerenciador_estoque.py - Lógica de gerenciamento de estoque

Este módulo implementa as funções e/ou classes responsáveis pela lógica de controle de estoque do sistema.
Inclui operações de entrada, saída, atualização, consulta e validação de produtos no estoque.

Autor: Bruno Novais Costa Simões
Data: 10/07/2025
Versão: 1.0
"""
from datetime import datetime
from banco_dados import BancoDados

class Produto:
    """
    Classe que representa um produto do estoque.
    """
    def __init__(self, id=None, nome="", descricao="", quantidade=0, preco=0.0):
        self.id = id  # Identificador único do produto
        self.nome = nome  # Nome do produto
        self.descricao = descricao  # Descrição do produto
        self.quantidade = quantidade  # Quantidade em estoque
        self.preco = preco  # Preço unitário
    
    def formatar_preco(self):
        """
        Retorna o preço formatado em reais (R$).
        """
        return f"R$ {self.preco:.2f}"

class GerenciadorEstoque:
    """
    Classe responsável por gerenciar as operações de estoque e usuários, utilizando o BancoDados.
    """
    def __init__(self):
        self.bd = BancoDados()  # Instância do gerenciador de banco de dados
        self.bd.criar_tabelas()  # Garante que as tabelas existem

    def adicionar_produto(self, nome, descricao, quantidade, preco, forcar=False):
        """
        Adiciona um novo produto ao estoque.
        Se já existir um produto com o mesmo nome, lança erro, a menos que 'forcar' seja True.
        """
        # Verifica se já existe produto com o mesmo nome (case insensitive)
        produtos_iguais = self.bd.buscar_produto_por_nome(nome)
        existe_igual = any(p[1].strip().lower() == nome.strip().lower() for p in produtos_iguais)
        if existe_igual and not forcar:
            raise ValueError('duplicado')
        self.bd.inserir_produto(nome, descricao, quantidade, preco)

    def editar_produto(self, produto_id, nome, descricao, quantidade, preco):
        """
        Edita os dados de um produto existente.
        """
        self.bd.atualizar_produto(produto_id, nome, descricao, quantidade, preco)

    def remover_produto(self, produto_id):
        """
        Remove um produto do estoque pelo ID.
        """
        self.bd.remover_produto(produto_id)

    def listar_produtos(self):
        """
        Retorna uma lista de objetos Produto com todos os produtos cadastrados.
        """
        return [Produto(*p) for p in self.bd.listar_produtos()]

    def buscar_produto(self, produto_id):
        """
        Busca um produto pelo ID e retorna um objeto Produto ou None se não existir.
        """
        produto = self.bd.buscar_produto(produto_id)
        return Produto(*produto) if produto else None

    def buscar_produtos_por_nome(self, nome):
        """
        Busca produtos pelo nome (busca parcial, case insensitive).
        """
        return [Produto(*p) for p in self.bd.buscar_produto_por_nome(nome)]

    def registrar_venda(self, produto_id, quantidade):
        """
        Registra uma venda de um produto, atualizando o estoque e a tabela de vendas.
        Retorna True se a venda foi realizada, False caso não haja estoque suficiente.
        """
        return self.bd.registrar_venda(produto_id, quantidade)

    def listar_vendas(self):
        """
        Retorna uma lista de dicionários com as vendas realizadas, convertendo datas para objetos datetime.
        """
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
        """
        Retorna o total de produtos vendidos (soma das quantidades de todas as vendas).
        """
        return self.bd.total_produtos_vendidos()

    def total_produtos_estoque(self):
        """
        Retorna o total de produtos em estoque (soma das quantidades de todos os produtos).
        """
        return self.bd.total_produtos_estoque()

    # --- Usuários ---
    def cadastrar_usuario(self, nome, email, cpf, senha):
        """
        Cadastra um novo usuário no sistema.
        Lança erro se o e-mail ou CPF já estiverem cadastrados.
        """
        if self.bd.buscar_usuario_por_email(email):
            raise ValueError('E-mail já cadastrado.')
        if self.bd.buscar_usuario_por_cpf(cpf):
            raise ValueError('CPF já cadastrado.')
        self.bd.inserir_usuario(nome, email, cpf, senha)

    def autenticar_usuario(self, email, senha):
        """
        Autentica um usuário pelo e-mail e senha.
        Retorna o registro do usuário se autenticado, ou None caso contrário.
        """
        usuario = self.bd.buscar_usuario_por_email(email)
        if usuario and usuario[4] == senha:
            return usuario
        return None