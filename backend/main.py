from flask import Flask, render_template, request, jsonify
from gerenciador_estoque import GerenciadorEstoque
import os

app = Flask(
    __name__,
    template_folder=os.path.join("..", "frontend", "templates"),
    static_folder=os.path.join("..", "frontend", "static")
)

gerenciador = GerenciadorEstoque()

@app.route('/')
def index():
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
