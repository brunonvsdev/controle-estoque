import sqlite3
from datetime import datetime
import os

class BancoDados:
    def __init__(self, nome_bd=None):
        caminho_padrao = os.path.join(os.path.dirname(__file__), '..', 'data', 'estoque.db')
        self.nome_bd = nome_bd or os.path.abspath(caminho_padrao)
        self.conexao = None
        self.cursor = None

    def conectar(self):
        self.conexao = sqlite3.connect(self.nome_bd)
        self.cursor = self.conexao.cursor()

    def desconectar(self):
        if self.conexao:
            self.conexao.close()
        self.conexao = None
        self.cursor = None

    def criar_tabelas(self):
        self.conectar()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                quantidade INTEGER,
                preco REAL
            )
        ''')

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

        self.conexao.commit()
        self.desconectar()

    def inserir_produto(self, nome, descricao, quantidade, preco):
        self.conectar()
        self.cursor.execute('''
            INSERT INTO produtos (nome, descricao, quantidade, preco)
            VALUES (?, ?, ?, ?)
        ''', (nome, descricao, quantidade, preco))
        self.conexao.commit()
        self.desconectar()


    def atualizar_produto(self, produto_id, nome, descricao, quantidade, preco):
        self.conectar()
        self.cursor.execute('''
            UPDATE produtos
            SET nome=?, descricao=?, quantidade=?, preco=?
            WHERE id=?
        ''', (nome, descricao, quantidade, preco, produto_id))
        self.conexao.commit()
        self.desconectar()

    def remover_produto(self, produto_id):
        self.conectar()
        self.cursor.execute('DELETE FROM produtos WHERE id=?', (produto_id,))
        self.conexao.commit()
        self.desconectar()

    def listar_produtos(self):
        self.conectar()
        self.cursor.execute('SELECT * FROM produtos ORDER BY nome')
        produtos = self.cursor.fetchall()
        self.desconectar()
        return produtos

    def buscar_produto(self, produto_id):
        self.conectar()
        self.cursor.execute('SELECT * FROM produtos WHERE id=?', (produto_id,))
        produto = self.cursor.fetchone()
        self.desconectar()
        return produto

    def buscar_produto_por_nome(self, nome):
        self.conectar()
        self.cursor.execute('SELECT * FROM produtos WHERE nome LIKE ?', (f'%{nome}%',))
        produtos = self.cursor.fetchall()
        self.desconectar()
        return produtos

    def registrar_venda(self, produto_id, quantidade):
        self.conectar()
        self.cursor.execute('SELECT nome, quantidade, preco FROM produtos WHERE id=?', (produto_id,))
        resultado = self.cursor.fetchone()

        if resultado:
            nome_produto, estoque, preco_unitario = resultado
            if estoque >= quantidade:
                novo_estoque = estoque - quantidade
                self.cursor.execute('UPDATE produtos SET quantidade=? WHERE id=?',
                                    (novo_estoque, produto_id))

                total = preco_unitario * quantidade
                data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.cursor.execute('''
                    INSERT INTO vendas (produto_id, produto_nome, quantidade, preco_unitario, total, data)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (produto_id, nome_produto, quantidade, preco_unitario, total, data))

                self.conexao.commit()
                self.desconectar()
                return True

        self.desconectar()
        return False

    def listar_vendas(self):
        self.conectar()
        self.cursor.execute('''
            SELECT id, produto_nome, quantidade, preco_unitario, total, data FROM vendas
            ORDER BY data DESC
        ''')
        vendas = self.cursor.fetchall()
        self.desconectar()
        return vendas

    def total_produtos_vendidos(self):
        self.conectar()
        self.cursor.execute('SELECT SUM(quantidade) FROM vendas')
        total = self.cursor.fetchone()[0] or 0
        self.desconectar()
        return total

    def total_produtos_estoque(self):
        self.conectar()
        self.cursor.execute('SELECT SUM(quantidade) FROM produtos')
        total = self.cursor.fetchone()[0] or 0
        self.desconectar()
        return total
