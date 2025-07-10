"""
Módulo banco_dados.py - Gerenciamento do banco de dados do sistema de controle de estoque

Este módulo contém funções e/ou classes responsáveis pela conexão, manipulação e operações no banco de dados utilizado pelo sistema.
Inclui criação de tabelas, inserção, atualização, exclusão e consultas de dados.

Autor: Bruno Novais Costa Simões
Data: 10/07/2025
Versão: 1.0
"""
import sqlite3
from datetime import datetime
import os

class BancoDados:
    """
    Classe responsável por gerenciar a conexão e as operações no banco de dados SQLite.
    """
    def __init__(self, nome_bd=None):
        """
        Inicializa o caminho do banco de dados. Se não for informado, usa o padrão na pasta data.
        """
        caminho_padrao = os.path.join(os.path.dirname(__file__), '..', 'data', 'estoque.db')
        self.nome_bd = nome_bd or os.path.abspath(caminho_padrao)
        self.conexao = None  # Conexão com o banco
        self.cursor = None   # Cursor para executar comandos SQL

    def conectar(self):
        """
        Abre a conexão com o banco de dados e inicializa o cursor.
        """
        self.conexao = sqlite3.connect(self.nome_bd)
        self.cursor = self.conexao.cursor()

    def desconectar(self):
        """
        Fecha a conexão com o banco de dados, se estiver aberta.
        """
        if self.conexao:
            self.conexao.close()
        self.conexao = None
        self.cursor = None

    def criar_tabelas(self):
        """
        Cria as tabelas principais do sistema (produtos, vendas, usuarios) caso não existam.
        """
        self.conectar()

        # Tabela de produtos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                quantidade INTEGER,
                preco REAL
            )
        ''')

        # Tabela de vendas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                produto_nome TEXT NOT NULL,
                quantidade INTEGER,
                preco_unitario REAL,
                total REAL,
                data TEXT NOT NULL
            )
        ''')

        # Tabela de usuários
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                cpf TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        ''')

        self.conexao.commit()
        self.desconectar()

    def inserir_produto(self, nome, descricao, quantidade, preco):
        """
        Insere um novo produto na tabela produtos.
        """
        self.conectar()
        self.cursor.execute('''
            INSERT INTO produtos (nome, descricao, quantidade, preco)
            VALUES (?, ?, ?, ?)
        ''', (nome, descricao, quantidade, preco))
        self.conexao.commit()
        self.desconectar()

    def atualizar_produto(self, produto_id, nome, descricao, quantidade, preco):
        """
        Atualiza os dados de um produto existente pelo ID.
        """
        self.conectar()
        self.cursor.execute('''
            UPDATE produtos
            SET nome=?, descricao=?, quantidade=?, preco=?
            WHERE id=?
        ''', (nome, descricao, quantidade, preco, produto_id))
        self.conexao.commit()
        self.desconectar()

    def remover_produto(self, produto_id):
        """
        Remove um produto do banco de dados pelo ID.
        """
        self.conectar()
        self.cursor.execute('DELETE FROM produtos WHERE id=?', (produto_id,))
        self.conexao.commit()
        self.desconectar()

    def listar_produtos(self):
        """
        Retorna uma lista com todos os produtos cadastrados, ordenados por nome.
        """
        self.conectar()
        self.cursor.execute('SELECT * FROM produtos ORDER BY nome')
        produtos = self.cursor.fetchall()
        self.desconectar()
        return produtos

    def buscar_produto(self, produto_id):
        """
        Busca um produto pelo ID.
        """
        self.conectar()
        self.cursor.execute('SELECT * FROM produtos WHERE id=?', (produto_id,))
        produto = self.cursor.fetchone()
        self.desconectar()
        return produto

    def buscar_produto_por_nome(self, nome):
        """
        Busca produtos cujo nome contenha o termo informado (busca parcial).
        """
        self.conectar()
        self.cursor.execute('SELECT * FROM produtos WHERE nome LIKE ?', (f'%{nome}%',))
        produtos = self.cursor.fetchall()
        self.desconectar()
        return produtos

    def registrar_venda(self, produto_id, quantidade):
        """
        Registra uma venda de um produto, atualizando o estoque e inserindo o registro na tabela de vendas.
        Retorna True se a venda foi realizada, False se não havia estoque suficiente.
        """
        self.conectar()
        self.cursor.execute('SELECT nome, quantidade, preco FROM produtos WHERE id=?', (produto_id,))
        resultado = self.cursor.fetchone()

        if resultado:
            nome_produto, estoque, preco_unitario = resultado
            if estoque >= quantidade:
                novo_estoque = estoque - quantidade
                # Atualiza o estoque do produto
                self.cursor.execute('UPDATE produtos SET quantidade=? WHERE id=?',
                                    (novo_estoque, produto_id))

                total = preco_unitario * quantidade
                data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # Insere o registro da venda
                self.cursor.execute('''
                    INSERT INTO vendas (produto_id, produto_nome, quantidade, preco_unitario, total, data)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (produto_id, nome_produto, quantidade, preco_unitario, total, data))

                self.conexao.commit()
                self.desconectar()
                return True  # Venda realizada

        self.desconectar()
        return False  # Estoque insuficiente ou produto não encontrado

    def listar_vendas(self):
        """
        Retorna uma lista com todas as vendas realizadas, ordenadas da mais recente para a mais antiga.
        """
        self.conectar()
        self.cursor.execute('''
            SELECT id, produto_nome, quantidade, preco_unitario, total, data FROM vendas
            ORDER BY data DESC
        ''')
        vendas = self.cursor.fetchall()
        self.desconectar()
        return vendas

    def total_produtos_vendidos(self):
        """
        Retorna o total de produtos vendidos (soma das quantidades de todas as vendas).
        """
        self.conectar()
        self.cursor.execute('SELECT SUM(quantidade) FROM vendas')
        total = self.cursor.fetchone()[0] or 0
        self.desconectar()
        return total

    def total_produtos_estoque(self):
        """
        Retorna o total de produtos em estoque (soma das quantidades de todos os produtos).
        """
        self.conectar()
        self.cursor.execute('SELECT SUM(quantidade) FROM produtos')
        total = self.cursor.fetchone()[0] or 0
        self.desconectar()
        return total

    # Métodos de usuário
    def inserir_usuario(self, nome, email, cpf, senha):
        """
        Insere um novo usuário na tabela de usuários.
        """
        self.conectar()
        self.cursor.execute('''
            INSERT INTO usuarios (nome, email, cpf, senha)
            VALUES (?, ?, ?, ?)
        ''', (nome, email, cpf, senha))
        self.conexao.commit()
        self.desconectar()

    def buscar_usuario_por_email(self, email):
        """
        Busca um usuário pelo e-mail.
        """
        self.conectar()
        self.cursor.execute('SELECT * FROM usuarios WHERE email=?', (email,))
        usuario = self.cursor.fetchone()
        self.desconectar()
        return usuario

    def buscar_usuario_por_cpf(self, cpf):
        """
        Busca um usuário pelo CPF.
        """
        self.conectar()
        self.cursor.execute('SELECT * FROM usuarios WHERE cpf=?', (cpf,))
        usuario = self.cursor.fetchone()
        self.desconectar()
        return usuario
