from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from gerenciador_estoque import GerenciadorEstoque
import os
import re

app = Flask(
    __name__,
    template_folder=os.path.join("..", "frontend", "templates"),
    static_folder=os.path.join("..", "frontend", "static")
)
app.secret_key = 'sua_chave_secreta'

gerenciador = GerenciadorEstoque()

def cpf_valido(cpf):
    return re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = gerenciador.autenticar_usuario(email, senha)
        if usuario:
            session['usuario'] = usuario[1]  # nome
            session['usuario_email'] = usuario[2]
            return redirect(url_for('index'))
        else:
            error = 'E-mail ou senha inválidos.'
    return render_template('login.html', error=error)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    error = None
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        senha = request.form['senha']
        if not cpf_valido(cpf):
            error = 'CPF inválido. Use o formato 000.000.000-00.'
        else:
            try:
                gerenciador.cadastrar_usuario(nome, email, cpf, senha)
                flash('Cadastro realizado com sucesso! Faça login.')
                return redirect(url_for('login'))
            except ValueError as e:
                error = str(e)
    return render_template('cadastro.html', error=error)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('usuario_email', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    produtos = gerenciador.listar_produtos()
    vendas = gerenciador.listar_vendas()
    total_estoque = gerenciador.total_produtos_estoque()
    total_vendidos = gerenciador.total_produtos_vendidos()
    return render_template('index.html', 
                         produtos=produtos,
                         vendas=vendas,
                         total_estoque=total_estoque,
                         total_vendidos=total_vendidos)

# API endpoints
@app.route('/api/produtos', methods=['POST'])
def adicionar_produto():
    data = request.get_json()
    forcar = data.get('forcar', False)
    try:
        gerenciador.adicionar_produto(
            nome=data['nome'],
            descricao=data['descricao'],
            quantidade=int(data['quantidade']),
            preco=float(data['preco']),
            forcar=forcar
        )
        return jsonify({'success': True}), 201
    except ValueError as e:
        if str(e) == 'duplicado':
            return jsonify({'success': False, 'duplicate': True}), 200
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/produtos/<int:id>', methods=['PUT', 'DELETE'])
def gerenciar_produto(id):
    if request.method == 'PUT':
        data = request.get_json()
        try:
            gerenciador.editar_produto(
                produto_id=id,
                nome=data['nome'],
                descricao=data['descricao'],
                quantidade=int(data['quantidade']),
                preco=float(data['preco'])
            )
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    elif request.method == 'DELETE':
        try:
            gerenciador.remover_produto(id)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/vendas', methods=['POST'])
def registrar_venda():
    data = request.get_json()
    try:
        success = gerenciador.registrar_venda(
            produto_id=int(data['produto_id']),
            quantidade=int(data['quantidade'])
        )
        return jsonify({'success': success, 'message': 'Venda registrada' if success else 'Estoque insuficiente'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/buscar', methods=['GET'])
def buscar_produtos():
    termo = request.args.get('termo', '')
    produtos = gerenciador.buscar_produtos_por_nome(termo) if termo else []
    return jsonify([{
        'id': p.id, 'nome': p.nome, 'descricao': p.descricao, 
        'quantidade': p.quantidade, 'preco': p.preco
    } for p in produtos])

if __name__ == '__main__':
    app.run(debug=True)
